import os
import signal
import sys
from pathlib import Path

from ImageGoNord import GoNord

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt
from rich.progress import track


def main():
    signal.signal(signal.SIGINT, signal_handler)
    console = Console()

    global gruvbox_factory
    gruvbox_factory = GoNord()
    gruvbox_factory.reset_palette()
    add_gruvbox_palette()

    # Parse arguments / input as a list
    if len(sys.argv) == 1:
        console.print(
            Panel(
                "🏭 [bold green] Gruvbox Factory [/] 🏭",
                expand=False,
                border_style="yellow",
            )
        )
        image_paths = console.input("🖼️ [bold yellow]Which image do you want to manufacture?[/]").split()
    else:
        image_paths = sys.argv[1:]

    # Convert each image to gruvbox colors
    for image_path in image_paths:
        try:
            image = gruvbox_factory.open_image(image_path)
        except:
            console.print(
                f"❌ [red]We had a problem in the pipeline! Make sure your picure can be found at '{image_path}'! [/]"
            )
            sys.exit(1)
        console.print(f"🔨 [yellow]manufacturing gruvbox wallpaper '{image_path}'...[/]")
        gruvbox_factory.convert_image(
            image,
            save_path=(
                os.path.join(
                    os.path.dirname(image_path),
                    "gruvbox_" + os.path.basename(image_path),
                )
            ),
        )

        console.print(
            "✅ [bold green]Done![/] [green](saved as gruvbox_"
            + os.path.basename(image_path)
            + ")[/]"
        )


def add_gruvbox_palette():
    current_path = Path(__file__).parent.absolute()
    palette = open(str(current_path) + "/gruvbox.txt", "r")
    for line in palette.readlines():
        gruvbox_factory.add_color_to_palette(line[:-1])


## handle CTRL + C
def signal_handler(signal, frame):
    print()
    sys.exit(0)


if __name__ == "__main__":
    main()
