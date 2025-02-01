import argparse
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from signal import SIGINT, Signals, signal
from types import FrameType
from typing import Any, Literal

import ImageGoNord
from pick import pick
from PIL.Image import Image as PilImage
from PIL.ImageFile import ImageFile
from rich import console, panel

Palette = Literal["pink", "white", "mix"]
Image = str
Images = list[Image]


@dataclass
class Arguments:
    palette: Palette | None
    images: list[Image] = field(default_factory=list[Image])


class Parser(argparse.ArgumentParser):

    def __init__(self) -> None:
        super().__init__(
            description="A simple cli to manufacture Gruvbox themed wallpapers.",
            prefix_chars="-",
            argument_default=None,
            conflict_handler="error",
        )

        self.add_argument(
            "-p",
            "--palette",
            choices=["white", "pink", "mix"],
            nargs="?",
            default="pink",
            const="pink",
            help="choose your palette, panther 'pink' (default), snoopy 'white' or smooth 'mix'",
        )
        self.add_argument(
            "-i", "--images", nargs="+", type=str, help="path(s) to the image(s)."
        )

        self._parsed_args: argparse.Namespace  # type: ignore
        self.arguments: Arguments  # type: ignore

    def parse(self) -> None:
        self._parsed_args = self.parse_args()
        self.arguments = Arguments(
            palette=self._parsed_args.palette, images=self._parsed_args.images
        )


def is_palette(value: str | None) -> bool:
    return value in {"pink", "white", "mix"}


def signal_handler(signum: int, _frame: FrameType | None = None) -> None:
    if signum == Signals.SIGINT:
        sys.exit(2)


class Console(console.Console):
    def __init__(self) -> None:
        super().__init__()

    def print_title(self) -> None:
        self.print(
            panel.Panel(
                "🏭 [bold green] Gruvbox Factory [/] 🏭",
                expand=False,
                border_style="yellow",
            )
        )


def select_palette() -> Palette:
    prompt: str = (
        "🎨 [bold yellow]Palette (panther 'pink', snoopy 'white' or smooth 'mix'):[/] "
    )
    options: list[str] = ["pink", "white", "mix"]

    value: Any = pick(options, title=prompt, clear_screen=False)
    _, selection = value

    return selection if is_palette(selection) else "white"


@dataclass
class Factory(ImageGoNord.GoNord):
    def __init__(self) -> None:
        super().__init__()
        self.image_paths: list[str] = []
        self.reset_palette()


class GruvboxFactory:
    def __init__(self) -> None:
        _ = signal(SIGINT, signal_handler)
        self.console: Console = Console()
        self.parser: Parser = Parser()
        self.factory: Factory = Factory()

    def get_palette(self) -> Palette:
        palette: Palette | None = self.parser.arguments.palette
        palette = palette if palette is not None else select_palette()
        if is_palette(palette):
            return palette
        raise Exception("This is unreachable.")

    def add_palette(self, palette: str) -> None:
        cwd: Path = Path(__file__).parent.absolute()
        path: Path = cwd / f"gruvbox-{palette}.txt"
        colors: list[str] = []

        try:
            with open(path) as fd:
                colors = fd.read().splitlines()
        except FileNotFoundError:
            self.console.print(f"❌ [red]Palette file {path} not found.[/]")
            sys.exit(1)

        for color in colors:
            self.factory.add_color_to_palette(color)

        return None

    def select_paths(self) -> list[str]:
        prompt: str = "🖼️ [bold yellow]Image paths (separated by spaces):[/] "
        user_input = self.console.input(prompt)
        paths: list[str] = []
        for raw_path in user_input.split():
            path = Path(os.path.expanduser(raw_path))
            if "*" in raw_path:
                paths.extend(
                    [str(p) for p in path.parent.glob(path.name) if p.is_file()]
                )
            elif path.exists() and path.is_file():
                paths.append(str(path))
            else:
                self.console.print(f"❌ [red]Skipping {raw_path} (not a valid file)[/]")
        return paths

    def write_image_color(self, path: str) -> None:
        image: PilImage | ImageFile = self.factory.open_image(path)
        parent = os.path.dirname(path)
        base = os.path.basename(path)
        dest = os.path.join(parent, f"gruvbox_{base}")

        self.console.print(f"🔨 [yellow]manufacturing '{base}' -> {dest}[/]")
        self.factory.convert_image(image, save_path=dest, parallel_threading=True)
        self.console.print(f"✅ [bold green]Done![/] [green](saved to '{dest}')[/]")

    def process_images(self, images: Images) -> bool:
        failed = 0
        passed = 0
        for path in images:
            if os.path.exists(path) and os.path.isfile(path):
                self.write_image_color(path)
                passed += 1
            else:
                self.console.print(f"❌ [red]Skipping {path} (file not found) [/]")
                failed += 1

        succeeded: bool = failed == 0
        if succeeded:
            self.console.print("🎉 [bold green]All images processed successfully![/]")
        elif failed and passed:
            self.console.print("🎉 [bold orange]Some images processed successfully![/]")
        else:
            self.console.print("🎉 [bold red]Couldn't process any images[/]")
            return False
        return True


def main() -> None:

    factory = GruvboxFactory()

    factory.parser.parse()
    image_paths = factory.parser.arguments.images

    if len(sys.argv) < 2:
        sys.exit(factory.parser.print_help())

    palette = factory.get_palette()
    factory.add_palette(palette)

    if factory.process_images(image_paths) is not True:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
