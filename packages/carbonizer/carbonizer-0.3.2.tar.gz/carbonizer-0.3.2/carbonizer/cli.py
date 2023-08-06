import enum
import pathlib
import typing
import asyncio

import typer

from carbonizer import utils, carbon, clipboard

app = typer.Typer()


class Theme(str, enum.Enum):
    one_light = "one-light"
    one_dark = "one-dark"
    monokai = "monokai"
    night_owl = "night_owl"

async def wrap_carbonizer(file, exclude, output_folder, rgba, font):
    output = output_folder / ("carbonized_" + file.stem + ".png")
    carbonizer = carbon.Carbonizer(input_file=file,
                                   output_file=output,
                                   exclude=exclude,
                                   background=rgba,
                                   font=font)
    await carbonizer()
    return output

@app.command()
def carbonize(
        walk: bool = typer.Option(False, "--walk", "-w"),
        input: pathlib.Path =typer.Argument("."),
        theme: Theme = typer.Option(..., "--theme", "-t"),
        glob_pattern: str = typer.Option("*", "--glob", "-g"),
        output_folder: pathlib.Path = typer.Option(".", "--output-folder", "-o"),
        exclude: str = typer.Option("__pychache__*", "--exclude", "--filter", "-e"),
        copy: bool = typer.Option(False, "--copy", "-c"),
        rgbs: str = typer.Option("0:0:0:0", "--rgbs","--background", help="background in rgba seperated with ':'"),
        dry_run: bool = typer.Option(False, "--dry-run",)
):
    # TODO: Refactor to comply SRP
    files: typing.Iterable[pathlib.Path]
    outputs: typing.List[pathlib.Path]

    if not input.exists():
        typer.echo(f"No such file or directory - {input}")
        raise typer.Exit()

    if input.is_file():
        files = [input]
    elif walk:
        files = input.rglob(glob_pattern)
    else:
        files = input.glob(glob_pattern)

    output_folder.mkdir(exist_ok=True)
    rgba = utils.RGBA(*[int(x) for x in rgbs.split(":")])
    outputs = gather_carbonized_code(files, exclude,output_folder,rgba,theme.value)

    if copy:
        file = outputs[-1]
        clipboard.Clipboard().copy(file)
        file.unlink()


def gather_carbonized_code(files, exclude, output_folder, rgba, theme) -> list[pathlib.Path]:
    res = []
    for file in files:
        out = asyncio.run(wrap_carbonizer(file,
                              exclude,
                              output_folder,
                              rgba,
                              theme))
        res.append(out)
    return res



if __name__ == "__main__":
    typer.run(carbonize)
