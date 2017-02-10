import getpass


def get_username_and_password(msg):
    print(msg)
    un = raw_input("Username: ")
    pw = getpass.getpass("Password: ")
    return un, pw