import string
from random import choice
from typing import LiteralString, Annotated, Final
import keyring
import rich
from rich.console import Console
from rich.table import Table

import hasher
from database import Database
import typer

# TODO: Add duplication check
# TODO: Option to copy password into clipboard
# TODO: Command to get password of a single service

CHARS = string.ascii_letters
SPECIALS: Final[LiteralString] = string.punctuation
DIGITS: Final[LiteralString] = string.digits

app: typer.Typer = typer.Typer(name="pypwgen")


def gen_password(length: int = 8, *, digits: LiteralString | None = DIGITS,
                 specials: LiteralString | None = SPECIALS) -> str:
    """
    Generates a secure password
    :param length: The length of the password
    :param digits: Set to None to disable digits
    :param specials: Set to None to disable special characters
    :return: the generated password
    """
    password: str = ""
    global CHARS
    if digits is not None:
        CHARS += digits

    if specials is not None:
        CHARS += specials

    for _ in range(length):
        password += choice(CHARS)
    return password


def init_table(db: Database):
    db.execute('''create table if not exists passwords(
            id integer primary key autoincrement,
            service text not null, 
            password text not null
        )''')


def hash_password(password: str, master_password: str) -> str:
    hashed = hasher.encrypt_password(password, master_password)
    return str(hashed, "utf-8")


def save_password(password: str, service: str, db: Database) -> None:
    db.execute("insert into passwords(service, password) values(?, ?)", (service, password))


def get_passwords(db: Database) -> list[tuple]:
    return db.fetch_all("select * from passwords")


@app.command(name="init")
def init():
    master_pwd = typer.prompt("Please enter a master password", hide_input=True)
    keyring.set_password("pypwgen", "master", master_pwd)
    rich.print("✅ [green]Master password set successfully[/green]")


@app.command(name="pwgen")
def pypwgen(length: Annotated[int, typer.Option("--length", "-l", help="The length of the password")] = 8,
            service: Annotated[str, typer.Option("--service", "-s", prompt=True, help="The service name")] = "None",
            show: Annotated[bool, typer.Option("--show", help="Show the password after its creation")] = True,
            include_digits: Annotated[
                bool, typer.Option("--include-digits", "-d", help="Consider digits in password generation")] = True,
            include_specials: Annotated[bool, typer.Option("--include-specials", "-s",
                                                           help="Consider special character in password generation")] = True,
            ):
    """
    Generates a password
    """
    database: Database = Database("db.sqlite")
    password: str = gen_password(length, digits=DIGITS if include_digits else None,
                                 specials=SPECIALS if include_specials else None)

    master_pwd: str | None = keyring.get_password("pypwgen", "master")
    if master_pwd is None:
        rich.print("⚠️ [yellow]Please run `pypwgen init` first[/yellow]")
        return

    hashed: str = hash_password(password, master_pwd)
    with database as db:
        init_table(db)
        save_password(hashed, service.strip(), db)
        if show: rich.print(f"✅ [green]Saved password for [yellow]{service}[/yellow]: [red]{password}[/red][/green]")


@app.command(name="view")
def view():
    database = Database("db.sqlite")
    master_pwd = typer.prompt("Please enter your master password", hide_input=True)
    table = Table("Service", "Password")
    console = Console()
    with database as db:
        passwords = get_passwords(db)
        for password in passwords:
            (_, service, pwd) = password
            decrypted_value = hasher.decrypt_password(pwd, master_pwd)
            table.add_row(service, decrypted_value)
    console.print(table)


if __name__ == "__main__":
    app()
