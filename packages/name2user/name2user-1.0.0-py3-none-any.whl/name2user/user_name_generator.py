from .user_name_creation_methods import UserNameCreationMethods

class UserNameGenerator:

    # Function for building the user names
    def build_usernames(full_name, mail, conversion):
        usernames = []
        def add(username):
            if mail is not None:
                username += f"@{mail}"
            usernames.append(username)

        # Last name only
        if conversion == UserNameCreationMethods.ALL.value or conversion == UserNameCreationMethods.LAST.value:
            username = f"{full_name.split(' ')[-1]}".lower()
            add(username)

        # First letter of first name + last name
        if conversion == UserNameCreationMethods.ALL.value or conversion == UserNameCreationMethods.FLAST.value:
            username = f"{full_name[0]}{full_name.split(' ')[-1]}".lower()
            add(username)

        # First letter of first name + "." + last name
        if conversion == UserNameCreationMethods.ALL.value or conversion == UserNameCreationMethods.FDLAST.value:
            username = f"{full_name[0]}.{full_name.split(' ')[-1]}".lower()
            add(username)

        # Full name without space
        if conversion == UserNameCreationMethods.ALL.value or conversion == UserNameCreationMethods.FULL.value:
            username = f"{''.join(full_name.split(' '))}".lower()
            add(username)

        # Full name with dot
        if conversion == UserNameCreationMethods.ALL.value or conversion == UserNameCreationMethods.FULLD.value:
            username = f"{full_name.replace(' ', '.')}".lower()
            add(username)

        # First name
        if conversion == UserNameCreationMethods.ALL.value or conversion == UserNameCreationMethods.FIRST.value:
            username = f"{full_name.split(' ')[0]}".lower()
            add(username)

        return usernames