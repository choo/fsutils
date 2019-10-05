from unittest import TestCase
import os
import fsutils

CUR_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CUR_DIR, 'data/json')

TEST_LINES_DATA = [
    'foo',
    'foo\tbar',
    'foo\tbar  foo bar'
]
TEST_CSV_DATA = [
    {'a': 1, 'b': 'b',                               'k': 'foofoo'},
    {'a': 3, 'b': 'b',  'c': 'c',                    'k': 'foobar'},
    {'a': 2, 'b': 'bb', 'c': 'cc', 'd': None,        'k': 'bar'}
]
TEST_CSV_EXPECTED = [
    {'a': '1', 'b': 'b',                             'k': 'foofoo'},
    {'a': '3', 'b': 'b',  'c': 'c',                  'k': 'foobar'},
    {'a': '2', 'b': 'bb', 'c': 'cc',                 'k': 'bar'}
]
TEST_DATA = [
    {'a': 1, 'b': 'b',  'h': {'h_a': 'a'},           'k': 'foofoo'},
    {'a': 3, 'b': 'b',  'h': {'h_b': 'a'}, 'c': 'c', 'k': 'foobar'},
    {'a': 2, 'b': 'bb', 'c': 'cc', 'd': None,        'k': 'bar'}
]


class TestFsUtils(TestCase):

    def test_list_files(self):
        filepaths = fsutils.list_files(DATA_DIR)
        self.assertEqual(len(filepaths), 4)

        filepaths = fsutils.list_files(DATA_DIR, 'txt')
        self.assertEqual(len(filepaths), 1)

        filepaths = fsutils.list_files(DATA_DIR, 'piyo')
        self.assertEqual(len(filepaths), 0)

        filepaths = fsutils.list_files(DATA_DIR, 'json')
        self.assertEqual(len(filepaths), 3)

        filepaths = fsutils.list_files(DATA_DIR, 'a')
        self.assertEqual(len(filepaths), 0)

        recursively = True
        filepaths = fsutils.list_files(DATA_DIR, 'json', recursively)
        self.assertEqual(len(filepaths), 4)


    def test_read_and_write_lines(self):
        testfilepath = os.path.join(CUR_DIR, 'test.txt')
        fsutils.write_lines(TEST_LINES_DATA, testfilepath)
        content = fsutils.read_lines(testfilepath)
        self.assertEqual(TEST_LINES_DATA, content)
        os.remove(testfilepath)


    def test_read_and_write_csv(self):
        testfilepath = os.path.join(CUR_DIR, 'test.tsv')
        fsutils.write_csv(TEST_CSV_DATA, testfilepath)
        content = fsutils.read_csv(testfilepath)
        self.assertEqual(TEST_CSV_EXPECTED, content)
        os.remove(testfilepath)


    def test_read_json(self):
        filepath = os.path.join(DATA_DIR, 'a.json')
        content  = fsutils.read_json(filepath)
        expected = {
            "a" : "a_a",
            "b" : "a_b",
            "c" : {
                "c_a" : "a_c_a",
                "c_b" : "a_c_b"
            }
        }
        self.assertEqual(content, expected)
