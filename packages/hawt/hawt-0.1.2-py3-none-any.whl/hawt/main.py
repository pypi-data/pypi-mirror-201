import typer
from hawt import identity_center

app = typer.Typer()
app.add_typer(identity_center.app, name="identitycenter")


@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")


def typer_main():
    app()
