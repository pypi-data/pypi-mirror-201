import click
from playground.constants import PLAYGROUND_FOLDER


def init_project_code_folder(name: str) -> None:
    project_code_folder = PLAYGROUND_FOLDER / "projects" / name
    project_code_folder.mkdir(exist_ok=True)

    for folder in ("data", "features", "notebooks", "configs"):
        (project_code_folder / folder).mkdir(exist_ok=True)
        if folder in ("data", "features"):
            (project_code_folder / folder / "__init__.py").touch()
            (project_code_folder / folder / "tasks.py").touch()

    (project_code_folder / "__init__.py").touch()
    (project_code_folder / "configs" / "data_config.py").touch()
    (project_code_folder / "configs" / "model_config.py").touch()
    (project_code_folder / "workflows.py").touch()
    (project_code_folder / "README.md").touch()


@click.command()
@click.option("--name", type=str)
def new_project(name: str):
    init_project_code_folder(name=name)


@click.group()
def cli():
    pass


cli.add_command(new_project)


if __name__ == "__main__":
    cli()
