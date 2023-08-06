from pydantic import FilePath, DirectoryPath


types_map = {
    "string": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
    "tuple": tuple,
    "set": set,
    "file_path": FilePath,
    "directory_path": DirectoryPath,
}