import json
import pathlib
import unittest
import logging
from preservationdatabase import constants, utils

logger = logging.getLogger(__name__)
logging.disable(logging.NOTSET)
logger.setLevel(logging.DEBUG)


class ArchiveTestCase(unittest.TestCase):
    """
    Tests for archival presences and absences using known good data
    """
    def test(self):
        test_file = \
            pathlib.Path(
                pathlib.Path(__file__).resolve().parent.parent / 'test_data'
                / 'tests.jsonl')
        logging.debug(f'Loading tests from {test_file}')

        with open(test_file, 'r') as json_file:
            json_list = list(json_file)

        for json_str in json_list:
            result = json.loads(json_str)

            # resolve archive object
            archive = result['archive']
            archive_object = constants.archives[archive]
            doi = result['doi']
            should_be_present = result['present']

            preservation_status, doi = \
                utils.show_preservation_for_doi(doi, archive)

            if should_be_present:
                print(f'Testing if {doi["DOI"]} is in {archive}')
                logging.debug(f'Testing if {doi["DOI"]} is in {archive}')

                self.assertTrue(archive_object.name() in preservation_status,
                                msg=f'{doi["DOI"]} is not in {archive}')

                if archive_object.name() in preservation_status:
                    self.assertFalse(
                        preservation_status[
                            archive_object.name()] == (None, False),
                        msg=f'{doi["DOI"]} is not in {archive}')
            else:
                print(f'Testing if {doi["DOI"]} is not in {archive}')
                logging.debug(f'Testing if {doi["DOI"]} is not in {archive}')

                self.assertTrue(
                    archive_object.name() not in preservation_status or
                    preservation_status[archive_object.name()] == (None, False))


if __name__ == '__main__':
    unittest.main()
