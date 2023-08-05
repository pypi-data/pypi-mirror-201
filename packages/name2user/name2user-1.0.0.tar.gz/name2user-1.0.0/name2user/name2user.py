#!/usr/bin/env python3

import sys
import argparse
from .user_name_creation_methods import UserNameCreationMethods
from .user_name_generator import UserNameGenerator

# Description text
desc_text = f"""Converts full names to user names.

Examples
========
{sys.argv[0]} \"Liam Smith\"
{sys.argv[0]} \"Olivia Johnson\" -c flast
{sys.argv[0]} \"Noah Williams\" -m \"somecompany.com\"
cat some_text_file | {sys.argv[0]}
cat some_text_file | {sys.argv[0]} -c fdlast > results.txt

Options for conversion (-c)
============================
all (All variations)
last (Last name only)
flast (First letter of first name + last name)
fdlast (First letter of first name + dot + last name)
full (Full name withouth spaces)
fulld (Full name with dots instead of spaces)
first (First name only)"""

# Optional parameters
parser = argparse.ArgumentParser(
    prog = "Name2User",
    description = desc_text,
    formatter_class = argparse.RawTextHelpFormatter
)

# "name" is mandatory is there is no stdin input
if sys.stdin.isatty() is True:
    parser.add_argument("name", help = "Name to generate usernames for")
parser.add_argument("-c", "--conversion", default = UserNameCreationMethods.ALL.value, help = "User name creation conversion mode. Defaults to \"ALL\"")
parser.add_argument("-m", "--mail", default = None, help = "Mail domain. Will be appended to all user names when set")

args = parser.parse_args()

# Exit in error if both positional argument and stdin are empty
if sys.stdin.isatty() is True and hasattr(args, "name") is False:
    print("You must provide a full name as positonal argument or pipe somethin to this program! Exiting.")
    sys.exit()

# Remove first "@" in case mail is provided and user added it
if args.mail is not None and args.mail[0] == "@":
    args.mail = args.mail[1:]

# Main function
def main():
    usernames = []

    # No stdin present, check parameters
    if sys.stdin.isatty() is True:

        # Single name
        if args.name is not None:
            usernames.extend(UserNameGenerator.build_usernames(args.name, args.mail, args.conversion))

    # stdin present
    else:
        for line in sys.stdin:
            usernames.extend(UserNameGenerator.build_usernames(line.rstrip(), args.mail, args.conversion))

    # Print out generated names
    for line in usernames:
        print(line)
