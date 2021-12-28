from unittest import TestCase

from pupilComb.s3_utils import does_file_exist

class s3UtilsTestCase(TestCase):

    def test_does_file_exist_True(self):
        if ans := input("does test.mp4 exist in the tests folder in the bucket [y/n]") == 'y':
            self.assertTrue(does_file_exist('tests/test.mp4'))
        elif ans == 'n':
            print('please upload a file with that name and rerun the tests')
            self.assertTrue(False, "File does not exist")
        else:
            self.assertTrue(False, "input is not of accepted format")

    def test_does_file_exist_False(self):
        self.assertFalse(does_file_exist('DNE.mp4'))