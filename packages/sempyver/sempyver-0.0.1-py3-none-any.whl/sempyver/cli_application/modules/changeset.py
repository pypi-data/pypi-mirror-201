"""
Create a changeset file given a list of options and inputs.
"""
import sys
import os
from typing import Dict, List
from pathlib import Path
from colorama import init, Fore, Style
import inquirer as iq
from faker import Faker
# Import the tags for the type of change
from sempyver.cli_application.utilities.tags_for_change import SEMVER_TAGS
# Import the custom inquirer theme
from sempyver.cli_application.utilities.theme import CustomTheme

# Init colorama and Faker
init()
RESET = Style.RESET_ALL
fake = Faker()


class Changeset:
    """Class that generate the changeset file given a list of options and inputs
    given by the user.

    Public methods:
    ---------------
        - run: Run the questions to obtain the data from the user
        - create_file: Create the .md file once the questions were asked.
    """
    __slots__ = ["_data"]

    def __init__(self) -> None:
        # Instance the _data variable
        self._data: List[Dict[str, str]] = []

    def __version_changes(self, data: Dict[str, str]) -> None:
        """Ask for how this entire changes would affect the project.

        Raises:
        -------
            - ValueError: If the user doesn't provide the type of SemVer.
        """
        question = [
            iq.List("change_type",
                    message=f"These {Fore.BLUE}changes{RESET}" +
                    f" for {Fore.GREEN}{data['package']}{RESET} are close to which " +
                    f"version of {Fore.GREEN}SemVer{RESET}?",
                    choices=[
                        ("MAJOR: Most of the times related to breaking changes.", "major"),
                        ("MINOR: New features that keeps backwards compatibility.", "minor"),
                        ("PATCH: Refactors, bugs, fixes and small changes.", "patch")
                    ],
                    autocomplete=False
                    )
        ]
        answer = iq.prompt(question, theme=CustomTheme(),
                           raise_keyboard_interrupt=True)
        # Check that the user has provided a type of SemVer
        if not answer or not answer["change_type"]:
            raise ValueError(
                f"You need to provide a type of {Fore.GREEN}SemVer{RESET}.")
        # Add the response to the dictionary of data
        data.update(answer)

    def __tag_changes(self, data: Dict[str, str]) -> None:
        """Depending on the type of change (MAJOR, MINOR or PATCH)
        it can tag the type of change. This tags would be taken of a dictionary
        outside of this file.

        Raises:
        -------
            - ValueError: If the user doesn't select a tag for the change.
        """
        # Obtain the tags for this type of change.
        tags = SEMVER_TAGS[data["change_type"]]
        question = [
            iq.List("tag",
                    message=f"Which {Fore.BLUE}tag{RESET} is more accurate for the change " +
                    f"{Fore.RED}{data['change_type']}{RESET} in the package {Fore.GREEN}" +
                    f"{data['package']}{RESET}?",
                    choices=tags,
                    other=True,
                    autocomplete=False
                    )
        ]
        answer = iq.prompt(question, theme=CustomTheme(),
                           raise_keyboard_interrupt=True)
        # Check that the user has provided a correct answer.
        if not answer or not answer["tag"]:
            raise ValueError(
                f"You must provide or select a correct {Fore.BLUE}tag{RESET}.")
        # Add the tag to the data
        data.update(answer)

    def __describe_changes(self, data: Dict[str, str]) -> None:
        """Describe the changes that you are including for this new release.

        Raises:
        -------
            - ValueError: If the user doesn't provide a description of the changes.
            - ValueError: If the description of the user is not long enough of if it is too long.
        """
        #! TODO: Add a variable length configurable in the `pyproject.toml`
        min_length: int = 0
        max_length: int = 1000
        question = [
            iq.Text("desc",
                    message=f"Describe the {Fore.BLUE}changes{RESET} that you want to" +
                    f" include in this new release of {Fore.BLUE}{data['package']}{RESET}"
                    )
        ]
        answer = iq.prompt(question, theme=CustomTheme(),
                           raise_keyboard_interrupt=True)
        # Check that the uses has provided an answer
        if not answer or not answer["desc"]:
            raise ValueError(
                f"\nYou must provide a description of the {Fore.BLUE}changes{RESET}.")
        # Now, check that the description is not too short or too large.
        if len(answer["desc"]) < min_length or len(answer["desc"]) > max_length:
            # Define the word to use in the raise
            length: str = "short" if len(answer["desc"]) < 80\
                else "large"
            raise ValueError(f"\nYou must provide a {Fore.GREEN}{length}{RESET} description." +
                             f" Your actual description contains {Fore.RED}{len(answer['desc'])}" +
                             f"{RESET} characters.")
        # Now, update the data
        data.update(answer)

    def __update_packages(self) -> None:
        """Find the packages available and let the user decide which package would be
        updated with this release.

        Raises:
        --------
            - ValueError: If the `other` option returns nothing.
        """
        packages_found = self.__find_modules()
        question = [
            iq.Checkbox("packages",
                        message=f"Which of the following {Fore.BLUE}packages{RESET} or " +
                        f"{Fore.BLUE}modules{RESET} are going to be updated with this " +
                        f"{Fore.GREEN}release{RESET}?",
                        choices=packages_found,
                        other=True
                        )
        ]
        answer = iq.prompt(question, theme=CustomTheme(),
                           raise_keyboard_interrupt=True)
        # If not answer is provided
        if not answer or not answer["packages"]:
            raise ValueError(
                f"You must provide a {Fore.BLUE}package{RESET} to be updated.")
        # Create a list with all the packages given
        self._data += [{"package": package} for package in answer["packages"]]

    def __find_modules(self) -> List[str]:
        """Find the available modules to update only if the folder has a `__init__.py` inside.

        Returns:
        --------
            - A list with the packages or modules available to update.
        """
        module_or_package_available: List[str] = []
        for root, _, files in os.walk(str(Path().absolute())):
            # If the __init__ exist on the files, then append the folder name to the module list
            if "__init__.py" in files and not "/." in root:
                module_or_package_available.append(root.split("/")[-1])

        return module_or_package_available

    # =============================================== #
    #             RUN AND CREATE METHODS              #
    # =============================================== #

    def run(self) -> None:
        """Run the changeset questions to obtain the required information
        to created the file.
        """
        try:
            self.__update_packages()
            for package in self._data:
                self.__version_changes(package)
                self.__tag_changes(package)
                self.__describe_changes(package)
                print('\n')
        except KeyboardInterrupt:
            print(f"Operation {Fore.RED}cancelled{RESET} by user.")
            sys.exit()
        except ValueError as error:
            print(
                f"{error} {Fore.RED}Closing the app due to lack of information{RESET}...")
            sys.exit()

    def create_file(self) -> List[str]:
        """If we have data, create a changeset file

        Raise:
        -------
            - ValueError: If the `run` has been not run yet.

        Returns:
        -------
            - List with the names of the recently created changesets
        """
        name_of_changeset_files: List[str] = []
        if not self._data:
            raise ValueError(
                "We have no data to create the changeset file. Please run the `run` method first.")
        # Then, create the changeset for each package
        for package in self._data:
            fake_file_name: str = fake.file_name(extension='md')
            changesets_path = Path(f".changesets/{fake_file_name}")
            changesets_path.parent.mkdir(parents=True, exist_ok=True)
            with changesets_path.open("w", encoding="utf-8") as file:
                file.write(
                    10*"-"+"\n" +
                    f"{package['change_type']}:{package['package']}\n" +
                    10*"-"+"\n\n")
                file.write(f"`{package['tag']}`:{package['desc']}\n")
            file.close()
            # Print a message saying that the file was created successfully
            print(f"File with name {Fore.BLUE}{fake_file_name}{RESET} was created" +
                  f" {Fore.GREEN}successfully{RESET}!")
            name_of_changeset_files.append(fake_file_name)
        # Return the name at the end
        return name_of_changeset_files
