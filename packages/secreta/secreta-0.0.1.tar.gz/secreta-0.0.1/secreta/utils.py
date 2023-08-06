import json
import os

import typer
from cryptography.fernet import Fernet

from secreta.constants import PASSWORDS_FILE


def auth_user() -> bool:
    access_password = typer.prompt("Enter your access password", hide_input=True)
    return access_password == decrypt_from_service("access_password").get("password")


def get_credentials() -> dict:
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, "r") as f:
            d = json.load(f)
            return d
    return {}


def encrypt_credentials(password: str, username: str = None) -> dict:
    key = Fernet.generate_key()
    f = Fernet(key)
    data = {}
    data["key"] = key.decode()
    data["password"] = f.encrypt(password.encode()).decode()
    if username:
        data["username"] = f.encrypt(username.encode()).decode()
    return data


def decrypt_from_service(service: str) -> dict:
    d = get_credentials()
    if d == {}:
        return {}
    key = d[service]["key"].encode()
    f = Fernet(key)
    data = {}
    if "username" in d.get(service, {}):
        username = d[service]["username"]
        data["username"] = f.decrypt(username.encode()).decode()
    password = d[service]["password"]
    data["password"] = f.decrypt(password.encode()).decode()
    return data


def input_manager(access_password=False):
    data = {}
    if not access_password:
        service = typer.prompt("Set the service you would like to add").lower()
        username = typer.prompt("Set your username")
        data = {"service": service, "username": username}
    password = typer.prompt("Set your password", hide_input=True)
    confirmed_password = typer.prompt("Confirm your password", hide_input=True)
    while password != confirmed_password:
        typer.echo(typer.style("Error: The two entered values do not match.", fg=typer.colors.RED))
        confirmed_password = typer.prompt("Confirm your password", hide_input=True)
    data["password"] = password
    return data
