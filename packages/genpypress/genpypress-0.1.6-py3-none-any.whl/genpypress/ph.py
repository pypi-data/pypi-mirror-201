from pathlib import Path as _Path
import fire as _fire
from genpypress import app_cc as _app_cc
from genpypress import app_patch_to_validtime as _app_patch_to_validtime


def apatch(directory: str, limit: int = 50, encoding: str = "utf-8"):
    """apatch: patch TPT skriptů pro async stage

    Args:
        directory (str): adresář, kde jsou TPT skripty
        limit (int): kolik maximálně souborů upravit
        encoding (str): jak jsou soubory nakódované
    """
    d = _Path(directory)
    assert d.is_dir(), f"toto není adresdář: {directory}"
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
    _app_cc.conditional_create(
        directory, scenario, input_encoding, output_encoding, max_files
    )


def _main():
    _fire.Fire()


if __name__ == "__main__":
    _main()
