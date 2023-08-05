# add2winpath

Adds/removes folders to the PATH on Windows (Current User/All Users). It doesn't spoil paths with variables (e.g. %windir%\system32)

### pip install add2winpath

### Tested against Windows 10 / Python 3.10 / Anaconda 

## Usage

```python
# Adds "folders" to the path (beginning) and removes "remove_from_path",
# the function doesn't mess around with file paths containing variables like "%windir%\system32"

from add2winpath import add_to_path_all_users,add_to_path_current_user,get_all_subfolders_from_folder
cva0 = add_to_path_current_user(
    folders=[
        "c:\\cygwin\\bin",r"C:\baba ''bubu"
    ],
    remove_from_path=["c:\\cygwin"],
    beginning=True,
)
cva1 = add_to_path_all_users(
    folders=["c:\\cygwin\\bin", "c:\\cygwin"],
    remove_from_path=["c:\cygwin3"],
    beginning=True,
)
allsubfolders = get_all_subfolders_from_folder(
    folders=[r"C:\cygwin\var\lib\rebase"]
)  # list of all subfolders

```

## add_to_path_all_users

```python
add_to_path_all_users(folders: Union[str, List[str]], remove_from_path: Union[str, List[str]], beginning: bool = False) -> str
    Adds the specified folders to the PATH environment variable for all users on the system.
    
    Args:
        folders (Union[str, List[str]]): A string or list of strings representing the folders to be added to the PATH.
        remove_from_path (Union[str, List[str]]): A string or list of strings representing the folders to be removed from the PATH.
        beginning (bool, optional): A boolean indicating whether the folders should be added to the beginning or end of the PATH. Defaults to False.
    
    Returns:
        str: A string representing the registry script that was executed to update the PATH environment variable.

```
## add_to_path_current_user


```python
add_to_path_current_user(folders: Union[str, List[str]], remove_from_path: Union[str, List[str]], beginning: bool = False) -> str
    Adds the specified folders to the PATH environment variable of the current user.
    
    Args:
        folders (Union[str, List[str]]): The folder(s) to be added to the PATH environment variable.
        remove_from_path (Union[str, List[str]]): The folder(s) to be removed from the PATH environment variable.
        beginning (bool, optional): If True, the specified folders will be added to the beginning of the PATH variable.
                                    If False, the specified folders will be added to the end of the PATH variable. Defaults to False.
    
    Returns:
        str: The string representation of the registry key that was added to the Windows registry.
```


## get_all_subfolders_from_folder


```python
	
get_all_subfolders_from_folder(folders: Union[str, List[str]]) -> List[str]
    Returns a sorted list of unique subfolder names contained within the specified folder(s).
    
    Args:
        folders (Union[str, List[str]]): A string representing the path(s) to the folder(s) to search for subfolders.
    
    Returns:
        List[str]: A sorted list of unique subfolder names contained within the specified folder(s).
```