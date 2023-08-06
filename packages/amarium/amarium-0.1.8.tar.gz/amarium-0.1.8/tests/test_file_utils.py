import time
import sys
import os
import numpy as np
import pytest

from src.amarium.utils import (
    insert_string_in_file_name,
    prepare_file_name_saving,
    make_date_file_name,
    load_json_from_file,
    convert_str_to_bool,
    make_full_filename,
    save_json_to_file,
    search_subdirs,
    append_slash,
    delete_file,
    write_tar,
    copy_dir,
)

from src.amarium.checks import check_make_file_name_suffix, check_make_dir


def test_delete_file():

    file_name = "./tests/empty.txt"
    with pytest.raises(Exception) as e:
        delete_file(file_name)

    with open(file_name, "w") as fp:
        pass

    delete_file(file_name)
    assert not os.path.isfile(file_name)


def test_check_file_name():
    def make_name(file_name, ending, expectation):
        new_file_name = check_make_file_name_suffix(file_name, ending)
        assert new_file_name == expectation, (
            " old file_name "
            + str(file_name)
            + " ending"
            + str(ending)
            + " returned file_name "
            + str(new_file_name)
        )

    # case 1
    file_name = "foo"
    ending = "bar"
    expectation = "foo.bar"
    make_name(file_name, ending, expectation)
    # case 2
    file_name = "foo.bar"
    ending = None
    expectation = "foo.bar"
    make_name(file_name, ending, expectation)


def test_make_full_name():
    def make_name(prefix, file_name, expectation):
        new_file_name = make_full_filename(prefix=prefix, file_name=file_name)
        assert new_file_name == expectation, (
            str(prefix)
            + " old file_name "
            + str(file_name)
            + " returned file_name "
            + str(new_file_name)
        )

    # case 1
    prefix = "tests"
    file_name = "testfile.png"
    expectation = "tests/testfile.png"
    make_name(prefix, file_name, expectation)
    # case 2
    prefix = None
    file_name = "tests/testfile.png"
    expectation = "tests/testfile.png"
    make_name(prefix, file_name, expectation)
    # case 3
    prefix = "tests/"
    file_name = "/testfile.png"
    expectation = "tests/testfile.png"
    make_name(prefix, file_name, expectation)
    # case 3
    prefix = "tests"
    file_name = "/testfile.png"
    expectation = "tests/testfile.png"
    make_name(prefix, file_name, expectation)
    # case 4
    prefix = "tests/data"
    file_name = "testfile.png"
    expectation = "tests/data/testfile.png"
    make_name(prefix, file_name, expectation)


def test_prepare_file_name_saving():

    # case 1
    test_dir = "tests/data"
    name = "test_file_name_saving"
    suffix = ".txt"
    file_name = prepare_file_name_saving(
        prefix=test_dir, file_name=name, suffix=suffix)
    assert file_name == "tests/data/test_file_name_saving.txt"
    # case 2
    test_dir = "tests/data/"
    file_name = prepare_file_name_saving(
        prefix=test_dir, file_name=name, suffix=suffix)
    assert file_name == "tests/data/test_file_name_saving.txt"
    # case 3
    file_name = "tests/data/test_file_name_saving.txt"
    file_name = prepare_file_name_saving(file_name)
    assert file_name == "tests/data/test_file_name_saving.txt"


def test_insert_string_in_file_name():
    def make_name(file_name, insertions, suffix, expectation):

        new_file_name = insert_string_in_file_name(
            file_name=file_name, insertion=insertion, suffix=suffix
        )
        assert new_file_name == expectation, (
            str(file_name)
            + " old file_name "
            + str(insertion)
            + str(ending)
            + " returned file_name "
            + str(new_file_name)
        )

    # case 1
    file_name = "foo.bar"
    insertion = "fantastic"
    suffix = None
    expectation = "foo_fantastic.bar"
    result_name = make_name(file_name, insertion,
                            suffix, expectation=expectation)

    # case2
    file_name = "foo"
    suffix = ".bar"
    insertion = "fantastic"
    ending = None
    expectation = "foo_fantastic.bar"
    result_name = make_name(
        file_name, insertion, suffix=suffix, expectation=expectation
    )

    # case3
    file_name = "foo"
    suffix = None
    insertion = "fantastic"
    ending = None
    expectation = "foo_fantastic.bar"

    with pytest.raises(
        ValueError,
        match="You must either specify an suffix in the file_name or pass an suffix through the\
            suffix argument. For example the file_name could be 'foo.bar' or you pass\
            file_name'foo' with suffix = '.bar'",
    ):
        new_file_name = insert_string_in_file_name(
            file_name=file_name, insertion=insertion, suffix=suffix
        )

    # case 4
    file_name = "foo"
    suffix = "bar"
    insertion = "fantastic"
    ending = None
    expectation = "foo_fantastic.bar"
    result_name = make_name(
        file_name, insertion, suffix=suffix, expectation=expectation
    )


def test_save_json_to_file():
    """
    The test_save_json_to_file function tests the saving and loading functionalities regarding
    json objects of the package
    :return: None.

    :doc-author: Julian M. Kleber
    """

    prefix = "tests/"
    file_name = "test_json.json"

    # case1
    file_name = make_full_filename(prefix, file_name)
    a = {"1": np.array([1, 2, 3]), "2": np.int32(12)}
    save_json_to_file(a, file_name=file_name)
    loaded_a = load_json_from_file(file_name=file_name)
    assert list(loaded_a.keys()) == list(a.keys())

    # case 2
    file_name == None
    save_json_to_file(a, file_name=file_name)
    loaded_a = load_json_from_file(file_name=file_name)
    assert list(loaded_a.keys()) == list(a.keys())


def test_search_subdir():
    """
    The test_search_subdir function tests the search_subdirs function.
    It does this by creating a directory with two subdirectories, each containing one file.
    The test then calls the search_subdirs function on the parent directory and checks that it returns all three files and both directories.


    :doc-author: Julian M. Kleber
    """

    def check_output(result_files, result_dirs):
        assert len(result_files) == 4
        files = [
            "tests/test_dir_search/dir2/file1",
            "tests/test_dir_search/dir2/dir1/file1",
            "tests/test_dir_search/dir2/file2",
            "tests/test_dir_search/dir1/file1",
        ]
        for name in files:
            assert name in result_files

        reference_sub_dirs = [
            "tests/test_dir_search/dir1",
            "tests/test_dir_search/dir2",
            "tests/test_dir_search/dir2/dir1",
        ]
        assert len(result_dirs) == 3
        for ref in reference_sub_dirs:
            assert ref in result_dirs

    search_dir = "tests/test_dir_search/"
    result_files, result_dirs = search_subdirs(dir_name=search_dir)
    check_output(result_files, result_dirs)

    search_dir = "tests/test_dir_search"
    result_files, result_dirs = search_subdirs(dir_name=search_dir)
    check_output(result_files, result_dirs)


def test_tar_writer():

    target_dir = "tests/test_dir_search"
    file_name = "tests/test.tar"
    write_tar(target_dir=target_dir, file_name=file_name)
    assert os.path.isfile(file_name)
    os.remove(file_name)
    assert not os.path.isfile(file_name)


def test_copy_dir():

    import shutil

    target_dir = "tests/test_dir_copy"
    old_dir = "tests/test_dir_search"
    copy_dir(old_dir, new_dir=target_dir)
    assert os.path.isdir(target_dir)
    shutil.rmtree(target_dir)
    assert not os.path.isdir(target_dir)


def test_str_convert_to_bool():

    test_string = "False"
    test_bool = convert_str_to_bool(test_string)
    assert test_bool is False
    test_string = "True"
    test_bool = convert_str_to_bool(test_string)
    assert test_bool is True


def test_make_date_file_name():

    time_str = time.strftime("%Y%m%d-%H%M%S")
    date_file_name = make_date_file_name(prefix="", file_name="", suffix="")  #
    assert (
        date_file_name == time_str
    ), "The time strings do not match, it could be the function is too slow. That means anyways that the system is not suitable for tests."


def test_attach_string():

    test_string ="test_dir_or_file"
    test_string_mod = append_slash(test_string)
    assert test_string_mod == test_string + "/"

    test_string = "test_dir_or_file/"
    test_string_mod = append_slash(test_string)
    assert test_string_mod == test_string