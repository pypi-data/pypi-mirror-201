from pathlib import Path as _Path
import fire as _fire
from rich import traceback
from genpypress import app_cc as _app_cc
from genpypress import app_patch_to_validtime as _app_patch_to_validtime
from genpypress import app_join as _app_join

traceback.install(show_locals=False, max_frames=1)

_cwd = str(_Path.cwd())


def join(
    directory: str,
    join_to: str = "part_1.sql",
    delete: bool = True,
    mask: str = "*.sql",
    encoding: str = "utf-8",
    add_comment: bool = True,
):
    """sloučí sadu SQL souborů do jednoho, a smaže je"""
    _app_join.join_files(
        directory=directory, join_to=join_to, delete=delete, mask=mask, encoding=encoding, add_comment=add_comment
    )
    print("done")


def apatch(directory: str, limit: int = 50, encoding: str = "utf-8"):
    """apatch: patch TPT skriptů pro async stage

    Args:
        directory (str): adresář, kde jsou TPT skripty
        limit (int): kolik maximálně souborů upravit
        encoding (str): jak jsou soubory nakódované
    """
    d = _Path(directory)
    if not d.is_dir():
        print(f"toto není adresář: {directory}")
        exit(1)
    _app_patch_to_validtime.async_patch(d, limit, encoding)


def cc(
    directory: str,
    scenario: str = "drop",
    input_encoding: str = "utf-8",
    output_encoding: str = "utf-8",
    max_files: int = 20,
):
    """cc: conditional create

    Args:
        directory (str): directory where to do the work
        scenario (str): ["drop", "create", "cleanup", "drop-only"]
        input_encoding (str): Defaults to "utf-8".
        output_encoding (str): Defaults to "utf-8".
    """
    _app_cc.conditional_create(directory, scenario, input_encoding, output_encoding, max_files)


def _main():
    _fire.Fire()


if __name__ == "__main__":
    _main()
