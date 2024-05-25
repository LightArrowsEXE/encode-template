from stgpytools import FileWasNotFoundError, SPath, SPathLike

from .logger import Log

__all__: list[str] = [
    "get_src_paths"
]


def get_src_paths(
    dir: SPathLike, script_filename: SPathLike,
    suffix: str = ".m2ts", recursive: bool = False
) -> list[SPath]:
    """
    Get the source paths for the script as a list of SPaths.

    :param dir:                     The source directory.
    :param script_filename:         The script filename.
    :param suffix:                  The suffix of the source file.
    :param recursive:               Whether to search recursively.

    :return:                        A list of matched source paths.

    :raises FileWasNotFoundError:   No files were found.
    """

    src_dir = SPath(dir)
    src_name = SPath(script_filename).with_suffix(suffix).to_str().split('_')[-1]

    results = list(src_dir.rglob(src_name) if recursive else src_dir.glob(src_name))

    if not results:
        raise FileWasNotFoundError(
            f"Could not find any files matching \"{src_name}\" in \"{src_dir.absolute()}\". "
            "Please check the source directory, the script filename, and the file extension.",
            get_src_paths,
        )

    Log.debug(f"Found {len(results)} files matching \"{src_name}\" in \"{src_dir.absolute()}\".", get_src_paths)
    Log.debug(f"Source paths: {results}", get_src_paths)

    return results
