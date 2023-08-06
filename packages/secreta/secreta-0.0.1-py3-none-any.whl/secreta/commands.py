import json

import typer

from secreta.constants import PASSWORDS_FILE
from secreta.utils import auth_user, decrypt_from_service, encrypt_credentials, get_credentials, input_manager

app = typer.Typer()


@app.command()
def set():
    """Set your secreta access password"""
    access_password = input_manager(access_password=True).get("password")
    d = get_credentials()
    encrypted = encrypt_credentials(access_password)
    d["access_password"] = {"password": encrypted["password"], "key": encrypted["key"]}
    with open(PASSWORDS_FILE, "w") as f:
        json.dump(d, f)
    typer.echo(typer.style("Access password set successfully!", fg=typer.colors.GREEN))


@app.command()
def new():
    """Add new credentials for a service"""
    if not auth_user():
        typer.echo(typer.style("Invalid access password!", fg=typer.colors.RED))
        return
    service, username, password = input_manager().values()
    encrypted = encrypt_credentials(password, username)
    d = get_credentials()
    d[service] = {"username": encrypted["username"], "password": encrypted["password"], "key": encrypted["key"]}
    with open(PASSWORDS_FILE, "w") as f:
        json.dump(d, f)
    typer.echo(typer.style(f"Credentials for {service.capitalize()} set successfully!", fg=typer.colors.GREEN))


@app.command()
def get(service: str):
    """Get credentials for a given service"""
    if not auth_user():
        typer.echo(typer.style("Invalid access password!", fg=typer.colors.RED))
        return
    service = service.lower()
    decrypted = decrypt_from_service(service)
    typer.echo(typer.style(f"Username: {decrypted['username']}", fg=typer.colors.YELLOW))
    typer.echo(typer.style(f"Password: {decrypted['password']}", fg=typer.colors.YELLOW))


@app.command()
def ls():
    """List all credentials added"""
    if not auth_user():
        typer.echo(typer.style("Invalid access password!", fg=typer.colors.RED))
        return
    d = get_credentials()
    if len(d.keys()) == 1:
        typer.echo(typer.style("No credentials added yet!", fg=typer.colors.RED))
    for key in d.keys():
        if key != "access_password":
            typer.echo(typer.style(key.capitalize(), fg=typer.colors.BLUE))


if __name__ == "__main__":
    app()