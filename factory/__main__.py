import argparse
import signal
import sys
from os import getcwd, listdir
from os.path import basename, dirname, expanduser, isdir, join, split
from pathlib import Path

from ImageGoNord import GoNord
from rich.console import Console
from rich.panel import Panel


def main():
    signal.signal(signal.SIGINT, signal_handler)
    console = Console()
    args = fromCommandArgument(console)

    gruvbox_factory = GoNord()
    gruvbox_factory.reset_palette()

    # Checks if there's an argument
    if len(sys.argv) > 2:
        image_paths = args.images
        add_gruvbox_palette(gruvbox_factory, args.palette)
    else:
        image_paths, palette = fromTui(console)
        if palette == None:
            return
        add_gruvbox_palette(gruvbox_factory, palette)

    for image_path in image_paths:
        folder, file = split(image_path)
        if file == "*":
            subfolder = join(dirname(split(image_path)[0]), split(folder)[1])
            # assert that image_path is a folder that can be iterated through
            if isdir(subfolder):
                for i in listdir(folder):
                    # TODO: make a check to see that 'i' ends with png, jpg, etc ...
                    process_image(join(subfolder, i), console, gruvbox_factory)
                continue
            else:
                console.print(
                    f"❌ [red]We had a problem in the pipeline! \n'{split(folder)[1]}' is not a folder that can be iterated through! \nSkipping... [/]"
                )
                continue
        elif isdir(image_path):
            console.print(
                f"⏭️ [yellow]We had a problem in the pipeline! \nSkipping {split(folder)[1]}... [/]"
            )
            continue
        process_image(image_path, console, gruvbox_factory)


# Gets the file path from the Argument
def fromCommandArgument(console):
    command_parser = argparse.ArgumentParser(
        description="A simple cli to manufacture gruvbox themed wallpapers."
    )

    command_parser.add_argument(
        "-p",
        "--palette",
        choices=["white", "pink"],
        nargs="?",
        default="pink",
        type=str,
        help="choose your palette, panther 'pink' (default) or snoopy 'white'",
    )
    command_parser.add_argument(
        "-i", "--images", nargs="+", type=str, help="path(s) to the image(s)."
    )

    args = command_parser.parse_args()
    return args


# Gets the file path from user input
def fromTui(console):
    console.print(
        Panel(
            "🏭 [bold green] Gruvbox Factory [/] 🏭", expand=False, border_style="yellow"
        )
    )

    image_paths = [
        expanduser(path)
        for path in console.input(
            "🖼️ [bold yellow]Which image(s) do you want to manufacture? (image paths separated by spaces):[/] "
        ).split()
    ]
    palette = console.input(
        "🎨 [bold yellow]Which palette do you prefer? (panther 'pink' or snoopy 'white'):[/] "
    )
    if palette not in ["pink", "white"]:
        console.print(
            f"❌ [red]We had a problem in the pipeline! \nThe palette you chose is not available! \nShuting down... [/]"
        )
        palette = None

    return (image_paths, palette)


def process_image(image_path, console, gruvbox_factory):
    image = gruvbox_factory.open_image(image_path)

    console.print(f"🔨 [yellow]manufacturing '{basename(image_path)}'...[/]")

    save_path = join(dirname(image_path), "gruvbox_" + basename(image_path))

    gruvbox_factory.convert_image(image, save_path=(save_path))
    console.print(f"✅ [bold green]Done![/] [green](saved at '{save_path}')[/]")


def add_gruvbox_palette(gruvbox_factory, palette):
    current_path = Path(__file__).parent.absolute()
    file_name = f"gruvbox-{palette}.txt"

    with open(join(current_path, file_name), "r") as f:
        for line in f.readlines():
            gruvbox_factory.add_color_to_palette(line[:-1])


## handle CTRL + C
def signal_handler(signal, frame):
    print()
    sys.exit(0)


if __name__ == "__main__":
    main()
