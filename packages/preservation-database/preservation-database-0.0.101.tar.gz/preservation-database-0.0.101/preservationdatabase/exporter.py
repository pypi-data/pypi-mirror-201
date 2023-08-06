import hashlib
import json
import logging
import os
import sys
from collections import defaultdict, OrderedDict
from datetime import date, datetime
from typing import DefaultDict, Any

from caseconverter import kebabcase

SAMPLES_BUCKET = "samples.research.crossref.org"
SAMPLES_PATH = "members-works/2023-03-05/samples/"

ANNOTATION_BUCKET = "outputs.research.crossref.org"
ANNOTATION_PATH = "annotations"
ANNOTATION_FILENAME = "preservation.json"

REPORT_BUCKET = "outputs.research.crossref.org"
REPORT_PATH = "reports"
REPORT_FILENAME = "preservation.json"

CODE_BUCKET = "airflow-crossref-research-annotation"

PARALLEL_JOBS = 5

import boto3


def get_members(
    s3client=None, samples_bucket=None, samples_path=None
) -> list[str]:
    """
    Retrieves the list of members from the S3 bucket
    :param s3client: the s3client object to use to fetch
    :param samples_bucket: the name of the samples bucket
    :param samples_path: the path of the samples object
    :return: a list of strings of member IDs
    """

    # the samples research bucket contains JSON-L with the filename
    # schema member-1.jsonl etc.
    # Note also: we use S3 for this so that we definitely know what
    # files are available, rather than the REST API (in case there is
    # a bug in the sampling framework that leads to an unavailable
    # object)

    if not s3client:
        s3client = boto3.client("s3")

    import re

    r = re.compile(r"member-(\d+).jsonl")
    return [
        m.group(1)
        for m in map(
            r.match,
            list_bucket(
                s3client,
                samples_bucket=samples_bucket,
                samples_path=samples_path,
            ),
        )
        if m is not None
    ]


def list_bucket(s3client, samples_bucket, samples_path) -> list[str]:
    """
    Lists the contents of the samples bucket
    :param s3client: the s3client object to use to fetch
    :param samples_bucket: the name of the samples bucket
    :param samples_path: the path of the samples object
    :return: a list of object names
    """

    paginator = s3client.get_paginator("list_objects_v2")
    member_list = []

    for page in paginator.paginate(
        Bucket=samples_bucket, Prefix=f"{samples_path}"
    ):
        for obj in page["Contents"]:
            filename = obj["Key"]
            member_list.append(filename.split("/")[-1])

    return member_list


def get_samples(
    s3client, member_id, samples_bucket, samples_path, verbose=False
) -> list:
    """
    Retrieves the list of samples from the S3 bucket
    :param s3client: the s3client object to use to fetch
    :param samples_bucket: the name of the samples bucket
    :param samples_path: the path of the samples object
    :param member_id: the ID of the member to retrieve
    :param verbose: whether to log progress
    :return: a list of samples
    """

    key = f"{samples_path}member-{member_id}.jsonl"

    data = (
        s3client.get_object(Bucket=samples_bucket, Key=key)["Body"]
        .read()
        .decode("utf-8")
    )

    from io import StringIO
    import logging

    with StringIO(data) as json_file:
        output = list(json_file)
        if verbose:
            logging.info(
                f"Found {len(output)} samples for " f"member {member_id}"
            )
        return output


def preservation_status(result) -> (dict, str):
    """
    Return preservation statistics for a specific member
    :param result: the pre-parsed JSON entry of the member
    :return: 2-tuple: dictionary of preservations and the DOI string
    """
    from utils import show_preservation

    container_title = (
        result["container-title"] if "container-title" in result else None
    )
    issn = result["ISSN"] if "ISSN" in result else None
    volume = result["volume"] if "volume" in result else None

    # not in sampling framework (yet)
    no = None

    year = None
    # "published": {"date-parts": [[2005, 12, 30]]}}}

    if "published" in result:
        year = result["published"]["date-parts"][0][0]

    return show_preservation(
        container_title=container_title,
        issn=issn,
        volume=volume,
        no=no,
        doi=result,
        year=year,
    )


def score(
    one_archive, two_archives, three_archives, sample_count, verbose=False
):
    score = "Unclassified"

    if sample_count > 0:
        if verbose:
            logging.info(
                "Score for Bronze is: {}. Needs to be greater than 0.25".format(
                    (one_archive / sample_count)
                    + (two_archives / sample_count)
                    + (three_archives / sample_count)
                )
            )

            logging.info(
                "Score for Silver is: {}. Needs to be greater than 0.50".format(
                    (two_archives / sample_count)
                    + (three_archives / sample_count)
                )
            )

            logging.info(
                "Score for Gold is: {}. Needs to be greater than 0.75".format(
                    (three_archives / sample_count)
                )
            )

        # 25% in 1 or more archives
        if (
            (one_archive / sample_count)
            + (two_archives / sample_count)
            + (three_archives / sample_count)
        ) >= 0.25:
            score = "Bronze"

        # 50% in 2 or more archives
        if (
            (two_archives / sample_count) + (three_archives / sample_count)
        ) >= 0.50:
            score = "Silver"

        # 75% in 3 archives
        if (three_archives / sample_count) >= 0.75:
            score = "Gold"

    return score


def process_member_sample(samples, sample_path, verbose=False) -> dict:
    """
    Processes samples for a single member
    :param samples: the samples to process
    :param sample_path: the path of the sample
    :param verbose: whether to print the sample
    :return: a dictionary of preservation statistics
    """
    from constants import archives
    from datetime import datetime
    import json

    from collections import defaultdict

    overall_status: DefaultDict[Any, Any] = defaultdict(int)

    # date stamp this output
    overall_status["about"] = {
        "date-generated": str(datetime.now()),
        "sample-file": sample_path,
    }

    three_archives = 0
    two_archives = 0
    one_archive = 0

    session = boto3.Session()
    s3 = session.resource("s3")

    for sample_item in samples:
        result = json.loads(sample_item)["data-point"]

        overall_status["about"]["member"] = result["member"]
        overall_status["unpreserved-items"] = list()

        # we can only work with journal articles
        # we exclude journal articles from the current year because they
        # most likely have not been ingested into digital preservation
        # systems yet
        if "type" in result and result["type"] == "journal-article":
            year_published = (
                result["published"]["date-parts"][0][0]
                if "published" in result
                else None
            )

            if year_published and str(year_published) != str(date.today().year):
                has_preservation = False
                archive_count = 0

                preservation_statuses, doi = preservation_status(result)

                md5_doi = hashlib.md5(doi["DOI"].lower().encode()).hexdigest()
                aws_key = (
                    f"{ANNOTATION_PATH}/works/{md5_doi}/{ANNOTATION_FILENAME}"
                )

                preserved_json = {
                    "about": {
                        "DOI": doi["DOI"],
                        "date-generated": str(datetime.now()),
                    }
                }

                # increment the sample count
                overall_status["sample-count"] += 1

                for key, value in preservation_statuses.items():
                    preserved, done = value

                    if preserved:
                        has_preservation = True

                        # increment this archive's stats
                        overall_status[key] += 1

                        # increment the archive counter
                        archive_count += 1

                        # increment total preservation instances count
                        overall_status["preservation-instances"] += 1

                        # log this for DOI-level annotation
                        if done:
                            preserved_json[key] = "preserved"
                        else:
                            preserved_json[key] = "preserved (in progress)"

                    else:
                        preserved_json[key] = "unpreserved"

                new_annotation = {}

                for key, value in preserved_json.items():
                    new_key = normalize_json_key(key)
                    new_annotation[new_key] = value

                push_json_to_s3(
                    s3=s3,
                    json_obj=new_annotation,
                    bucket=ANNOTATION_BUCKET,
                    path=aws_key,
                )

                # preserved_count refers to the number of works with at
                # least one preservation
                if has_preservation:
                    overall_status["preserved-count"] += 1

                    if verbose:
                        logging.info(f"{doi['DOI']} has a preservation")
                        logging.info(
                            f"Running total: "
                            f"{overall_status['preserved-count']} preserved, "
                            f"{overall_status['unpreserved-count']} unpreserved"
                        )

                else:
                    overall_status["unpreserved-count"] += 1

                    overall_status["unpreserved-items"].append(doi["DOI"])

                    if verbose:
                        logging.info(f"{doi['DOI']} has no preservation")
                        logging.info(
                            f"Running total: "
                            f"{overall_status['preserved-count']} preserved, "
                            f"{overall_status['unpreserved-count']} unpreserved"
                        )

                # increment the correct counters for overall stats
                if archive_count == 1:
                    one_archive += 1
                elif archive_count == 2:
                    two_archives += 1
                elif archive_count > 2:
                    three_archives += 1
            else:
                overall_status["excluded-current-year"] += 1
                if verbose:
                    logging.info(
                        f"{result['DOI']} is excluded as is too recent"
                    )
        else:
            # this is an excluded sample item
            if "type" in result and result["type"] != "journal-article":
                overall_status["excluded-non-journal"] += 1
                if verbose:
                    logging.info(
                        f"{result['DOI']} is excluded as it is not a journal "
                        f"article"
                    )
            elif "published" not in result:
                overall_status["excluded-no-date"] += 1
                if verbose:
                    logging.info(
                        f"{result['DOI']} is excluded as it is not a journal "
                        f"article"
                    )
            elif date.today().year == result["published"]["date-parts"][0][0]:
                overall_status["excluded-current-year"] += 1
                if verbose:
                    logging.info(
                        f"{result['DOI']} is excluded as is too recent"
                    )

    # add blank keys for archives that weren't used
    for preservation_system, class_o in archives.items():
        if class_o.name() not in overall_status:
            overall_status[class_o.name()] = 0

    # calculate percentage of preservation
    if overall_status["sample-count"] > 0:
        overall_status["percentage-preserved"] = (
            overall_status["preserved-count"] / overall_status["sample-count"]
        ) * 100
    else:
        overall_status["percentage-preserved"] = 0

    # add the counters
    overall_status["preserved-in-one-archive"] = one_archive
    overall_status["preserved-in-two-archives"] = two_archives
    overall_status["preserved-in-three-or-more-archives"] = three_archives

    # determine the classes
    overall_status["member-grade"] = score(
        one_archive,
        two_archives,
        three_archives,
        overall_status["sample-count"],
    )

    return overall_status


def score_member(member_id):
    return rescore_member(
        ANNOTATION_BUCKET,
        ANNOTATION_FILENAME,
        ANNOTATION_PATH,
        SAMPLES_BUCKET,
        SAMPLES_PATH,
        member_id,
        CODE_BUCKET,
        push_to_s3=False,
        verbose=True,
    )


def push_json_to_s3(
    s3,
    json_obj,
    bucket,
    path,
    verbose=False,
) -> None:
    """
    Writes the JSON data to S3
    :param s3: the s3 object to use
    :param bucket: the name of the bucket
    :param path: the path of the object to store
    :param json_obj: the JSON to write
    :param verbose: whether to print status messages
    :return:
    """
    import json
    import logging

    if verbose:
        logging.info("Normalizing JSON keys")

    json_obj = normalize_json_keys(json_obj)

    if verbose:
        logging.info(f"Writing JSON to S3 bucket {bucket} at path {path}")

    obj = s3.Object(bucket, path)
    obj.put(Body=json.dumps(json_obj))


def normalize_json_keys(json_obj: dict) -> dict:
    """
    Always normalize keys to kebab case
    :param json_obj: the JSON object to normalize
    :return: a new JSON object with normalized keys
    """
    new_json_obj = {}

    if isinstance(json_obj, list):
        new_json_obj = []

        for item in json_obj:
            new_item = {}

            for key in item:
                new_item[normalize_json_key(key)] = item[key]

            new_json_obj.append(new_item)
    else:
        for key in json_obj.keys():
            new_json_obj[normalize_json_key(key)] = json_obj[key]

    return new_json_obj


def normalize_json_key(key: str) -> str:
    """
    Normalize keys to kebab case
    :param key: the key to normalize
    :return: the normalized key
    """
    # while it seems overkill to have this as a separate function,
    # it's useful in other contexts, too, to have it on its own
    return kebabcase(key)


def process_sample(
    annotation_bucket,
    annotation_filename,
    annotation_path,
    samples_bucket,
    samples_path,
    member_id,
    code_bucket,
    verbose=False,
):
    """
    Process a single member sample
    :param annotation_bucket: the annotation bucket
    :param annotation_filename: the annotation filename
    :param annotation_path: the annotation path
    :param samples_bucket: the samples bucket
    :param samples_path: the samples path
    :param member_id: the member id
    :param verbose: whether to print status messages
    :param code_bucket: the code bucket where settings are located
    :return:
    """
    import logging

    # the environment setup is needed for logging etc. because of the
    # joblib parallelization
    import environment

    environment.setup_environment(code_bucket, download_settings=False)

    import boto3

    s3client = boto3.client("s3")
    session = boto3.Session()
    s3 = session.resource("s3")

    if verbose:
        logging.info(f"Processing member {member_id}")

    samples = get_samples(
        s3client,
        member_id,
        samples_bucket=samples_bucket,
        samples_path=samples_path,
    )

    overall_status = process_member_sample(
        samples, samples_path, verbose=verbose
    )

    key = f"{annotation_path}/members/{member_id}/{annotation_filename}"

    push_json_to_s3(
        s3=s3,
        json_obj=overall_status,
        bucket=annotation_bucket,
        path=key,
        verbose=True,
    )

    return {member_id: overall_status}


def generate_report(resume_from: int):
    import boto3
    import logging
    from rich.progress import track

    s3client = boto3.client("s3")

    from joblib import Parallel, delayed

    # get member list from S3
    members = get_members(
        s3client=s3client,
        samples_bucket=SAMPLES_BUCKET,
        samples_path=SAMPLES_PATH,
    )

    logging.info(f"There are {len(members)} to process.")

    # we resume from the resume form, in the order returned by the S3 bucket
    if resume_from > 0:
        index_slice = members.index(str(resume_from))
        members = members[index_slice:]

        logging.info(f"After resume, there are now {len(members)} to process.")

    # the results of the parallel processing are dictionaries with
    # the member ID as the key and a dictionary of preservation statistics
    # as the value.

    results = Parallel(n_jobs=PARALLEL_JOBS)(
        delayed(process_sample)(
            ANNOTATION_BUCKET,
            ANNOTATION_FILENAME,
            ANNOTATION_PATH,
            SAMPLES_BUCKET,
            SAMPLES_PATH,
            member_id,
            CODE_BUCKET,
        )
        for member_id in track(members)
    )

    return members


def member_reports():
    s3client = boto3.client("s3")
    session = boto3.Session()
    s3 = session.resource("s3")

    # get member list from S3
    members = get_members(
        s3client=s3client,
        samples_bucket=SAMPLES_BUCKET,
        samples_path=SAMPLES_PATH,
    )

    from joblib import Parallel, delayed
    from rich.progress import track

    results = Parallel(n_jobs=PARALLEL_JOBS)(
        delayed(member_report)(
            member_id,
        )
        for member_id in track(members)
    )


def member_report(member_id):
    import boto3
    import logging

    s3client = boto3.client("s3")
    session = boto3.Session()
    s3 = session.resource("s3")

    samples = get_samples(
        s3client=s3client,
        member_id=member_id,
        samples_bucket=SAMPLES_BUCKET,
        samples_path=SAMPLES_PATH,
    )

    overall_samples = []
    unpreserved_samples = []

    import botocore

    for sample in samples:
        sample = json.loads(sample)["data-point"]

        if "type" in sample and sample["type"] == "journal-article":
            year = None

            if "published" in sample:
                year = sample["published"]["date-parts"][0][0]

            if sample["DOI"] == "10.16995/glossa.8784":
                print("FOUND ARTICLE")
                print(str(year))
                print(str(datetime.now().year))
                print(str(year) != str(datetime.now().year))
                print(sample)

            if str(year) != str(datetime.now().year):
                md5_doi = hashlib.md5(
                    sample["DOI"].lower().encode()
                ).hexdigest()

                try:
                    annotation = get_annotation(
                        s3client=s3client,
                        member_id=member_id,
                        annotation_name="preservation.json",
                        annotations_bucket=ANNOTATION_BUCKET,
                        annotations_path=ANNOTATION_PATH,
                        path=f"works/{md5_doi}",
                        use_member_id=False,
                    )

                    preserved = any(
                        v.startswith("preserved")
                        for v in annotation.values()
                        if isinstance(v, str)
                    )

                    if not preserved:
                        unpreserved_samples.append(annotation)

                    overall_samples.append(annotation)

                except Exception as e:
                    ...
                    # print(e)
                    # print(f"This DOI was excluded: {sample['DOI']}")

    key = f"{REPORT_PATH}/members/{member_id}/preservation-report.json"
    unpreserved_key = f"{REPORT_PATH}/members/{member_id}/unpreserved.json"

    push_json_to_s3(
        s3=s3,
        json_obj=unpreserved_samples,
        bucket=REPORT_BUCKET,
        path=unpreserved_key,
        verbose=True,
    )

    push_json_to_s3(
        s3=s3,
        json_obj=overall_samples,
        bucket=REPORT_BUCKET,
        path=key,
        verbose=True,
    )


def rescore_member(
    annotation_bucket,
    annotation_filename,
    annotation_path,
    samples_bucket,
    samples_path,
    member_id,
    code_bucket,
    verbose=False,
    push_to_s3=True,
):
    import environment

    environment.setup_environment(code_bucket, download_settings=False)

    import boto3
    import logging

    s3client = boto3.client("s3")
    session = boto3.Session()
    s3 = session.resource("s3")

    try:
        preservations = get_annotation(
            s3client=s3client,
            annotations_bucket=ANNOTATION_BUCKET,
            annotations_path=ANNOTATION_PATH,
            member_id=member_id,
            annotation_name="preservation.json",
        )

        one_archive = preservations["preserved-in-one-archive"]
        two_archives = preservations["preserved-in-two-archives"]
        three_archives = preservations["preserved-in-three-or-more-archives"]

        sample_count = preservations["sample-count"]

        # determine the classes
        preservations["member-grade"] = score(
            one_archive,
            two_archives,
            three_archives,
            preservations["sample-count"],
            verbose=verbose,
        )

        key = f"{annotation_path}/members/{member_id}/{annotation_filename}"

        if verbose:
            logging.info(
                f"Rescoring member {member_id} as "
                f"{preservations['member-grade']}"
            )

        if push_to_s3:
            push_json_to_s3(
                s3=s3,
                json_obj=preservations,
                bucket=annotation_bucket,
                path=key,
            )

        return preservations["member-grade"]
    except Exception as e:
        logging.error(f"Unable to rescore member {member_id}. Error follows.")
        raise e


def overall_report(members=None, limit=0):
    import boto3
    import logging

    s3client = boto3.client("s3")
    session = boto3.Session()
    s3 = session.resource("s3")

    if not members:
        # get member list from S3
        members = get_members(
            s3client=s3client,
            samples_bucket=SAMPLES_BUCKET,
            samples_path=SAMPLES_PATH,
        )

    if limit > 0:
        members = members[:limit]

    # overall reports we want to build:
    # 1. Breakdown by member size
    # 2. Totally unpreserved members ["percentage-preserved"]
    # 3. Members with 75% in three archives (gold standard) ["member-grade"]
    # 4. Members with 50% in two archives (silver standard) ["member-grade"]
    # 5. Members with 25% in one archive (bronze standard) ["member-grade"]

    member_tier_names = [
        "<USD 1 million",
        "USD 1 million - USD 5 million",
        "USD 5 million - USD 10 million",
        "USD 10 million - USD 25 million",
        "USD 25 million - USD 50 million",
        "USD 50 million - USD 100 million",
        "USD 100 million - USD 200 million",
        "USD 200 million - USD 500 million",
        ">USD 500 million",
    ]

    member_tiers = {
        "<USD 1 million": 275,
        "USD 1 million - USD 5 million": 550,
        "USD 5 million - USD 10 million": 1650,
        "USD 10 million - USD 25 million": 3900,
        "USD 25 million - USD 50 million": 8300,
        "USD 50 million - USD 100 million": 14000,
        "USD 100 million - USD 200 million": 22000,
        "USD 200 million - USD 500 million": 33000,
        ">USD 500 million": 50000,
    }

    size_bracket_names = [
        "Unknown",
        "1-10",
        "11-100",
        "101-500",
        "501-1,000",
        "1,001-10,000",
        "10,001-100,000",
        "100,001-1,000,000",
        "1,000,001+",
    ]

    size_brackets = OrderedDict(
        {
            0: 0,
            1: 10,
            11: 100,
            101: 500,
            501: 1000,
            1001: 10000,
            10001: 100000,
            100001: 1000000,
            1000001: -1,
        }
    )

    gold_members = {member_tier: 0 for member_tier in member_tier_names}
    silver_members = {member_tier: 0 for member_tier in member_tier_names}
    bronze_members = {member_tier: 0 for member_tier in member_tier_names}
    unclassified_members = {member_tier: 0 for member_tier in member_tier_names}

    gold_members_by_country = defaultdict(int)
    silver_members_by_country = defaultdict(int)
    bronze_members_by_country = defaultdict(int)
    unclassified_members_by_country = defaultdict(int)

    gold_members_by_size = {
        size_bracket: 0 for size_bracket in size_bracket_names
    }
    silver_members_by_size = {
        size_bracket: 0 for size_bracket in size_bracket_names
    }
    bronze_members_by_size = {
        size_bracket: 0 for size_bracket in size_bracket_names
    }
    unclassified_members_by_size = {
        size_bracket: 0 for size_bracket in size_bracket_names
    }

    gold_member_ids = []
    silver_member_ids = []
    bronze_member_ids = []
    unclassified_member_ids = []

    total_items_unpreserved = 0
    total_items_preserved = 0
    total_preservation_instances = 0
    total_items_sampled = 0

    plus_token = os.environ.get("CROSSREF_PLUS_TOKEN", None)

    from crossref.restful import Etiquette, Members

    my_etiquette = Etiquette(
        "Preservation Status",
        "0.01",
        "https://eve.gd",
        "meve@crossref.org",
    )

    for member in members:
        logging.info(f"Fetching preservation statistics for member {member}")

        if plus_token:
            members = Members(
                etiquette=my_etiquette,
                crossref_plus_token=plus_token,
            )
            logging.info(f"Using plus lookup")
        else:
            members = Members(etiquette=my_etiquette)
            logging.info(f"Using regular lookup")

        logging.info(f"API lookup for {member}: done")

        member_obj = members.member(member)

        if "primary-name" not in member_obj:
            print(member_obj)

        preservations = get_annotation(
            s3client=s3client,
            annotations_bucket=ANNOTATION_BUCKET,
            annotations_path=ANNOTATION_PATH,
            member_id=member,
            annotation_name="preservation.json",
        )

        member_data = get_annotation(
            s3client=s3client,
            member_id=member,
            annotations_bucket=ANNOTATION_BUCKET,
            annotations_path=ANNOTATION_PATH,
            annotation_name="member-profile.json",
        )

        logging.info(f"S3 fetches for member {member}: done")

        try:
            annual_fee = int(member_data["annual-fee"])
        except ValueError:
            annual_fee = 0

        member_band = None

        logging.info(
            f"{member_obj['primary-name']} has an annual fee of {annual_fee}"
        )

        for key, val in member_tiers.items():
            if annual_fee <= int(val):
                # put this member in this band
                logging.info(f"{member_obj['primary-name']} is in band {key}")
                member_band = key
                break

            if member_band:
                break

        if not member_band:
            logging.warning(f"Unable to classify this member ({member})")

        # now log the country here
        country = member_obj["location"].split(",")[-1]

        # size em up
        deposits = member_obj["counts"]["total-dois"]

        size = None

        for key, val in size_brackets.items():
            if deposits == 0:
                size = "Unknown"
            elif val == -1:
                # special case
                if deposits >= key:
                    size = size_bracket_names[
                        list(size_brackets.keys()).index(key)
                    ]
            elif key <= deposits <= val:
                size = size_bracket_names[list(size_brackets.keys()).index(key)]

        total_items_preserved += (
            preservations["preserved-count"]
            if "preserved-count" in preservations
            else 0
        )
        total_items_unpreserved += (
            preservations["unpreserved-count"]
            if "unpreserved-count" in preservations
            else 0
        )
        total_preservation_instances += (
            preservations["preservation-instances"]
            if "preservation-instances" in preservations
            else 0
        )
        total_items_sampled += (
            preservations["sample-count"]
            if "sample-count" in preservations
            else 0
        )

        # this calculates the preservation grades for different member tiers
        # using fee level as the benchmark
        if preservations["member-grade"] == "Bronze":
            logging.info(f"{member_obj['primary-name']} is Bronze")
            bronze_members[member_band] += 1
            bronze_members_by_country[country] += 1
            bronze_members_by_size[size] += 1
            bronze_member_ids.append(f"{member_obj['primary-name']} ({member})")
        elif preservations["member-grade"] == "Silver":
            logging.info(f"{member_obj['primary-name']} is Silver")
            silver_members[member_band] += 1
            silver_members_by_country[country] += 1
            silver_members_by_size[size] += 1
            silver_member_ids.append(f"{member_obj['primary-name']} ({member})")
        elif preservations["member-grade"] == "Gold":
            logging.info(f"{member_obj['primary-name']} is Gold")
            gold_members[member_band] += 1
            gold_members_by_country[country] += 1
            gold_members_by_size[size] += 1
            gold_member_ids.append(f"{member_obj['primary-name']} ({member})")
        else:
            logging.info(f"{member_obj['primary-name']} is Unclassified")
            unclassified_members[member_band] += 1
            unclassified_members_by_country[country] += 1
            unclassified_members_by_size[size] += 1
            unclassified_member_ids.append(
                f"{member_obj['primary-name']} ({member})"
            )

    gold_totals = sum(gold_members.values())
    silver_totals = sum(silver_members.values())
    bronze_totals = sum(bronze_members.values())
    unclassified_totals = sum(unclassified_members.values())

    # bundle this all up
    overall_result = {
        "gold-members-by-fee": gold_members,
        "silver-members-by-fee": silver_members,
        "bronze-members-by-fee": bronze_members,
        "unclassified-members-by-fee": unclassified_members,
        "gold-totals": gold_totals,
        "silver-totals": silver_totals,
        "bronze-totals": bronze_totals,
        "unclassified-totals": unclassified_totals,
        "gold-members-by-country": gold_members_by_country,
        "silver-members-by-country": silver_members_by_country,
        "bronze-members-by-country": bronze_members_by_country,
        "unclassified-members-by-country": unclassified_members_by_country,
        "gold-members-by-size": gold_members_by_size,
        "silver-members-by-size": silver_members_by_size,
        "bronze-members-by-size": bronze_members_by_size,
        "unclassified-members-by-size": unclassified_members_by_size,
        "total-items-preserved": total_items_preserved,
        "total-items-unpreserved": total_items_unpreserved,
        "total-preservation-instances": total_preservation_instances,
        "total-items-sampled": total_items_sampled,
        "gold-member-ids": gold_member_ids,
        "silver-member-ids": silver_member_ids,
        "bronze-member-ids": bronze_member_ids,
        "unclassified-member-ids": unclassified_member_ids,
    }

    key = f"{REPORT_PATH}/{REPORT_FILENAME}"

    push_json_to_s3(
        s3=s3,
        json_obj=overall_result,
        bucket=REPORT_BUCKET,
        path=key,
    )

    return overall_result


def member_position(members=None, limit=0, member_id=None):
    import boto3
    import logging

    s3client = boto3.client("s3")
    session = boto3.Session()
    s3 = session.resource("s3")

    if not members:
        # get member list from S3
        members = get_members(
            s3client=s3client,
            samples_bucket=SAMPLES_BUCKET,
            samples_path=SAMPLES_PATH,
        )

    logging.info(
        f"Member {member_id} is at position {members.index(member_id)} of {len(members)} ({members.index(member_id) / len(members) * 100}%)"
    )


def rename_keys(members=None, limit=0, member_id=None):
    import boto3
    import logging

    s3client = boto3.client("s3")
    session = boto3.Session()
    s3 = session.resource("s3")

    if not members:
        # get member list from S3
        members = get_members(
            s3client=s3client,
            samples_bucket=SAMPLES_BUCKET,
            samples_path=SAMPLES_PATH,
        )

    for member in members:
        member_annotation = get_annotation(
            s3client,
            member,
            ANNOTATION_BUCKET,
            ANNOTATION_PATH,
            "preservation.json",
        )

        new_annotation = {}

        for key, value in member_annotation.items():
            new_key = normalize_json_key(key)
            new_annotation[new_key] = value

        key = f"{ANNOTATION_PATH}/members/{member}/preservation.json"

        push_json_to_s3(
            s3=s3,
            json_obj=new_annotation,
            bucket=ANNOTATION_BUCKET,
            path=key,
        )

        logging.info(f"Renamed keys for {member} in {key}")


def rescore_all(members=None, limit=0):
    import boto3
    from rich.progress import track

    s3client = boto3.client("s3")
    session = boto3.Session()
    s3 = session.resource("s3")

    if not members:
        # get member list from S3
        members = get_members(
            s3client=s3client,
            samples_bucket=SAMPLES_BUCKET,
            samples_path=SAMPLES_PATH,
        )

    if limit > 0:
        members = members[:limit]

    from joblib import Parallel, delayed

    results = Parallel(n_jobs=PARALLEL_JOBS)(
        delayed(rescore_member)(
            ANNOTATION_BUCKET,
            ANNOTATION_FILENAME,
            ANNOTATION_PATH,
            SAMPLES_BUCKET,
            SAMPLES_PATH,
            member_id,
            CODE_BUCKET,
        )
        for member_id in track(members)
    )


def get_annotation(
    s3client,
    member_id,
    annotations_bucket,
    annotations_path,
    annotation_name,
    path="members",
    use_member_id=True,
):
    if s3client is None:
        s3client = boto3.client("s3")

    if use_member_id:
        key = f"{annotations_path}/{path}/{member_id}/{annotation_name}"
    else:
        key = f"{annotations_path}/{path}/{annotation_name}"

    data = (
        s3client.get_object(Bucket=annotations_bucket, Key=key)["Body"]
        .read()
        .decode("utf-8")
    )

    from io import StringIO
    import json

    with StringIO(data) as json_file:
        output = json.loads(json_file.read())

        return output
