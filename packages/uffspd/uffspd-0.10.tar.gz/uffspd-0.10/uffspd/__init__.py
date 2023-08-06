import os
import pathlib
import re
import tempfile
from typing import Union

import requests
from a_pandas_ex_fastloc import (
    pd_add_fastloc,
)
import numpy as np
from touchtouch import touch

pd_add_fastloc()
import pandas as pd
import subprocess
from a_pandas_ex_fast_string import pd_add_fast_string

pd_add_fast_string()

dtypes = {
    "aa_path": "string",
    "aa_name": "string",
    "aa_path_only": "string",
    "aa_size": np.uint64,
    "aa_size_on_disk": np.uint64,
    "aa_created": "category",
    "aa_last_written": "category",
    "aa_last_accessed": "category",
    "aa_descendents": np.uint32,
    "aa_read_only": np.uint8,
    "aa_archive": np.uint8,
    "aa_system": np.uint8,
    "aa_hidden": np.uint8,
    "aa_offline": np.uint8,
    "aa_not_content_indexed_file": np.uint8,
    "aa_no_scrub_file": np.uint8,
    "aa_integrity": np.uint8,
    "aa_pinned": np.uint8,
    "aa_unpinned": np.uint8,
    "aa_directory_flag": np.uint8,
    "aa_compressed": np.uint8,
    "aa_encrypted": np.uint8,
    "aa_sparse": np.uint8,
    "aa_reparse": np.uint8,
    "aa_attributes": np.uint16,
}


def get_tmpfile(suffix=".bin"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    touch(filename)
    return filename


def check_if_installed(apppath):
    if not apppath:
        apppath = ""
    if not os.path.exists(apppath):
        bax = requests.get(
            "https://github.com/githubrobbi/Ultra-Fast-File-Search/raw/master/bin/x64/COM/uffs.com"
        )
        newpath = os.path.normpath(
            os.path.join(os.path.normpath(os.path.dirname(__file__)), "uffs.com")
        )
        with open(
            newpath,
            mode="wb",
        ) as f:
            f.write(bax.content)
        return newpath
    else:
        return apppath


def vartolist(regular_expressions):
    return (
        [regular_expressions]
        if isinstance(regular_expressions, str)
        else list(regular_expressions)
        if not isinstance(regular_expressions, list)
        else regular_expressions
    )


def list_all_files(
    path2search: str,
    file_extensions: Union[None, list, tuple] = None,
    uffs_com_path: Union[None, str] = None,
) -> pd.DataFrame:
    r"""
    This function lists all files in a directory and its subdirectories that match the specified file extensions.
    It is insanely fast. On my C drive, the data is taking up 350 GB, UFFS was able to scan the
    whole HD, in less than 3 minutes. And the best thing is: This module here formats the UFFS' output and transforms
    the huge binary string into data types. A lot of times, you have to do some post-processing  after searching with regular
     Expressions in huge datasets.  Using UFFS + Pandas makes everything easier.


    Args:
        path2search (str): The path to the directory to search for files.
        file_extensions (Union[None, list, tuple], optional): A list or tuple of file extensions to search for. Defaults to None (all files are accepted).
        uffs_com_path (Union[None, str], optional): The path to the Universal File Finder command-line tool. Defaults to None.
        If it is None, the app will try to install it. If you want to install it by yourself, visit this page: https://github.com/githubrobbi/Ultra-Fast-File-Search (Important: don't download the .exe file, you need the .com version
    !)


    Returns:
        pd.DataFrame: A pandas DataFrame containing information about the files found, including their names, paths, sizes, and modification dates and so on
        https://github.com/githubrobbi/Ultra-Fast-File-Search

    """
    uffs_com_path = check_if_installed(uffs_com_path)
    uffs_com_path = os.path.normpath(uffs_com_path)
    if uffs_com_path:
        print(f"UFFS path: {uffs_com_path} ")

    if not file_extensions:
        file_extensions = "--ext=*"
    else:
        feax = vartolist(file_extensions)
        file_extensions = "--ext=" + (
            ",".join([x.strip(". ") for x in feax]).strip().strip(".")
        )
    exefile = os.path.normpath(uffs_com_path)
    parsedpath = pathlib.Path(path2search).as_posix()
    wholecmdsearch = [rf"{exefile}", "--columns=all", file_extensions, parsedpath]
    dada = subprocess.run(
        wholecmdsearch,
        shell=False,
        capture_output=True,
    )
    out = dada.stdout
    dat2 = out.splitlines()
    df2 = pd.DataFrame(dat2)
    df3 = df2.copy()
    df = df3[0].s_str().rsplit(b",", n=24, expand=True)
    newcols = [
        "aa_"
        + re.sub(
            r"\W+", "_", x.decode("utf-8", "ignore").strip(""""\' """).lower()
        ).strip("_ ")
        for x in df.iloc[0].to_list()
    ]
    df.columns = newcols
    df = df[2:].drop_duplicates().dropna().reset_index(drop=True)

    for col in ["aa_path", "aa_name", "aa_path_only"]:
        if col in ["aa_path", "aa_path_only"]:
            df[col] = df[col].apply(os.path.normpath)
        df[col] = (
            np.char.array(df[col].__array__()).strip(b'" \r').decode("utf-8", "replace")
        )
        if col in ["aa_path", "aa_path_only"]:
            df[col] = df[col].s_str().rstrip(r"\ ")

    df = df.astype(dtypes)
    return df
