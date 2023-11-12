import pytest

from pypeliner.readers.bulk_readers.file_readers import (
    CSVFileReader,
    FileReader,
)


@pytest.fixture
def file_reader():
    return FileReader(file_path="tests/test_files/file_reader_test_file.txt")


@pytest.fixture
def csv_reader(request):
    return CSVFileReader(**request.param)


def test_file_reader(file_reader):
    assert file_reader.read() == (
        "the quick brown fox jumps over the lazy dog.\n"
    )


@pytest.mark.parametrize(
    ["input_params", "expected_result"],
    [
        [
            {
                "file_path": "tests/test_files/csv_reader_test_file.csv",
                "detect_numbers": False,
            },
            {
                "column a": ["1", "a", "11", "trans", "dddddd"],
                "column b": ["2", "c", "d", "late", "ddddd"],
                "column c": ["3", "n", "dd", "da", "dddd"],
                "column d": ["4", "k", "14", "ting", "ddd"],
                "column e": ["5", "d", "fff", "fast", "d"],
            },
        ],
        [
            {
                "file_path": "tests/test_files/csv_reader_test_file.csv",
                "load_titles_row": True,
                "detect_numbers": True,
            },
            {
                "column a": [1, "a", 11, "trans", "dddddd"],
                "column b": [2, "c", "d", "late", "ddddd"],
                "column c": [3, "n", "dd", "da", "dddd"],
                "column d": [4, "k", 14, "ting", "ddd"],
                "column e": [5, "d", "fff", "fast", "d"],
            },
        ],
        [
            {
                "file_path": "tests/test_files/csv_reader_test_file.csv",
                "load_titles_row": True,
                "detect_numbers": True,
                "columns_names": ["a", "b", "c", "d", "e"],
            },
            {
                "a": [1, "a", 11, "trans", "dddddd"],
                "b": [2, "c", "d", "late", "ddddd"],
                "c": [3, "n", "dd", "da", "dddd"],
                "d": [4, "k", 14, "ting", "ddd"],
                "e": [5, "d", "fff", "fast", "d"],
            },
        ],
        [
            {
                "file_path": "tests/test_files/csv_reader_test_file.csv",
                "load_titles_row": False,
                "detect_numbers": True,
                "columns_names": ["a", "b", "c", "d", "e"],
            },
            {
                "a": ["column a", 1, "a", 11, "trans", "dddddd"],
                "b": ["column b", 2, "c", "d", "late", "ddddd"],
                "c": ["column c", 3, "n", "dd", "da", "dddd"],
                "d": ["column d", 4, "k", 14, "ting", "ddd"],
                "e": ["column e", 5, "d", "fff", "fast", "d"],
            },
        ],
        [
            {
                "file_path": "tests/"
                "test_files/"
                "csv_reader_test_file_semicolon_delimiter.csv",
                "load_titles_row": False,
                "detect_numbers": True,
                "delimiter": ";",
                "columns_names": ["a", "b", "c", "d", "e"],
            },
            {
                "a": ["column a", 1, "a", 11, "trans", "dddddd"],
                "b": ["column b", 2, "c", "d", "late", "ddddd"],
                "c": ["column c", 3, "n", "dd", "da", "dddd"],
                "d": ["column d", 4, "k", 14, "ting", "ddd"],
                "e": ["column e", 5, "d", "fff", "fast", "d"],
            },
        ],
    ],
)
def test_csv_reader(input_params, expected_result):
    # noinspection PyArgumentList
    reader = CSVFileReader(**input_params)
    assert reader.read() == expected_result
