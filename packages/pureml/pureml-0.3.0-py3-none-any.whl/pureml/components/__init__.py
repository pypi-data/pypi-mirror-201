import os, json
from pureml.schema import PathSchema

path_schema = PathSchema().get_instance()


def get_token():
    """It checks if the token exists in the user's home directory. If it does, it returns the token. If it
    doesn't, it returns None

    Returns
    -------
        The token is being returned.
    """
    path = path_schema.PATH_USER_TOKEN
    # path = os.path.expanduser(path)

    if os.path.exists(path):
        creds = open(path, "r").read()

        creds_json = json.loads(creds)
        token = creds_json["accessToken"]
        # print(f"[bold green]Authentication token exists!")

        # print(token)
        return token
    else:
        print(f"[bold red]Authentication token doesnot exist! Please login")

        return


def get_org_id():
    """It checks if the org exists in the user's home directory. If it does, it returns the org. If it
    doesn't, it returns None

    Returns
    -------
        The org is being returned.

    """

    path = path_schema.PATH_USER_TOKEN

    path = os.path.expanduser(path)

    if os.path.exists(path):
        creds = open(path, "r").read()

        creds_json = json.loads(creds)

        org_id = creds_json["org_id"]
        # print(f"[bold green]Organization exists!")

        # print(org_id)
        return org_id
    else:
        print(f"[bold red]Organization token doesnot exist! Please login")

        return


def convert_values_to_string(logged_dict):

    for key in logged_dict:
        logged_dict[key] = str(logged_dict[key])

    return logged_dict
