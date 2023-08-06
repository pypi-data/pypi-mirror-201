import csv
import gc
import logging
import re
import sys
import tracemalloc
from csv import DictReader
from io import StringIO
from random import randint

import django
import requests
from crossref.restful import Etiquette, Journals, Works
from django.db import transaction
from django.db.models import QuerySet, Count

from lxml import etree as ET


def expand_issns(issn) -> set:
    """
    Expands a list of ISSNs using the ISSNL lookup database.
    :param issn: the list of ISSNs to expand
    :return: a set of expanded ISSNs
    """
    from preservationdatabase.models import ISSN, ISSNL

    final_issn_list = []

    for issn_item in issn:
        final_issn_list.append(issn_item)
        issn_objs = ISSN.objects.filter(identifier=issn_item)
        issnl_objs = ISSNL.objects.filter(identifier=issn_item)

        for issn_obj in issn_objs:
            issnl_objs = ISSNL.objects.filter(
                identifier=issn_obj.issnl.identifier
            )

            for issnl_obj in issnl_objs:
                issn_reversed = ISSN.objects.filter(issnl=issnl_obj)

                for issn_reversed_obj in issn_reversed:
                    final_issn_list.append(issn_reversed_obj.identifier)

        for issn_reversed in issnl_objs:
            final_issn_list.append(issn_reversed.identifier)

            issn_objs = ISSN.objects.filter(issnl=issn_reversed)

            for issn_obj in issn_objs:
                final_issn_list.append(issn_obj.identifier)

    final_issn_list = set(final_issn_list)

    return final_issn_list


def show_preservation(
    container_title: str,
    issn: set,
    volume: str,
    no: str | None,
    doi: str,
    archive: str = None,
    year: str | None = None,
    no_issn: bool = False,
    verbose: bool = False,
) -> (dict | None, str):
    """
    Determine whether an item is preserved
    :param container_title: the journal/container name
    :param issn: the ISSN
    :param volume: the volume
    :param no: the number
    :param doi: the DOI
    :param no_issn: if true, will not look up ISSNs for expansion
    :param year: the year
    :param verbose: if true, will print status updates
    :param archive: the archive to query (or None for all archives)
    :return: a dictionary of preservations and a doi
    """
    from preservationdatabase import constants

    # extend ISSNs
    issn = [] if not issn else issn
    issn = set(issn)

    # extend the ISSN using the ISSNL lookup table
    if no_issn:
        final_issn_list = issn
    else:
        final_issn_list = expand_issns(issn)

    if issn != final_issn_list and verbose:
        logging.info(
            f"Expanded ISSN list for title from {issn} to {final_issn_list}"
        )

    if archive is None:
        preservation_systems = [*constants.archives.values()]
    else:
        preservation_systems = [constants.archives[archive]]

    preservations = {}

    for system in preservation_systems:
        preserved, done = system.preservation(
            container_title, final_issn_list, volume, no=no, year=year, doi=doi
        )
        preservations[system.name()] = preserved, done

    return preservations, doi


def unpack_range(s: str) -> list:
    """Converts a range of numbers to a full set"""
    r = []
    for i in s.split(","):
        if "-" not in i and " to " not in i:
            r.append(int(i))
        elif " to " in i:
            l, h = map(int, i.split(" to "))
            r += range(l, h + 1)
        else:
            l, h = map(int, i.split("-"))
            r += range(l, h + 1)
    return r


def show_preservation_for_doi(
    doi_input: str, archive: str = None, no_issn: bool = False
) -> (dict | None, str):
    """
    Determine whether a DOI is preserved with resolution via the REST API
    :param doi_input: the DOI to look up
    :param no_issn: if true, will not look up ISSNs for expansion
    :param archive: the archive to query (or None for all archives)
    :return:
    """

    my_etiquette = Etiquette(
        "Preservation Status", "0.01", "https://eve.gd", "meve@crossref.org"
    )

    works = Works(etiquette=my_etiquette)
    doi = works.doi(doi_input)

    if not doi:
        logging.info(f"Unable to resolve DOI: {doi_input}")
        return {}, doi_input

    container_title = (
        doi["container-title"] if "container-title" in doi else None
    )
    issns = set(doi["ISSN"]) if "ISSN" in doi else None

    volume = doi["volume"] if "volume" in doi else None
    no = doi["issue"] if "issue" in doi else None

    logging.info(
        f'Checking {doi["DOI"]}: {container_title} '
        f"({issns}) v{volume} n{no}"
    )

    year = None
    # "published": {"date-parts": [[2005, 12, 30]]}}}

    if "published" in doi:
        year = doi["published"]["date-parts"][0][0]

    preserves, doi_echo = show_preservation(
        container_title,
        issns,
        volume,
        no,
        doi,
        archive,
        year=year,
        no_issn=no_issn,
    )

    # the "archive" field is apparently returned if deposited

    archives = set(doi["archive"]) if "archive" in doi else set()

    if "archive" in doi:
        for archive in archives:
            if archive in preserves and preserves[archive][0]:
                logging.info(
                    f"{doi_input} correctly asserts preservation in {archive}."
                )
            else:
                logging.info(
                    f"{doi_input} incorrectly asserts preservation in {archive}."
                )

    else:
        logging.info(f"{doi_input} asserts no preservation information.")

    return preserves, doi_input


def normalize_doi(doi: str) -> str:
    """
    Normalize a DOI
    :param doi: the DOI to normalize
    :return: a DOI without the prefix
    """

    # extract the DOI from the input
    # note that this is not as rigorous as it could be, but writing a single
    # expression that captures everything is hard.
    # See: https://www.crossref.org/blog/dois-and-matching-regular-expressions/
    pattern = r"(10.\d{4,9}/[-._;()/:A-Z0-9]+)"

    result = re.search(pattern, doi, re.IGNORECASE)

    return result.group(0) if result else None


def generic_lockss_import(
    url: str, model, skip_first_line: bool = False, local: bool = False
) -> None:
    """
    The generic import function for LOCKSS-like models
    :param url: the URL to download
    :param model: the model class to use
    :param local: whether to use a local file
    :param skip_first_line: whether to skip the first line of the file
    :return: None
    """
    from preservationdatabase.models import Publisher

    # get CSV data
    csv_file = download_remote(local, model, url)

    # clear out
    clear_out(model)

    with StringIO(csv_file) as input_file:
        # skip the top line in the CSV which is something like
        # #Keepers CLOCKSS serials 2022-12-19
        if skip_first_line:
            next(input_file)

        csv_reader = DictReader(input_file)

        for row in csv_reader:
            # trim the publisher field if needed
            publisher_name = row["Publisher"][:254]

            publisher, created = Publisher.objects.get_or_create(
                name=publisher_name
            )

            if (
                model.name() == "CLOCKSS"
                or model.name() == "LOCKSS"
                or model.name() == "Cariniana"
            ):
                # create the item
                model.create_preservation(
                    issn=row["ISSN"],
                    eissn=row["eISSN"],
                    title=row["Title"],
                    preserved_volumes=row["Preserved Volumes"],
                    preserved_years=row["Preserved Years"],
                    in_progress_volumes=row["In Progress Volumes"],
                    in_progress_years=row["In Progress Years"],
                    publisher=publisher,
                    model=model,
                )
            elif model.name() == "PKP PLN":
                model.create_preservation(
                    issn=row["ISSN"],
                    title=row["Title"],
                    preserved_volumes=row["Vol"],
                    preserved_no=row["No"],
                    publisher=publisher,
                    model=model,
                )

            logging.info(f'Added {row["Title"]} to {model.name()} data')


def clear_out(model):
    if hasattr(model, "name"):
        logging.info(f"Clearing previous {model.name()} data")
    model.objects.all().delete()


def download_remote(
    local,
    model,
    url,
    bucket="",
    s3client=None,
    decode=True,
    file=False,
    filename="",
):
    if s3client:
        if not file:
            if decode:
                return (
                    s3client.get_object(Bucket=bucket, Key=url)["Body"]
                    .read()
                    .decode("utf-8")
                )
            else:
                return s3client.get_object(Bucket=bucket, Key=url)[
                    "Body"
                ].read()
        else:
            logging.info("Storing downloaded file as {}".format(filename))
            s3client.download_file(bucket, url, filename)
            return filename

    if not local:
        logging.info(f"Downloading: {model.name()} data")
        csv_file = requests.get(url).text
    else:
        logging.info(f"Using local file for {model.name()} data")

        if decode:
            with open(url, "r") as f:
                csv_file = f.read()
        else:
            with open(url, "rb") as f:
                csv_file = f.read()

    return csv_file


def preservation_status(
    model, container_title, issn, volume, no=None
) -> (dict | None, str):
    """
    Determine whether a DOI is preserved in model
    :param model: the model class to use
    :param container_title: the container title
    :param issn: the ISSN
    :param volume: the volume
    :param no: the issue number
    :return: A model item (or None) and a bool indicating whether the item is
    fully preserved
    """
    preserved_item = get_preserved_item_record(model, container_title, issn)

    if not preserved_item or len(preserved_item) == 0:
        return None, False

    for pi in preserved_item:
        vols = [x.strip() for x in pi.preserved_volumes.split(";")]
        vols_in_prog = [x.strip() for x in pi.in_progress_volumes.split(";")]

        volume = str(volume)

        if volume in vols:
            return preserved_item, True
        elif volume in vols_in_prog:
            return preserved_item, False

    return None, False


def get_preserved_item_record(model, container_title, issn) -> QuerySet | None:
    """
    Retrieves preservation records from the model
    :param model: the preservation model to use
    :param container_title: the name of the container
    :param issn: a list of ISSNs
    :return: a queryset of preservation model records or None
    """
    fields = [f.name for f in model._meta.get_fields()]

    # test ISSN
    try:
        if issn and "issn" in fields:
            preserved_item = None

            for sub_issn in issn:
                preserved_item = model.objects.filter(issn=sub_issn)
                if len(preserved_item) > 0:
                    break

            if not preserved_item or len(preserved_item) == 0:
                raise model.DoesNotExist
        else:
            raise model.DoesNotExist
    except model.DoesNotExist:
        # test EISSN
        try:
            if issn and "eissn" in fields:
                preserved_item = None

                for sub_issn in issn:
                    preserved_item = model.objects.filter(eissn=sub_issn)
                    if len(preserved_item) > 0:
                        break

                if not preserved_item or len(preserved_item) == 0:
                    raise model.DoesNotExist
            else:
                raise model.DoesNotExist
        except model.DoesNotExist:
            # test container title
            try:
                if container_title and "container_title" in fields:
                    preserved_item = model.objects.filter(title=container_title)
                    if not preserved_item or len(preserved_item) == 0:
                        raise model.DoesNotExist
                else:
                    raise model.DoesNotExist
            except model.DoesNotExist:
                return None

    return preserved_item


def process_onix(xml_file, elements, callback) -> None:
    """
    A faster method for processing ONIX XML than using DOM methods
    """
    current_object = {"volumes": [], "issues": []}

    collect = False

    count = 0

    for event, elem in ET.iterparse(xml_file, events=("start", "end")):
        if (
            event == "end"
            and elem.tag == "{http://www.editeur.org/onix/"
            "serials/SOH}HoldingsRecord"
        ):
            callback(current_object)

            gc.collect()

            current_object = {"volumes": [], "issues": []}

            count = count + 1
            stats = []

            filters = [tracemalloc.Filter(inclusive=True, filename_pattern="*")]

            if count % 100 == 0:
                django.db.reset_queries()

            # free memory (urgh)
            # a note: without this, the elementree will simply grow in memory
            # and previously iterated elements will not be garbage collected
            elem.clear()

        # detect if it's an ISSN
        if (
            event == "start"
            and elem.tag == "{http://www.editeur.org/onix/"
            "serials/SOH}ResourceVersionIDType"
            and elem.text == "07"
        ):
            collect = True
        elif (
            event == "start"
            and elem.tag == "{http://www.editeur.org/onix/"
            "serials/SOH}ResourceVersionIDType"
            and elem.text != "07"
        ):
            collect = False

        if (
            event == "start"
            and elem.tag == "{http://www.editeur.org/onix/"
            "serials/SOH}IDValue"
            and collect
        ):
            current_object["issn"] = normalize_issn(elem.text)

        if (
            event == "start"
            and elem.tag == "{http://www.editeur.org/onix/"
            "serials/SOH}TitleText"
            and collect
        ):
            current_object["title"] = elem.text

        if (
            event == "start"
            and elem.tag == "{http://www.editeur.org/onix/"
            "serials/SOH}PublisherName"
            and collect
        ):
            current_object["publisher"] = elem.text

        if (
            event == "start"
            and elem.tag == "{http://www.editeur.org/onix/"
            "serials/SOH}Coverage"
            and collect
        ):
            coverage = elem

            volume = ""
            issue = ""

            level_one = coverage.find(
                ".//{http://www.editeur.org/onix/serials/SOH}Level1"
            )
            level_two = coverage.find(
                ".//{http://www.editeur.org/onix/serials/SOH}Level2"
            )

            levels = [level_one, level_two]
            unit = None

            for level in levels:
                if level:
                    unit = level.find(
                        ".//{http://www.editeur.org/onix/serials/SOH}Unit"
                    )

                    # no idea why, but this HAS to be an explicit comparison
                    # with None rather than a boolean comparison
                    unit = unit.text if unit is not None else None

                    number = level.find(
                        ".//{http://www.editeur.org/onix/serials/SOH}Number"
                    )

                    number = number.text if number is not None else None

                    if unit == "Volume":
                        volume = number
                    elif unit == "Issue":
                        issue = number
                    else:
                        print("Unrecognised unit: {}".format(unit))

            if unit:
                current_object["volumes"].append(volume)
                current_object["issues"].append(issue)

        if (
            event == "start"
            and elem.tag == "{http://www.editeur.org/onix/"
            "serials/SOH}PreservationStatusCode"
            and collect
        ):
            current_object["status"] = elem.text

        if (
            event == "start"
            and elem.tag == "{http://www.editeur.org/onix/"
            "serials/SOH}VerificationStatus"
            and collect
        ):
            current_object["verification"] = elem.text

    return


def normalize_issn(issn) -> str:
    """
    Normalizes an ISSN
    :param issn: the ISSN
    :return: the normalized ISSN
    """
    issn = "" if issn is None else issn.strip()

    return f"{issn[0:4]}-{issn[4:8]}" if issn and "-" not in issn else issn


@transaction.atomic
def random_db_entries(model, count, only_crossref=False) -> list:
    """
    Returns random entries from a database model
    :param model: the model to use
    :param count: the number of random entries to return
    :param only_crossref: whether to only return crossref entries
    :return: a list of random entries
    """

    # NB we do it like this because queryset.order_by('?') can be incredibly
    # slow
    output = []

    total = model.objects.all().count()

    my_etiquette = Etiquette(
        "Preservation Status", "0.01", "https://eve.gd", "meve@crossref.org"
    )

    jrnls = Journals(etiquette=my_etiquette)

    while len(output) < count - 1:
        random_index = randint(0, total - 1)

        entry = model.objects.all()[random_index]

        if only_crossref:
            append = False

            new_issns = expand_issns([entry.issn])

            for issn in new_issns:
                jrnl = jrnls.journal(issn=issn)

                if jrnl:
                    append = True
                    break

            if hasattr(entry, "eissn"):
                new_eissns = expand_issns([entry.eissn])

                for issn in new_eissns:
                    jrnl = jrnls.journal(issn=issn)

                    if jrnl:
                        append = True
                        break

            if append:
                output.append(entry)
                print(
                    "Found crossref entry ({}): {}".format(len(output), entry)
                )
        else:
            output.append(entry)

    return output


def in_archive(item, archive) -> bool:
    """
    Determines whether a container is in an archive
    :param item: the container to check
    :param archive: the archive to check
    :return: True if both items are in the same archive, False otherwise
    """

    fields = item._meta.fields

    if "issn" in fields:
        issns = archive.objects.filter(issn=item["issn"])

        if len(issns) > 0:
            return True

    if "eissn" in fields:
        try:
            issns = archive.objects.filter(eissn=item["eissn"])

            if len(issns) > 0:
                return True
        except:
            issns = archive.objects.filter(issn=item["eissn"])

            if len(issns) > 0:
                return True

    if "title" in fields:
        titles = archive.objects.filter(title=item["title"])

        if len(titles) > 0:
            return True

    return False


def import_issnl(issnl_file, issnl_model, issn_model):
    from rich.progress import track

    csv.field_size_limit(sys.maxsize)

    clear_out(issn_model)
    clear_out(issnl_model)

    logging.info("Erased existing ISSN-ISSNL mappings.")

    with open(issnl_file, "r") as input_file:
        csv_reader = csv.DictReader(input_file, delimiter="\t")

        for row in track(csv_reader):
            if row["ISSN"] != row["ISSN-L"]:
                issnl, created = issnl_model.objects.get_or_create(
                    identifier=row["ISSN-L"]
                )

                issn, created = issn_model.objects.get_or_create(
                    identifier=row["ISSN"], issnl=issnl
                )

                logging.info(
                    f"Created ISSN-ISSNL mapping: {issn.identifier} {issnl.identifier}"
                )
