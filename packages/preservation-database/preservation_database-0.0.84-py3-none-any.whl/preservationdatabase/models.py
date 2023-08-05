import csv
import logging
import re
import sys
import tempfile
import datetime
from datetime import datetime as dt
from io import StringIO
from pathlib import Path
from time import sleep

import pytz
from django.db import models, transaction

from preservationdatabase import utils

LIMIT_TIME_DELTA = datetime.timedelta(weeks=3)


class LastFill(models.Model):
    class Meta:
        db_table = "preservationData_lastfill"
        app_label = "preservationdatabase"

    archive_name = models.CharField(max_length=255)
    last_fill_date = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def set_last_fill(archive_name, last_fill_date=dt.now(pytz.utc)):
        lf, created = LastFill.objects.get_or_create(archive_name=archive_name)
        lf.last_fill_date = last_fill_date
        lf.save()

    @staticmethod
    def clear():
        LastFill.objects.all().delete()

    @staticmethod
    def get_last_fill(archive_name):
        try:
            return LastFill.objects.get(
                archive_name=archive_name
            ).last_fill_date
        except LastFill.DoesNotExist:
            return None

    def cache_valid(self) -> bool:
        time_delta = datetime.datetime.now(pytz.utc) - self.last_fill_date

        return True if LIMIT_TIME_DELTA > time_delta else False

    @staticmethod
    def will_cache(archive_name) -> bool:
        try:
            lf = LastFill.objects.get(archive_name=archive_name)
            return lf.cache_valid()
        except LastFill.DoesNotExist:
            return False

    def __str__(self):
        return "{}: {}".format(self.archive_name, self.last_fill_date)


class Publisher(models.Model):
    class Meta:
        db_table = "preservationData_publisher"
        app_label = "preservationdatabase"

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class LockssPreservation(models.Model):
    class Meta:
        db_table = "preservationData_locksspreservation"

        indexes = [
            models.Index(fields=["issn"]),
            models.Index(fields=["eissn"]),
            models.Index(fields=["title"]),
        ]

    title = models.TextField()
    issn = models.CharField(max_length=20)
    eissn = models.CharField(max_length=20)
    preserved_volumes = models.TextField()
    preserved_years = models.TextField()
    in_progress_volumes = models.TextField()
    in_progress_years = models.TextField()
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, default=None
    )

    def __str__(self):
        return (
            "{} (issn: {}) (eissn: {}) (v{}({})) "
            "(in progress: {} ({})) ".format(
                self.title,
                self.issn,
                self.eissn,
                self.preserved_volumes,
                self.preserved_years,
                self.in_progress_volumes,
                self.in_progress_years,
            )
        )

    @staticmethod
    def name() -> str:
        return "LOCKSS"

    @staticmethod
    def preservation(
        container_title: str,
        issn: str,
        volume: str,
        no=None,
        year=None,
        doi=None,
    ):
        """
        Determine whether a DOI is preserved in LOCKSS
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :param year: the year
        :param doi: a DOI
        :return: A LockssPreservation item (or None) and a bool indicating
        whether the item is fully preserved
        """
        return utils.preservation_status(
            LockssPreservation, container_title, issn, volume, no=no
        )

    @staticmethod
    def create_preservation(
        issn,
        eissn,
        title,
        preserved_volumes,
        preserved_years,
        in_progress_volumes,
        in_progress_years,
        publisher,
        model,
    ) -> None:
        """
        Create a preservation item of this model
        :param issn: the ISSN
        :param eissn: the eISSN
        :param title: the title
        :param preserved_volumes: the preserved volumes
        :param preserved_years: the preserved years
        :param in_progress_volumes: the in-progress volumes
        :param in_progress_years: the in-progress years
        :param publisher: the publisher object
        :param model: the model on which to operate
        :return: None
        """
        model.objects.create(
            issn=issn,
            eissn=eissn,
            title=title,
            preserved_volumes=preserved_volumes,
            preserved_years=preserved_years,
            in_progress_volumes=in_progress_volumes,
            in_progress_years=in_progress_years,
            publisher=publisher,
        )

    @staticmethod
    @transaction.atomic
    def import_data(url: str = None, local: bool = False) -> None:
        """
        Import data into the system
        :param url: the URL of the data file
        :param local: whether the data file is local
        :return: None
        """
        utils.generic_lockss_import(
            url, LockssPreservation, local=local, skip_first_line=True
        )


class CarinianaPreservation(models.Model):
    class Meta:
        db_table = "preservationData_carinianapreservation"

        indexes = [
            models.Index(fields=["issn"]),
            models.Index(fields=["eissn"]),
            models.Index(fields=["title"]),
        ]

    title = models.TextField()
    issn = models.CharField(max_length=20)
    eissn = models.CharField(max_length=20)
    preserved_volumes = models.TextField()
    preserved_years = models.TextField()
    in_progress_volumes = models.TextField()
    in_progress_years = models.TextField()
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, default=None
    )

    def __str__(self):
        return (
            "{} (issn: {}) (eissn: {}) (v{}({})) "
            "(in progress: {} ({})) ".format(
                self.title,
                self.issn,
                self.eissn,
                self.preserved_volumes,
                self.preserved_years,
                self.in_progress_volumes,
                self.in_progress_years,
            )
        )

    @staticmethod
    def name() -> str:
        return "Cariniana"

    @staticmethod
    def preservation(
        container_title: str,
        issn: str,
        volume: str,
        no=None,
        year=None,
        doi=None,
    ):
        """
        Determine whether a DOI is preserved in Cariniana
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :param year: the year
        :param doi: a DOI
        :return: A Cariniana item (or None) and a bool indicating
        whether the item is fully preserved
        """
        return utils.preservation_status(
            CarinianaPreservation, container_title, issn, volume, no=no
        )

    @staticmethod
    def create_preservation(
        issn,
        eissn,
        title,
        preserved_volumes,
        preserved_years,
        in_progress_volumes,
        in_progress_years,
        publisher,
        model,
    ) -> None:
        """
        Create a preservation item of this model
        :param issn: the ISSN
        :param eissn: the eISSN
        :param title: the title
        :param preserved_volumes: the preserved volumes
        :param preserved_years: the preserved years
        :param in_progress_volumes: the in-progress volumes
        :param in_progress_years: the in-progress years
        :param publisher: the publisher object
        :param model: the model on which to operate
        :return: None
        """
        model.objects.create(
            issn=issn,
            eissn=eissn,
            title=title,
            preserved_volumes=preserved_volumes,
            preserved_years=preserved_years,
            in_progress_volumes=in_progress_volumes,
            in_progress_years=in_progress_years,
            publisher=publisher,
        )

    @staticmethod
    @transaction.atomic
    def import_data(url: str = None, local: bool = False) -> None:
        """
        Import data into the system
        :param url: the URL of the data file
        :param local: whether the data file is local
        :return: None
        """
        utils.generic_lockss_import(
            url, CarinianaPreservation, local=local, skip_first_line=True
        )


class ClockssPreservation(models.Model):
    class Meta:
        db_table = "preservationData_clocksspreservation"

        indexes = [
            models.Index(fields=["issn"]),
            models.Index(fields=["eissn"]),
            models.Index(fields=["title"]),
        ]

    title = models.TextField()
    issn = models.CharField(max_length=20)
    eissn = models.CharField(max_length=20)
    preserved_volumes = models.TextField()
    preserved_years = models.TextField()
    in_progress_volumes = models.TextField()
    in_progress_years = models.TextField()
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, default=None
    )

    def __str__(self):
        return (
            "{} (issn: {}) (eissn: {}) (v{}({})) "
            "(in progress: {} ({})) ".format(
                self.title,
                self.issn,
                self.eissn,
                self.preserved_volumes,
                self.preserved_years,
                self.in_progress_volumes,
                self.in_progress_years,
            )
        )

    @staticmethod
    def name() -> str:
        return "CLOCKSS"

    @staticmethod
    def preservation(
        container_title: str,
        issn: str,
        volume: str,
        no=None,
        year=None,
        doi=None,
    ):
        """
        Determine whether a DOI is preserved in CLOCKSS
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :param year: the year
        :param doi: a DOI
        :return: A ClockssPreservation item (or None) and a bool indicating
        whether the item is fully preserved
        """
        return utils.preservation_status(
            ClockssPreservation, container_title, issn, volume, no=no
        )

    @staticmethod
    def create_preservation(
        issn,
        eissn,
        title,
        preserved_volumes,
        preserved_years,
        in_progress_volumes,
        in_progress_years,
        publisher,
        model,
    ) -> None:
        """
        Create a preservation item of this model
        :param issn: the ISSN
        :param eissn: the eISSN
        :param title: the title
        :param preserved_volumes: the preserved volumes
        :param preserved_years: the preserved years
        :param in_progress_volumes: the in-progress volumes
        :param in_progress_years: the in-progress years
        :param publisher: the publisher object
        :param model: the model on which to operate
        :return: None
        """
        model.objects.create(
            issn=issn,
            eissn=eissn,
            title=title,
            preserved_volumes=preserved_volumes,
            preserved_years=preserved_years,
            in_progress_volumes=in_progress_volumes,
            in_progress_years=in_progress_years,
            publisher=publisher,
        )

    @staticmethod
    @transaction.atomic
    def import_data(url: str = None, local: bool = False) -> None:
        """
        Import data into the system
        :param url: the URL of the data file
        :param local: whether the data file is local
        :return: None
        """
        utils.generic_lockss_import(
            url, ClockssPreservation, local=local, skip_first_line=True
        )


class PKPPreservation(models.Model):
    class Meta:
        db_table = "preservationData_pkppreservation"

        indexes = [
            models.Index(fields=["issn"]),
            models.Index(fields=["title"]),
        ]

    title = models.TextField()
    issn = models.CharField(max_length=20)
    preserved_volumes = models.TextField()
    preserved_no = models.TextField(blank=True, null=True)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, default=None
    )

    def __str__(self):
        return "{} (issn: {}) (v{}({})) ".format(
            self.title,
            self.issn,
            self.preserved_volumes,
            self.preserved_no,
        )

    @staticmethod
    def name() -> str:
        return "PKP PLN"

    @staticmethod
    def preservation(container_title, issn, volume, no, year=None, doi=None):
        """
        Determine whether a DOI is preserved in the PKP private LOCKSS network
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :param year: the year
        :param doi: a DOI
        :return: A PKPPreservation item (or None) and a bool indicating
        whether the item is fully preserved
        """
        preserved_item = utils.get_preserved_item_record(
            PKPPreservation, container_title, issn
        )

        if not preserved_item or len(preserved_item) == 0:
            return None, False

        if no is not None and no != "" and no != "0":
            preserved_item.filter(preserved_no=no)

            if len(preserved_item) == 0:
                return None, False

        return preserved_item, True

    @staticmethod
    @transaction.atomic
    def import_data(url: str = None, local: bool = False) -> None:
        """
        Import data into the system
        :param url: the URL of the data file
        :param local: whether the data file is local
        :return: None
        """
        utils.generic_lockss_import(
            url, PKPPreservation, local=local, skip_first_line=True
        )

    @staticmethod
    def create_preservation(
        issn, title, preserved_volumes, preserved_no, publisher, model
    ) -> None:
        """
        Create a preservation item of this model
        :param issn: the ISSN
        :param title: the title
        :param preserved_volumes: the preserved volumes
        :param publisher: the publisher object
        :param model: the model on which to operate
        :return: None
        """
        model.objects.create(
            issn=issn,
            title=title,
            preserved_volumes=preserved_volumes,
            preserved_no=preserved_no,
            publisher=publisher,
        )


class HathiPreservation(models.Model):
    class Meta:
        db_table = "preservationData_hathipreservation"

        indexes = [
            models.Index(fields=["issn"]),
            models.Index(fields=["title"]),
        ]

    title = models.TextField()
    issn = models.CharField(max_length=20)
    preserved_volumes = models.TextField()

    def __str__(self):
        return "{} (issn: {}) (v{}) ".format(
            self.title, self.issn, self.preserved_volumes
        )

    @staticmethod
    def name() -> str:
        return "HathiTrust"

    @staticmethod
    def preservation(
        container_title, issn, volume, no=None, year=None, doi=None
    ):
        """
        Determine whether a DOI is preserved in HathiTrust
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :param year: the year
        :param doi: a DOI
        :return: A HathiPreservation item (or None) and a bool indicating
        whether the item is fully preserved
        """
        preserved_item = utils.get_preserved_item_record(
            HathiPreservation, container_title, issn
        )

        if not preserved_item or len(preserved_item) == 0:
            return None, False

        if preserved_item:
            # HathiTrust records volume strings as "v[1, 2]" etc
            # but also as "v1999" etc.

            if year:
                volume_year_regex = re.compile(rf"v{year}")
                volume_year_regex_two = re.compile(rf"{year}")

                for pi in preserved_item:
                    matches = re.findall(
                        volume_year_regex, pi.preserved_volumes
                    )

                    if matches:
                        return pi, True

                    matches = re.findall(
                        volume_year_regex_two, pi.preserved_volumes
                    )

                    if matches:
                        return pi, True

            volume_regex = r"(\d+),?"

            volume = str(volume)

            for pi in preserved_item:
                matches = re.finditer(
                    volume_regex, pi.preserved_volumes, re.MULTILINE
                )

                for matchNum, match in enumerate(matches, start=1):
                    for groupNum in range(0, len(match.groups())):
                        groupNum = groupNum + 1

                        group = match.group(groupNum)

                        if group == volume:
                            return pi, True

            return None, False

        else:
            return None, False

    @staticmethod
    @transaction.atomic
    def import_data(url, bucket="", s3client=None, local=False):
        # download the data file from S3 bucket
        with tempfile.TemporaryDirectory() as tmp:
            if local:
                path = url
            else:
                path = Path(tmp) / "downloaded.file"

                hathi_data = utils.download_remote(
                    False,
                    HathiPreservation,
                    url,
                    bucket=bucket,
                    s3client=s3client,
                    decode=False,
                    file=True,
                    filename=str(path),
                )

            # clear out existing data
            utils.clear_out(HathiPreservation)

            csv.field_size_limit(sys.maxsize)

            with open(str(path), "r") as input_file:
                csv_reader = csv.reader(input_file, delimiter="\t")

                volume_matcher = r"v\.\s?(\d+(?:\-?\d+)?)"
                no_matcher = r"no\.\s?(\d+(?:\-?\d+)?)"
                year_matcher = r"\d{4}"
                issn_matcher = r"[0-9][0-9][0-9][0-9][-][0-9][0-9][0-9][X0-9]"

                for row in csv_reader:
                    try:
                        vols = row[4]
                        issn = row[9]
                        issns = []
                        title = row[11]
                        publishing_info = row[12]
                        date = row[16]
                        bf = row[19]
                        unknown_format = False

                        # check if it's an ISSN
                        # logging.info('ISSN: {}'.format(issn))

                        # Sometimes we have formats like this for ISSN:
                        # 1938-1603 (online),0022-1864
                        issn_matches = re.findall(issn_matcher, issn)

                        if issn_matches:
                            for match in issn_matches:
                                issns.append(match)

                        # if it's a serial, try to parse the vols
                        if bf == "SE" and len(issns) > 0 and vols:
                            matches = re.findall(volume_matcher, vols)

                            if matches:
                                for match in matches:
                                    vols = utils.unpack_range(match)
                            else:
                                matches = re.findall(no_matcher, vols)

                                if matches:
                                    for match in matches:
                                        vols = utils.unpack_range(match)
                                else:
                                    matches = re.findall(year_matcher, vols)

                                    if matches:
                                        for match in matches:
                                            vols = match
                                    else:
                                        unknown_format = True

                            if not unknown_format:
                                if title.endswith("."):
                                    title = title[:-1]

                                for issn_no in issns:
                                    HathiPreservation.objects.create(
                                        issn=issn_no,
                                        title=title,
                                        preserved_volumes=vols,
                                    )

                                logging.info(
                                    f"Added {title} (issns {issns}) to "
                                    f"{HathiPreservation.name()} data"
                                )
                    except IndexError:
                        pass


class PorticoPreservation(models.Model):
    class Meta:
        db_table = "preservationData_porticopreservation"

        indexes = [
            models.Index(fields=["issn"]),
            models.Index(fields=["eissn"]),
            models.Index(fields=["title"]),
        ]

    title = models.TextField()
    issn = models.CharField(max_length=20)
    eissn = models.CharField(max_length=20)
    preserved_volumes = models.TextField()

    # this indicates whether the title is preserved or queued
    preserved = models.BooleanField()
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, default=None
    )

    def __str__(self):
        return "{} (issn: {}) (eissn: {}) (v{}) ".format(
            self.title, self.issn, self.eissn, self.preserved_volumes
        )

    @staticmethod
    def name():
        return "Portico"

    @staticmethod
    def preservation(
        container_title, issn, volume, no=None, year=None, doi=None
    ):
        """
        Determine whether a DOI is preserved in Portico
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :param year: the year
        :param doi: a DOI
        :return: A PorticoPreservation item (or None) and a bool indicating
        whether the item is fully preserved
        """
        preserved_item = utils.get_preserved_item_record(
            PorticoPreservation, container_title, issn
        )

        if not preserved_item or len(preserved_item) == 0:
            return None, False

        # Portico gives volume formats as follows:
        # 2013/2014 - v. 2 (1-2)
        volume_regex = r"v\.\s(\d+)"

        for pi in preserved_item:
            matches = re.findall(volume_regex, pi.preserved_volumes)

            volume = str(volume)

            if volume in matches:
                return pi, pi.preserved

        return None, False

    @staticmethod
    @transaction.atomic
    def import_data(url: str = None, local: bool = False) -> None:
        """
        Import data into the system
        :param url: the URL of the data file
        :param local: whether the data file is local
        :return: None
        """
        # get CSV data
        csv_file = utils.download_remote(local, PorticoPreservation, url)

        # clear out
        utils.clear_out(PorticoPreservation)

        # increase the CSV field size to accommodate large entries
        csv.field_size_limit(sys.maxsize)

        with StringIO(csv_file) as input_file:
            csv_reader = csv.DictReader(
                input_file, delimiter="\t", quoting=csv.QUOTE_NONE
            )

            for row in csv_reader:
                publisher, created = Publisher.objects.get_or_create(
                    name=row["publisher_name"]
                )

                PorticoPreservation.objects.create(
                    issn=row["print_identifier"],
                    eissn=row["online_identifier"],
                    title=row["publication_title"],
                    preserved_volumes=row["holding_list"],
                    preserved=(row["notes"] == "Preserved"),
                    publisher=publisher,
                )

                logging.info(
                    f'Added {row["publication_title"]} to '
                    f"{PorticoPreservation.name()} data"
                )


class OculScholarsPortalPreservation(models.Model):
    class Meta:
        db_table = "preservationData_oculpreservation"

        indexes = [
            models.Index(fields=["issn"]),
            models.Index(fields=["title"]),
        ]

    title = models.TextField()

    """
    ONIX field codes to identify an ISSN:
    ResourceVersionIDType = 7
    IDValue = unhyphenated ISSN
    
    e.g.
    <oph:ResourceVersion>
        <oph:ResourceVersionIdentifier>
        <oph:ResourceVersionIDType>07</oph:ResourceVersionIDType>
        <oph:IDValue> 27697541</oph:IDValue>
    </oph:ResourceVersionIdentifier>
    """
    issn = models.CharField(max_length=20)
    preserved_volumes = models.TextField()
    preserved_no = models.TextField()

    # this indicates whether the title is preserved or queued
    """
    ONIX field codes for the <oph:PreservationStatus><oph:PreservationStatusCode> tags:
    00	Unknown	The preservation status is genuinely unknown, and should be updated as soon as information is available	5		
    01	Will not be preserved	Preservation agency has decided against preservation of the issues and e-content in the <Coverage> statement	5		
    02	Undecided	Preservation agency is considering preservation of the issues and e-content in the <Coverage> statement. No decision has yet been made. This status should be updated as soon as information is available	5		
    03	Committed	Preservation agency is committed to preserving the issues and e-content in the <Coverage> statement. No active steps have yet been taken	5		
    04	In progress	Preservation agency is in the process of preserving the issues and e-content in the <Coverage> statement	5		
    05	Preserved	Preservation agency has preserved the issues and e-content in the <Coverage> statement	5
    """
    preserved = models.IntegerField()

    """
    ONIX field codes for the <oph:VerificationStatus> tag:
    00	Unknown	It is genuinely unknown whether the preservation agency has checked the preserved holdings in the <Coverage> statement. This status should be updated when information is available		
    01	Unverified	Preservation agency has not checked the preserved holdings in the <Coverage> statement, and it is not known whether all issues or e-content items are preserved
    02	Verification in progress	Preservation agency is in the process of checking the preserved holdings in the <Coverage> statement, and nothing can be said about completeness at this stage		
    03	Verified and incomplete	Preservation agency has checked the preserved holdings in the <Coverage> statement, and some issues or e-content items intended to be preserved are not complete		
    04	Verified and complete	Preservation agency has checked the preserved holdings in the <Coverage> statement, and all issues or e-content items intended to be preserved are complete
    """
    verified = models.IntegerField()

    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, default=None
    )

    def __str__(self):
        return "{} (issn: {}) (v{}({})) ".format(
            self.title, self.issn, self.preserved_volumes, self.preserved_no
        )

    @staticmethod
    def name():
        return "OCUL Scholars Portal"

    @staticmethod
    def preservation(
        container_title, issn, volume, no=None, year=None, doi=None
    ):
        """
        Determine whether a DOI is preserved in OCUL Scholars Portal
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :param year: the year
        :param doi: a DOI
        :return: An OculScholarsPortalPreservation item (or None) and a bool
        indicating whether the item is fully preserved
        """
        preserved_item = utils.get_preserved_item_record(
            OculScholarsPortalPreservation, container_title, issn
        )

        if not preserved_item or len(preserved_item) == 0:
            return None, False

        # direct hit
        pis = preserved_item.filter(preserved_volumes=volume)

        volume = str(volume)

        if len(pis) > 0:
            return pis[0], pis[0].preserved
        else:
            # do a broader search that allows for the following volume formats:
            # v24(1)
            # 1, 2, 3-4, 3.4
            # 1 to 4
            basic_volume_regex = r"v(\d+)"
            unpack_volume_regex = r"(\d+\-\d+)"
            unpack_volume_words_regex = r"(\d+ to \d+)"

            pis = preserved_item.filter(
                preserved_volumes__iregex=basic_volume_regex
            )

            if len(pis) > 0:
                for pi in pis:
                    matches = re.findall(
                        basic_volume_regex, pi.preserved_volumes
                    )

                    if volume in matches:
                        return pi, pi.preserved

            pis = preserved_item.filter(
                preserved_volumes__iregex=unpack_volume_regex
            )

            if len(pis) > 0:
                for pi in pis:
                    matches = re.findall(
                        unpack_volume_regex, pi.preserved_volumes
                    )

                    for match in matches:
                        unpacked_range = utils.unpack_range(match)

                        if volume in unpacked_range:
                            return pi, pi.preserved

            pis = preserved_item.filter(preserved_volumes=volume)
            return None, False

    @staticmethod
    def import_data(url, bucket="", s3client=None):
        # download the data file from S3 bucket
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "downloaded.file"

            xml_file = utils.download_remote(
                False,
                OculScholarsPortalPreservation,
                url,
                bucket=bucket,
                s3client=s3client,
                decode=False,
                file=True,
                filename=str(path),
            )

            # local file for testing
            # xml_file = '/home/martin/scholars_portal_keepers_20230202.xml'

            # clear out
            utils.clear_out(OculScholarsPortalPreservation)

            fields = [
                "oph:ResourceVersionIDType",
                "oph:IDValue",
                "oph:FixedCoverage",
                "oph:PreservationStatusCode",
                "oph:VerificationStatus",
            ]

            xml_parsed = utils.process_onix(
                xml_file,
                fields,
                callback=OculScholarsPortalPreservation.create_preservation,
            )

    @staticmethod
    def create_preservation(output) -> None:
        """
        Create a preservation item of this model
        :param output: a dictionary from an ONIX import
        :return: None
        """

        if "status" not in output or output["status"] is None:
            status = 0
        else:
            status = output["status"]

        if "verified" not in output or output["verified"] is None:
            verified = 0
        else:
            verified = output["verified"]

        if "publisher" not in output or output["publisher"] is None:
            publisher = "Default"
        else:
            publisher = output["publisher"]

        if "title" not in output or output["title"] is None:
            title = "Unknown title"
        else:
            title = output["title"]

        publisher, created = Publisher.objects.get_or_create(name=publisher)

        volumes = output["volumes"]
        issues = output["issues"]

        for volume, issue in zip(volumes, issues):
            volume = volume if volume is not None else ""
            issue = issue if issue is not None else ""

            OculScholarsPortalPreservation.objects.create(
                issn=output["issn"],
                title=title,
                preserved_volumes=volume,
                preserved_no=issue,
                preserved=status,
                verified=verified,
                publisher=publisher,
            )

        logging.info(
            f"Added {title} to " f"{OculScholarsPortalPreservation.name()} data"
        )


class ISSNL(models.Model):
    class Meta:
        db_table = "preservationData_issnl"

        indexes = [
            models.Index(fields=["identifier"]),
        ]

    identifier = models.CharField(max_length=255)


class ISSN(models.Model):
    class Meta:
        db_table = "preservationData_issn"

        indexes = [
            models.Index(fields=["identifier"]),
        ]

    identifier = models.CharField(max_length=255)
    issnl = models.ForeignKey(ISSNL, on_delete=models.CASCADE, default=None)


class InternetArchivePreservation(models.Model):
    class Meta:
        db_table = "preservationData_iapreservation"

        indexes = [
            models.Index(fields=["issn"]),
            models.Index(fields=["eissn"]),
            models.Index(fields=["title"]),
        ]

    title = models.TextField()
    issn = models.CharField(max_length=20)
    eissn = models.CharField(max_length=20)
    preserved_volumes = models.TextField()

    # this indicates whether the title is preserved or queued
    preserved = models.BooleanField()
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, default=None
    )

    def __str__(self):
        return "{} (issn: {}) (eissn: {}) (v{}) ".format(
            self.title, self.issn, self.eissn, self.preserved_volumes
        )

    @staticmethod
    def name():
        return "Internet Archive"

    @staticmethod
    def preservation(
        container_title, issn, volume, no=None, year=None, doi=None
    ):
        """
        Determine whether a DOI is preserved in the Internet Archive
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :param year: the year
        :param doi: a DOI
        :return: An InternetArchivePreservation item (or None) and a bool
        indicating whether the item is fully preserved
        """
        preserved_item = utils.get_preserved_item_record(
            InternetArchivePreservation, container_title, issn
        )

        if not preserved_item or len(preserved_item) == 0:
            return None, False

        # We add a single IA entry per volume
        pi = preserved_item.filter(preserved_volumes=str(volume))

        if pi.count() > 0:
            return pi[0], True

        return None, False

    @staticmethod
    @transaction.atomic
    def import_data(url, bucket="", s3client=None, local=False):
        # download the data file from S3 bucket
        with tempfile.TemporaryDirectory() as tmp:
            if local:
                path = url
            else:
                path = Path(tmp) / "downloaded.file"

                ia_data = utils.download_remote(
                    False,
                    InternetArchivePreservation,
                    url,
                    bucket=bucket,
                    s3client=s3client,
                    decode=False,
                    file=True,
                    filename=str(path),
                )

            # clear out existing data
            utils.clear_out(InternetArchivePreservation)

            csv.field_size_limit(sys.maxsize)

            with open(str(path), "r") as input_file:
                csv_reader = csv.DictReader(input_file, delimiter="\t")

                for row in csv_reader:
                    publisher, created = Publisher.objects.get_or_create(
                        name=row["publisher_name"]
                    )

                    # we have to calculate the held volumes
                    first_vol = row["num_first_vol_online"]
                    last_vol = row["num_last_vol_online"]

                    if first_vol != "":
                        try:
                            first_vol = int(first_vol)
                        except ValueError:
                            first_vol = None

                    if last_vol != "":
                        try:
                            last_vol = int(last_vol)
                        except ValueError:
                            last_vol = None

                    volumes = []

                    if first_vol and last_vol is None:
                        # if no last volume, assume single volume
                        volumes.append(first_vol)
                    elif last_vol and first_vol is None:
                        # if no first volume, assume single volume
                        volumes.append(last_vol)
                    elif first_vol and last_vol:
                        # if there's a first and last volume
                        volumes.extend(range(first_vol, last_vol))

                    volumes = set(volumes)

                    for vol in volumes:
                        InternetArchivePreservation.objects.create(
                            issn=row["print_identifier"],
                            eissn=row["online_identifier"],
                            title=row["publication_title"],
                            preserved_volumes=str(vol),
                            preserved=True,
                            publisher=publisher,
                        )

                    logging.info(
                        f'Added {row["publication_title"]} to '
                        f"{InternetArchivePreservation.name()} data "
                        f"({len(volumes)} volumes)"
                    )


class InternetArchiveItem(models.Model):
    class Meta:
        db_table = "preservationData_iaitems"

        indexes = [
            models.Index(fields=["doi"]),
            models.Index(fields=["fatcat_ident"]),
        ]

    doi = models.TextField()
    url = models.TextField()
    fatcat_ident = models.TextField()

    def __str__(self):
        return "{} (url: {}) (fatcat: {})".format(
            self.doi, self.url, self.fatcat_ident
        )

    @staticmethod
    def name():
        return "Internet Archive Scholar (item-level data)"

    @staticmethod
    def import_data(file: str) -> None:
        """Imports data from an Internet Archive file. Updates are propagated
        in batches of 1000.

        :param file: the file to import from
        :return None
        """
        from rich.progress import track
        from rich.progress import Progress

        from msgspec.json import decode
        from msgspec import Struct
        from typing import Optional

        class URL(Struct):
            url: str
            rel: str

        class Files(Struct):
            urls: list[URL]

        class Identifier(Struct):
            doi: Optional[str] = None

        class IAItem(Struct):
            ident: str
            ext_ids: Identifier
            files: list[Files]

        file_size = Path(file).stat().st_size

        with Progress() as progress:
            with open(file, "rb") as f:
                task = progress.add_task("[red]Importing...", total=file_size)

                count = 0
                sample_count = 0
                batch_objects = []

                utils.clear_out(InternetArchiveItem)

                for json_data in f:
                    data = decode(json_data, type=IAItem)

                    list_comp = [
                        (data, x)
                        for file in data.files
                        for x in file.urls
                        if x.rel == "webarchive"
                        and data.ext_ids.doi is not None
                    ]

                    progress.update(task, advance=len(json_data))

                    for outcome, url in list_comp:
                        batch_objects.append(
                            InternetArchiveItem(
                                doi=outcome.ext_ids.doi,
                                url=url,
                                fatcat_ident=outcome.ident,
                            )
                        )

                        count += 1

                    # this is just a logging function so we can see
                    # what's going on
                    if sample_count == 100000:
                        progress.console.print(
                            "Buffer contains {} items".format(count)
                        )
                        progress.console.print(f"{data}")
                        sample_count = 0

                    sample_count += 1

                    if count > 1000:
                        InternetArchiveItem.objects.bulk_create(batch_objects)
                        progress.console.print(
                            f"Flushing {len(batch_objects)} items."
                        )
                        count = 0
                        batch_objects = []

                # flush the final objects
                InternetArchiveItem.objects.bulk_create(batch_objects)
                progress.console.print(f"Flushing {len(batch_objects)} items.")

            return

    @staticmethod
    def preservation(
        container_title, issn, volume, no=None, year=None, doi=None
    ):
        """
        Determine whether a DOI is preserved in the Internet Archive
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :param year: the year
        :param doi: a DOI
        :return: An InternetArchiveItem item (or None) and a bool
        indicating whether the item is fully preserved
        """
        try:
            preserved_item = InternetArchiveItem.objects.filter(doi=doi["DOI"])

            if len(preserved_item) > 0:
                return preserved_item[0], True
            else:
                return None, False
        except InternetArchiveItem.DoesNotExist:
            return None, False
