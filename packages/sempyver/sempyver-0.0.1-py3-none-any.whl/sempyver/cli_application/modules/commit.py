"""
Create and perform a commit operation
from the last tag from change.
"""
import os
from typing import List, Dict


class ChangesetCommit:
    """Create a changeset commit given the information of a changeset created."""
    __slots__ = ["_repo"]

    def generate(self, files: List[str]) -> None:
        """Generate a commit from a given list of files.

        Args:
        -------
            files (List[str]): Files to read.
        """
        changeset_details: List[Dict[str, str]] = []
        # First, open and read each changeset file
        if not files:
            print("There's no changeset file to add. No commit was made.")
            return
        for file in files:
            if ".changesets/" in file:
                file = file.split(".changesets/")[-1]
            # Now, open the file
            with open(".changesets/" + file, "r", encoding="utf-8") as changeset_file:
                lines = [line.replace("\n", "")
                         for line in changeset_file.readlines()]
                # Save the info in a dict that would be inside the changeset_details
                changeset_details.append({
                    "topic": lines[1].split(":")[-1].upper(),
                    "details": lines[4].split(":")[-1],
                    "full details": lines[4],
                    "path": ".changesets/" + file
                })
        # And then, check if there more than 1 file
        if len(changeset_details) > 1:
            files_path = " ".join(file["path"] for file in changeset_details)
            os.system(f'git add {files_path}')
            os.system('git commit -m "Adding changesets."')
        else:
            commit_info = changeset_details[0]
            # Add the changeset file
            os.system('git add '+commit_info["path"])
            # Create a commit for this unique changeset
            os.system(
                f'git commit -m "{commit_info["topic"]}: {commit_info["details"]}"')

    def push(self) -> None:
        """Push the commit into the git branch."""
        os.system('git push')
