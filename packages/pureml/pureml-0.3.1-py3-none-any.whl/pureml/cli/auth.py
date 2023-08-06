import os
from pathlib import Path
import socket
from time import sleep, time
from typing import Optional
import jwt
import requests
import typer
from rich import print
from rich.syntax import Syntax
from .orgs import select
from rich.progress import Progress, SpinnerColumn, TextColumn
from pureml.components import get_org_id, get_token
from rich.console import Console
from rich.table import Table
from urllib.parse import urljoin
import json
from pureml.schema import BackendSchema, PathSchema
import platform
import ipapi


path_schema = PathSchema().get_instance()
backend_schema = BackendSchema().get_instance()
app = typer.Typer()


def save_auth(org_id: str = None, access_token: str = None, email: str = None):
    token_path = path_schema.PATH_USER_TOKEN

    token_dir = os.path.dirname(token_path)
    os.makedirs(token_dir, exist_ok=True)

    # Read existing token
    if os.path.exists(token_path):
        with open(token_path, "r") as token_file:
            token = json.load(token_file)

        if org_id is not None:
            token["org_id"] = org_id
        if access_token is not None:
            token["accessToken"] = access_token
        if email is not None:
            if "email" in token and token["email"] != email:
                token["org_id"] = ""
            token["email"] = email
    else:
        token = {"org_id": org_id, "accessToken": access_token, "email": email}
        if org_id is None:
            token["org_id"] = ""

    token = json.dumps(token)

    with open(token_path, "w") as token_file:
        token_file.write(token)


@app.command()
def details():
    token = get_token()
    org_id = get_org_id()

    print("Org Id: ", org_id)
    print("Access Token: ", token)


@app.callback()
def callback():
    """
    Authentication user command

    Use with status, signup, login or logout option

    status - Checks current authenticated user
    signup - Creates new user
    login - Logs in user
    logout - Logs out user
    """


@app.command()
def signup(backend_url: str = typer.Option("", "--backend-url", "-b", help="Backend URL for self-hosted or custom pureml backend instance")):
    print("\nCreate a new account/\n")
    email: str = typer.prompt("Enter new email")
    handle: str = typer.prompt("Enter new user handle")
    name: str = typer.prompt("Enter new user name")
    password: str = typer.prompt(
        "Enter new password", confirmation_prompt=True, hide_input=True
    )
    # organization_id: str = typer.prompt("Enter Organization id")
    # data = {"email": email, "password": password, "org": organization_id}
    data = {"email": email, "password": password, "handle": handle, "name": name}

    url_path_1 = "user/signup"
    base_url = backend_schema.BASE_URL if backend_url == "" else backend_url
    url = urljoin(base_url, url_path_1)

    response = requests.post(url, json=data)

    if not response.ok:
        print(f"[red]Could not create account! Please try again later")
        return
    print(
        f"[green]Successfully created your account! You can now login using ```pure auth login```"
    )


def list_org(access_token: str, base_url: str):

    url_path = "org"
    url = urljoin(base_url, url_path)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(access_token),
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        print()
        print("[green]Select the Organization from the list below!")
        org_all = response.json()["data"]

        console = Console()

        table = Table("Organization Id", "Organization Handle")
        for org in org_all:
            table.add_row(org["org"]["uuid"], org["org"]["handle"])

        console.print(table)
        print()

    else:
        print("[red]Unable to fetch existing Organizations!")


def check_org_status(access_token: str, base_url: str):

    org_id: str = typer.prompt("Enter your Org Id")

    url_path = "org/id/{}".format(org_id)
    url = urljoin(base_url, url_path)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(access_token),
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        # print("[green]Organization Exists!")
        return org_id
    else:
        print("[red]Organization does not Exists!")
        return None


def get_location():
    try:
        response = ipapi.location(output="json")
    except:
        try:
            # print("Getting device details...")
            response = requests.get(f'https://api64.ipify.org?format=json').json()
            response = requests.get(f"https://ipapi.co/{response['ip']}/json/", headers={
                    "User-Agent": "pureml-cli"
                }).json()
        except:
            response = {
                "ip": socket.gethostbyname(socket.gethostname()),
                "city": "Unknown",
                "region": "Unknown",
                "country": "Unknown",
            }
    location_data = {
        "ip": response["ip"] or socket.gethostbyname(socket.gethostname()),
        "city": response["city"] or "Unknown",
        "region": response["region"] or "Unknown",
        "country": response["country_name"] or "Unknown",
    }
    return location_data

@app.command()
def login(
    backend_url: str = typer.Option("", "--backend-url", "-b", help="Backend URL for self-hosted or custom pureml backend instance"),
    frontend_url: str = typer.Option("", "--frontend-url", "-f", help="Frontend URL for self-hosted or custom pureml frontend instance"),
    browserless: bool = typer.Option(False, "--browserless", "-s", help="Browserless login for ssh or pipelines"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Login with email and password interactively"),
    ):

    base_url = backend_schema.BASE_URL if backend_url == "" else backend_url
    frontend_base_url = backend_schema.FRONTEND_BASE_URL if frontend_url == "" else frontend_url
    # Interactive login with email and password
    if interactive:
        print(f"\n[Enter your credentials to login[/\n")
        email: str = typer.prompt("Enter your email")
        password: str = typer.prompt("Enter your password", hide_input=True)
        data = {"email": email, "password": password}

        url_path = "user/login"
        url = urljoin(base_url, url_path)

        response = requests.post(url, json=data)

        if response.ok:
            token = response.text
            token = json.loads(token)["data"][0]

            access_token = token["accessToken"]
            email = token["email"]

            save_auth(access_token=access_token, email=email)

            print(f"[green]Successfully logged in as {email}!")

            # Select organization
            org_id = select()
            if org_id is not None:
                save_auth(org_id=org_id, access_token=access_token, email=email)
                print(f"[green]Successfully linked to organization {org_id}!")
            else:
                print(f"[red]Organization details not found! Please contact your admin to add you to an organization!")

        else:
            print(f"[red]Unable to login to your account!")
    
    # Browser based login
    else:
        # Get device details
        device = platform.platform()
        device_data = get_location()
        device_id = device_data["ip"]
        device_location = device_data["city"] + ", " + device_data["region"] + ", " + device_data["country"]

        # Create session
        device_data = {
            "device": device,
            "device_id": device_id,
            "device_location": device_location
        }
        url_path = "user/create-session"
        url = urljoin(base_url, url_path)

        # print(device_data)
        response = requests.post(url, json=device_data)

        if not response.ok:
            print(f"[red]Unable to create session! Please try again later")
            return
        
        session_id = response.json()["data"][0]["session_id"]

        # Generater link & Open browser
        link = urljoin(frontend_base_url, f"verify-session/{session_id}")

        if browserless:
            print(f"Please open the following link in your browser to login: [underline]{link}[/underline]")
        else:
            # Open browser
            print(f"Opening the browser : [underline]{link}[/underline]")
            typer.launch(link)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Waiting for response...", total=None)
            # Hit the endpoint to check if the session is verified
            start_time = time()
            while True:
                url_path = "user/session-token"
                url = urljoin(base_url, url_path)
                data = {
                    "session_id": session_id,
                    "device_id": device_id,
                }
                # print(data)
                response = requests.post(url, json=data)
                # print("Hit API response ", response.text)
                if response.ok:
                    token = response.text
                    token = json.loads(token)["data"][0]

                    access_token = token["accessToken"]
                    email = token["email"]

                    save_auth(access_token=access_token, email=email)

                    break
                else:
                    if response.status_code == 404:
                        print(f"[red]Session not found! Please try again later")
                        return
                    elif response.status_code == 403:
                        print(f"[red]Session expired or invalid device! Please try again later")
                        return

                if time() - start_time > 60 * 10:
                    print(f"[red]Session timed out!")
                    return
                
                sleep(1)
        print(f"[green]Successfully logged in as {email}!")
        
        # Select organization
        org_id = select()
        if org_id is not None:
            save_auth(org_id=org_id, access_token=access_token, email=email)
            print(f"[green]Successfully linked to organization {org_id}!")
        else:
            print(f"[red]Organization details not found! Please contact your admin to add you to an organization!")



# @app.command()
# def status():
#     print()
#     path = PATH_USER_TOKEN

#     curr_path = Path(__file__).parent.resolve()
#     if os.path.exists(path):
#         token = open(path, "r").read()
#         public_key = open(f"{curr_path}/public.pem", "rb").read()
#         payload = jwt.decode(token, public_key, algorithms=["RS256"])
#         print(f"[green]You are currently logged in as {payload['email']}")
#     else:
#         print("[red]You are not logged in!")


def statusHelper():
    path = path_schema.PATH_USER_TOKEN

    if os.path.exists(path):
        return open(path, "r").read()
    else:
        return None


def auth_validate():
    token = statusHelper()
    if not token:
        print("[red]You are not logged in!")
        raise typer.Exit()
    return token


# @app.command()
# def logout():
#     print()
#     path = PATH_USER_TOKEN

#     if os.path.exists(path):
#         os.remove(path)
#         print(f"[yellow]Successfully logged out!")
#     else:
#         print(f"[red]You are not logged in!")

if __name__ == "__main__":
    app()
