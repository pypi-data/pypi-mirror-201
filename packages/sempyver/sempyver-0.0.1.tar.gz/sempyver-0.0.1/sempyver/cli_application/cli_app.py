"""
CLI application that include all the modules and the possible ways to use them.
"""
import os
from typing import Callable, List, Tuple, Optional
import click
# Colorama imports
from colorama import init, Fore, Style
# Local imports
from sempyver.cli_application.modules import Changeset, ChangesetCommit, write_changelog


class CLI:
    """CLI application to manage the creation and update of changesets."""
    __slots__ = ["_group", "_reset"]

    def __init__(self) -> None:
        # Init colorama
        init()
        self._reset = Style.RESET_ALL

    def __group(self) -> None:
        """Method to use for group all the applications method"""

    def __parse_args(self, function: Callable, command_name: str,
                     args: List[Tuple[str, str, str, bool]]) -> click.Command:
        """Method to return a callable with the specified arguments using
        the 'click.arguments' method"""
        command = click.command(name=command_name)(function)
        for arg in args:
            click.option(arg[0], arg[1], help=arg[2], is_flag=arg[3])(command)
        return command

    @staticmethod
    def __obtain_git_files_with_differences() -> List[str]:
        """Obtain the files that have a difference with the git origin."""
        command_to_run: str = "git status --porcelain -- '.changesets/*.md'" +\
            " | sed s/^...// | tr '\n' ','"
        # With the subprocess, perform a cmd to obtain all the .md files not uploaded
        md_files = os.popen(cmd=command_to_run).__dict__["_stream"].read()
        return md_files.split(",")[:-1]

    # ------------------------------------ #
    # Add the methods for each application #
    # ------------------------------------ #
    def changeset(self, commit: bool = False, push: bool = False) -> None:
        """Generate a changeset file from a given option of questions."""
        _changesets = Changeset()
        # Depending on the command line arguments, perform a changeset
        _changesets.run()
        files = _changesets.create_file()
        if commit:
            self.commit(push, files)

    def commit(self, push: bool = False, files: Optional[List[str]] = None) -> None:
        """Generate a commit for a given list of changeset objects."""
        if not files:
            files_to_add: List[str] = self.__obtain_git_files_with_differences()
        else:
            files_to_add: List[str] = files
        if not files_to_add:
            print(f"{Fore.RED}There's no files to add.{self._reset}" +
                  f" Please add an {Fore.BLUE}existing one{self._reset} and try again.")
            return
        # Perform the commit
        _changeset_commit = ChangesetCommit()
        _changeset_commit.generate(files_to_add)
        if push:
            _changeset_commit.push()

    def remove_changesets(self) -> None:
        """Remove all the changeset files not uploaded to Git"""
        # Obtain the git files with differences
        md_files = self.__obtain_git_files_with_differences()
        # Now, remove all those files
        for file in md_files:
            os.remove(file)
        # map(os.remove, md_files)
        # Now, print that the files were successfully deleted
        print(f"The {Fore.BLUE}`.changeset/*.md`{self._reset} files were" +
              f" {Fore.GREEN}successfully{self._reset} deleted.")

    def changelog(self) -> None:
        """Create a changelog file with the given changesets."""
        # Just run the write changelog function.
        write_changelog()
        print(
            f"The changelog was created {Fore.GREEN}successfully{self._reset}.")

    def generate(self) -> click.Group:
        """Wrap the CLI application returning the click.Group generated.

        Returns:
        --------
            - Click group generated
        """
        _group = click.group()(self.__group)
        args_per_tool = {
            "change": [
                ("-c", "--commit",
                 "Perform the update of the changeset and include it in a commit.", True),
                ("-p", "--push",
                 "Push the commit generated with the flag `-c` or `--commit`", True)
            ],
            "commit": [
                ("-p", "--push",
                 "Push the commit generated with the flag `-c` or `--commit`", True),
                ("-f", "--files",
                 "Files to add in the commit. It you don't specify anything, we'd search for them",
                 False)
            ],
            "remove": [],
            "changelog": []
        }
        for command, c_name in [(self.changeset, "change"), (self.commit, "commit"),
                                (self.remove_changesets, "remove"), (self.changelog, "changelog")]:
            _group.add_command(self.__parse_args(command, command_name=c_name,
                                                 args=args_per_tool[c_name]))
        return _group
