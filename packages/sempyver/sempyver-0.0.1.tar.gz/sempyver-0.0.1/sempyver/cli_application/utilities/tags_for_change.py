"""
Tags for type of SemVer change.
"""
from colorama import init, Fore, Style

# Init colorama and other used variables.
init()
BLUE = Fore.BLUE
RESET = Style.RESET_ALL

SEMVER_TAGS = {
    "major": [
        (f"⚰️ {BLUE}Remove{RESET}: Removed features.", "REMOVE"),
        (f"🚚 {BLUE}Rename{RESET}: Renamed features.", "RENAME"),
        (f"✏️ {BLUE}I/O{RESET}: Changing input/output of features.", "I/O"),
        (f"💥 {BLUE}Behavior{RESET}: Changing features behavior.", "BEHAVIOR")
    ],
    "minor": [
        (f"✨ {BLUE}Feature{RESET}: New feature.", "FEATURE"),
        (f"➕  {BLUE}Add{RESET}: Add functionality to existing feature.", "ADD"),
        (f"✏️ {BLUE}I/O{RESET}: Include optional input/output to a feature.", "I/O"),
        (f"🗑️ {BLUE}Deprecated{RESET}: Deprecated features.", "DEPRECATED"),
    ],
    "patch": [
        (f"♻️ {BLUE}Refactor{RESET}: Refactor of existing code.", "REFACTOR"),
        (f"🐛  {BLUE}Bug{RESET}: Fix a bug.", "BUG"),
        (f"⚡️ {BLUE}Optimization{RESET}: Simple optimization of code.", "OPTIMIZATION"),
        (f"🧪 {BLUE}Tests{RESET}: Include or update tests.", "TESTS"),
        (f"🩹 {BLUE}Patch{RESET}: Include or delete logs, catch errors or related things.", "PATCH")
    ]
}

# Based on the https://keepachangelog.com/en/1.1.0/
CHANGELOG_TAG = {
    "REMOVE": "Removed",
    "RENAME": "Changed",
    "I/O": "Changed",
    "BEHAVIOR": "Changed",
    "FEATURE": "Added",
    "ADD": "Added",
    "DEPRECATED": "Deprecated",
    "REFACTOR": "Fixed",
    "BUG": "Fixed",
    "OPTIMIZATION": "Fixed",
    "TESTS": "Changed",
    "PATCH": "Changed"
}

# How to update the version number. 100 is 1.x.x; 10 is x.1.x and 1 is x.x.1
VERSION_UPDATE = {
    "major": 0,
    "minor": 1,
    "patch": 2
}
