import os
import pytest

from src.amarium.checks import (
    check_header_and_data,
    check_make_dir,
    check_make_file_name_suffix,
    check_delete_dir,
)


def test_check_header_and_data():

    header = ["a", "b", "c"]
    data = [1, 2, 3]
    check_header_and_data(data=data, header=header)
    data = [1, 2, 3, 4]
    with pytest.raises(RuntimeError) as run_time_error:
        check_header_and_data(data=data, header=header)

    assert (
        str(run_time_error.value)
        == "Input data and input header do not have the same number of fields. Please ensure an appropriate data structure."
    )

    header = ["a", "b", "c", "d", "e"]

    with pytest.raises(RuntimeError) as run_time_error:
        check_header_and_data(data=data, header=header)
    assert (
        str(run_time_error.value)
        == "Input data and input header do not have the same number of fields. Please ensure an appropriate data structure."
    )


def test_check_make_dir():

    test_dir = "tests/test_utils"
    test_folder = "test_utils"
    check_make_dir(test_dir)
    dirs = os.listdir("tests/")
    assert test_folder in dirs
    check_make_dir(test_dir)
    os.rmdir(test_dir)
    dirs = os.listdir("tests/")
    assert test_folder not in dirs


def test_check_file_name():

    file_name = "test"
    suffix = ".csv"
    res1 = check_make_file_name_suffix(file_name, suffix)
    assert res1 == file_name + suffix

    suffix = "csv"
    res1 = check_make_file_name_suffix(file_name, suffix)
    assert res1 == file_name + "." + suffix

    file_name = "test.csv"
    res1 = check_make_file_name_suffix(file_name)
    assert res1 == file_name


def test_check_delete_dir():

    test_dir = "tests/test_utils"
    test_folder = "test_utils"
    check_make_dir(test_dir)
    dirs = os.listdir("tests/")

    assert test_folder in dirs
    check_delete_dir(test_dir)
    assert os.path.isdir(test_dir) == False
    check_delete_dir(test_dir)
    assert os.path.isdir(test_dir) == False
