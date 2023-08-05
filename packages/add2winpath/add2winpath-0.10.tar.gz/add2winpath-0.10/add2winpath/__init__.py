import itertools
import os
import re
import subprocess
import tempfile
from math import floor
from typing import Union, List

from list_all_files_recursively import get_folder_file_complete_path
from reggisearch import search_values
from touchtouch import touch


def get_tmpfile(suffix=".bin"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    touch(filename)
    return filename


envdict = dict([x for x in os.__dict__["environ"].items() if isinstance(x[1], str)])


def add_to_path_all_users(
    folders: Union[str, List[str]],
    remove_from_path: Union[str, List[str]],
    beginning: bool = False,
) -> str:
    """
    Adds the specified folders to the PATH environment variable for all users on the system.

    Args:
        folders (Union[str, List[str]]): A string or list of strings representing the folders to be added to the PATH.
        remove_from_path (Union[str, List[str]]): A string or list of strings representing the folders to be removed from the PATH.
        beginning (bool, optional): A boolean indicating whether the folders should be added to the beginning or end of the PATH. Defaults to False.

    Returns:
        str: A string representing the registry script that was executed to update the PATH environment variable.

    """
    addpath = folders
    if not isinstance(remove_from_path, list):
        remove_from_path = [remove_from_path]
    remove_from_path = [os.path.normpath(x.strip()) for x in remove_from_path]
    if not isinstance(addpath, list):
        addpath = [addpath]
    di = search_values(
        mainkeys=r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
        subkeys=("Path",),
    )
    splitpath = di[list(di.keys())[0]]["Path"].split(";")
    if beginning:
        splitpath = addpath + splitpath
    else:
        splitpath.extend(addpath)
    validp = []
    for x in splitpath:
        x = os.path.normpath(x.strip())
        try:
            valid = re.findall(r"%+([^%]+)%+", x)[0].upper() in envdict
        except Exception:
            valid = os.path.isdir(x) and os.path.exists(x) and os.path.isabs(x)
        if valid:
            if x not in validp:
                if x not in remove_from_path:
                    validp.append(x)
        else:
            print(f"not valid: {x}")
    validpstr = ";".join(validp)

    regscript = f"""
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment]
"Path"="{validpstr.replace(os.sep, os.sep+os.sep)}"
    """
    exere = get_tmpfile(suffix=".reg")
    strir = regscript.strip()
    with open(exere, mode="w", encoding="utf-8") as f:
        f.write(strir)
    subprocess.run(rf'%systemroot%\system32\Reg.exe import "{exere}"', shell=True)
    return strir


def iter_split_list_into_chunks_fill_rest(n, iterable, fillvalue="00"):
    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)


def add_to_path_current_user(
    folders: Union[str, List[str]],
    remove_from_path: Union[str, List[str]],
    beginning: bool = False,
) -> str:
    """
    Adds the specified folders to the PATH environment variable of the current user.

    Args:
        folders (Union[str, List[str]]): The folder(s) to be added to the PATH environment variable.
        remove_from_path (Union[str, List[str]]): The folder(s) to be removed from the PATH environment variable.
        beginning (bool, optional): If True, the specified folders will be added to the beginning of the PATH variable.
                                    If False, the specified folders will be added to the end of the PATH variable. Defaults to False.

    Returns:
        str: The string representation of the registry key that was added to the Windows registry.

    """
    addpath = folders
    if not isinstance(remove_from_path, list):
        remove_from_path = [remove_from_path]
    remove_from_path = [os.path.normpath(x.strip()) for x in remove_from_path]
    if not isinstance(addpath, list):
        addpath = [addpath]
    usersecureid = sorted(
        [
            x.strip()
            for x in subprocess.run(
                f"""wmic useraccount where name="{os.environ.get('USERNAME')}" get sid""",
                shell=True,
                capture_output=True,
            ).stdout.splitlines()
        ],
        key=len,
    )[-1].decode("utf-8")
    di2 = search_values(
        mainkeys=rf"HKEY_USERS\{usersecureid}\Environment", subkeys=("Path",)
    )
    userp = di2[list(di2.keys())[0]]["Path"]
    splitpath = userp.split(";")
    if beginning:
        splitpath = addpath + splitpath
    else:
        splitpath.extend(addpath)
    validp = []
    for x in splitpath:
        x = os.path.normpath(x.strip())
        try:
            valid = re.findall(r"%+([^%]+)%+", x)[0].upper() in envdict
        except Exception:
            valid = os.path.isdir(x) and os.path.exists(x) and os.path.isabs(x)
        if valid:
            if x not in validp:
                if x not in remove_from_path:
                    validp.append(x)
        else:
            print(f"not valid: {x}")
    validpstr = ";".join(validp)

    vala = [hex(x)[2:].zfill(2) for x in validpstr.encode("utf-16-le")]
    valaad = list(
        iter_split_list_into_chunks_fill_rest(
            floor(len(vala) / 4), vala, fillvalue="00"
        )
    )
    valaad.append(("00",) * len(valaad[0]))
    valaad = [",".join(list(x)) for x in valaad]
    valaadlast = valaad[-1]
    valadfirst = valaad[:-1]
    valadfirst = [x + ",\\" for x in valadfirst]
    valaad = valadfirst + [valaadlast]
    valaad = "\n".join(valaad)
    valaad = (
        rf"""
Windows Registry Editor Version 5.00

[HKEY_USERS\{usersecureid}\Environment]
"Path"=hex(2):"""
        + valaad
    )
    exere = get_tmpfile(suffix=".reg")
    strir = valaad.strip()
    with open(exere, mode="w", encoding="utf-8") as f:
        f.write(strir)
    subprocess.run(rf'%systemroot%\system32\Reg.exe import "{exere}"', shell=True)
    return strir


def get_all_subfolders_from_folder(folders: Union[str, List[str]]) -> List[str]:
    """
    Returns a sorted list of unique subfolder names contained within the specified folder(s).

    Args:
        folders (Union[str, List[str]]): A string representing the path(s) to the folder(s) to search for subfolders.

    Returns:
        List[str]: A sorted list of unique subfolder names contained within the specified folder(s).
    """
    return list(sorted(set([x.folder for x in get_folder_file_complete_path(folders)])))

