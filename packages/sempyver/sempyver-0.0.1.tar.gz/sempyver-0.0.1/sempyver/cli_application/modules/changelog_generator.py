"""
Generate a changelog file using the SemVer version.
"""
import os
import shutil
import sys
from typing import Dict, List, Union, Tuple
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from colorama import init, Fore, Style
# Local imports
from sempyver.helpers.cache_generator import open_cache_file, create_cache
from sempyver.cli_application.utilities.tags_for_change import CHANGELOG_TAG, VERSION_UPDATE


def update_version(change: str) -> str:
    """Update the version to write it on the changelog.

    Args:
        change (str): Type of change.

    Returns:
        str: New version
    """
    version = "1.0.0"
    # Use the change list
    position_to_change: int = VERSION_UPDATE[change]
    version_numbers: Dict[str, str] = {
        f"Pos. {i}": v for i, v in enumerate(version.split("."))}
    new_version: Dict[str, str] = {}
    _position = f"Pos. {position_to_change}"
    already_upgrade_version: bool = False
    for position, number_of_version in version_numbers.items():
        if position != _position and already_upgrade_version is False:
            new_version[position] = number_of_version
        elif position == _position:
            new_version[position] = f"{int(number_of_version)+1}"
            already_upgrade_version = True
        else:
            new_version[position] = "0"
    # Return the new version
    return ".".join(version for version in new_version.values())


def read_changesets() -> Union[
        Tuple[Dict[str, List[str]], str, List[str]],
        Tuple[None, None, None]]:
    """Read all the changesets files from the changeset folders.

    Returns:
        Union[List[str], List[None]]: Content found
    """
    changeset_dir = Path(str(Path().absolute()) + "/.changesets")
    if not changeset_dir.exists():
        # Init colorama
        init()
        print(f"There's no {Fore.BLUE}changesets{Style.RESET_ALL} to add." +
              f" {Fore.RED}Going to exit{Style.RESET_ALL}...")
        return None, None, None
    # Iterate over the changeset folder
    files_in_dir = list(changeset_dir.iterdir())
    if not files_in_dir:
        return None, None, None
    # Also, open the cache file for the changesets
    previous_changeset = open_cache_file(
        Path(str(Path().absolute()) + "/.sempyver_cache"), "r")
    if previous_changeset is None or len(previous_changeset) < 1:
        previous_changeset = {"files": []}
    # Then, if you find files in the directory, retrieve all the content inside them
    content_from_files: Dict[str, List[str]] = defaultdict(list)
    # Read the content inside the directory
    type_of_changes: List[str] = []
    for file in files_in_dir:
        if os.path.basename(file) in previous_changeset["files"]:
            # Don't add the info from this changeset
            continue
        read_file: List[str] = file.open("r", encoding="utf-8").readlines()
        type_of_changes.append(read_file[1].split(":")[0])
        # And add that change in the content from files
        change_desc = read_file[4].replace("\n", "")
        changelog_tag = CHANGELOG_TAG[change_desc.split("`")[1]]
        # Define here the append operation
        content_from_files[changelog_tag].append(f"- {change_desc}\n")
    # Define the change
    if len(type_of_changes) < 1:
        return None, None, None
    change = min(type_of_changes, key=lambda c: VERSION_UPDATE[c])
    # Return the name of the files in str
    files_to_add = [str(file).rsplit(".changesets/", maxsplit=1)[-1]
                    for file in files_in_dir]
    # Return the parameters
    return content_from_files, change, files_to_add


def read_changelog() -> Union[List[str], None]:
    """Search to see if you can find a changelog file in this directory.

    Returns:
        Union[List[str], List[None]]: Content found
    """
    current_dir = Path().absolute()
    # Iterate over the current dir
    changelog_file = list(filter(lambda file: str(file).endswith(
        "CHANGELOG.md"), current_dir.iterdir()))
    if not changelog_file:
        return None
    # If there's a CHANGELOG file, open it.
    return changelog_file[0].open("r", encoding="utf-8").readlines()


def write_changelog() -> None:
    """Write a changelog file using the last changesets that can be found."""
    # Initialize the content to write in the new changelog
    content_to_write: List[str] = ["# Changelog\n\n"]
    # Obtain the content from the .changesets that are right now in the .changeset
    content_from_changesets, type_of_change, files = read_changesets()
    if not content_from_changesets:
        sys.exit()
    # Now, create a cache to avoid the unnecessary creation of repeated files
    create_cache(files)
    # Retrieve the version to assign
    if type_of_change:
        version_to_assign = update_version(type_of_change)
        content_to_write.append(
            f"## [{version_to_assign}] - {datetime.now().date()}\n\n")
    # Add the `content_from_changesets` to the content_to_write
    for key, items in content_from_changesets.items():
        content_to_write.append(f"### {key}\n\n")
        for item in items:
            content_to_write.append(item)
        content_to_write.append("\n")
    # Try to find a changelog file
    current_changelog = read_changelog()
    if current_changelog:
        search_useful_content: bool = True
        while search_useful_content and len(current_changelog) > 1:
            if current_changelog[0].startswith("#") and current_changelog[0] != "# Changelog\n":
                search_useful_content = False
            else:
                current_changelog = current_changelog[1:]
        # Add the current_changelog to the content_to_write
        content_to_write += current_changelog
    # Write the changelog file
    with open("CHANGELOG.md", "w", encoding="utf-8") as new_changelog:
        for content in content_to_write:
            new_changelog.write(content)
    # Delete the changesets
    delete_changesets()


def delete_changesets() -> None:
    """Delete all the changesets in the folder `./changesets`"""
    path: Path = Path(str(Path().absolute()) + "/.changesets")
    if path.is_dir():
        shutil.rmtree(path)
        return
    return
