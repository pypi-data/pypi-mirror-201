import numpy as np
import click
import subprocess
import os
from rich.console import Console
import re

console = Console()


def findDiff(d1, d2, path=""):
    """
    Find differences between two dictionaries containing NumPy arrays or scalar values.

    Parameters
    ----------
    d1 : dict
        First dictionary to compare.
    d2 : dict
        Second dictionary to compare.
    path : str, optional
        Current path in the dictionary hierarchy. Used for building the error message.
        Defaults to an empty string.

    Raises
    ------
    AssertionError
        If the dictionaries have different keys, values, or shapes.

    Returns
    -------
    None

    Notes
    -----
    This function is designed to compare dictionaries that may contain nested dictionaries
    and NumPy arrays or scalar values. The function checks for differences between the
    dictionaries, raising an AssertionError if any differences are found.

    If a difference is found in the dictionaries, an error message is constructed and raised
    with detailed information about the path of the difference, the expected value, and the
    actual value. If a NumPy array differs, each differing element is listed in the error
    message.

    Examples
    --------
    >>> a = {'a': 1, 'b': 2, 'c': {'d': 4, 'e': np.array([1,2,3])}}
    >>> b = {'a': 1, 'b': 2, 'c': {'d': 4, 'e': np.array([1,2,4])}}
    >>> findDiff(a, b)
    AssertionError:  -> c -> e:
    - e[2]: 3
    + e[2]: 4
    ####################

    >>> c = {'a': 1, 'b': 2, 'c': {'d': 4, 'e': np.array([1,2,3])}}
    >>> d = {'a': 1, 'b': 2, 'c': {'d': 4, 'e': np.array([1,2,3])}}
    >>> findDiff(c, d)
    None
    """

    error_msg = ""
    for k in d1:
        path_k = f"{path} -> {k}" if path else k
        if k not in d2:
            error_msg += f"{path_k} as key not in d2\n"
            continue

        if isinstance(d1[k], dict):
            findDiff(d1[k], d2[k], path_k)
            continue

        if not isinstance(d1[k], np.ndarray):
            if d1[k] != d2[k]:
                error_msg += f"{path_k}: \n"
                error_msg += f"  - {k}: {d1[k]}\n"
                error_msg += f"  + {k}: {d2[k]}\n"
                error_msg += 20 * "#"
            continue

        if d1[k].dtype not in (np.float64, np.int64):
            if not np.array_equal(d1[k], d2[k]):
                error_msg += f"{path_k}: \n"
                error_msg += f"  - {k}: {d1[k]}\n"
                error_msg += f"  + {k}: {d2[k]}\n"
                error_msg += 20 * "#"
            continue

        if d1[k].shape != d2[k].shape:
            error_msg += f"{path_k}: \n"
            error_msg += f"  - {k}.shape: {d1[k].shape}\n"
            error_msg += f"  + {k}.shape: {d2[k].shape}\n"
            error_msg += 20 * "#"
            continue

        diff = np.abs(d1[k] - d2[k])
        if not np.allclose(d1[k], d2[k]):
            error_msg += f"{path_k}: \n"
            for idx, val in np.ndenumerate(diff):
                if val > 0:
                    error_msg += f"  - {k}[{idx}]: {d1[k][idx]}\n"
                    error_msg += f"  + {k}[{idx}]: {d2[k][idx]}\n"
                    error_msg += 20 * "#"

    if error_msg:
        raise AssertionError(error_msg)


@click.command()
@click.option("--filename", help="filename of the jnl-File", required=False)
@click.option("--keys", "-k", help="key sequence", multiple=True)
@click.option("--calls", "-c", help="object call", multiple=True)
def extract_data_from_jnl(
    keys,
    calls,
    filename=None,
):
    """
    Extracts data from a jnl file using Abaqus.

    Parameters
    ----------
    filename : str, optional
        Filename of the jnl file. If not provided, all ".jnl" files in the current
        directory are used.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If the path to the Abaqus site-packages directory cannot be extracted.

    Notes
    -----
    This function requires Abaqus to be installed and the Abaqus environment to be
    set up properly. The Abaqus site-packages directory is determined using the
    `site` module and the path to the jnl loader script is constructed from it.
    The jnl loader script is then called with the specified jnl file, if any,
    using the Abaqus command line interface.

    """

    cmd_site = 'abaqus python -c "import site; print(site.getsitepackages()[0])"'
    path_site = subprocess.check_output(cmd_site, encoding="utf-8", shell=True).replace("\n", "")
    path_regex = r"\b[A-Z]:\\(?:[^\\\s]+\\)*[^\\\s]+\\?"
    match = re.search(path_regex, path_site)
    if match:
        path_site = match.group()
    else:
        raise TypeError("no path found")

    if not (keys or calls):
        raise click.UsageError("Must provide either --keys or --calls.")

    path_abml = os.path.join(path_site, "Lib", "site-packages", "abml").replace("\n", "")
    jnl_loader = os.path.join(path_abml, "jnl_loader.py").replace("\n", "")
    if filename is not None:
        files = np.array([filename]).flatten()
    else:
        files = os.listdir(".")

    for file in files:
        if ".jnl" in file:
            filename_path = os.path.abspath(file).replace("\n", "")
            cmd = f'abaqus cae nogui="{jnl_loader}" -- --filename "{filename_path}" --calls {calls[0]}'
            subprocess.call(cmd, shell=True)
