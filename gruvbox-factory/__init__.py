import os
from pathlib import Path
from ImageGoNord import GoNord
from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt
from rich.progress import track

def main():
    console = Console()
    global gruvbox_factory
    gruvbox_factory = GoNord()
    gruvbox_factory.reset_palette()

    add_gruvbox_palette()

    console.print("⚠️ WARNING ⚠️\n[italic]make sure you're in the same directory of the image you want to convert [/]\n")
    image_file = console.input("[bold yellow]Which image do you want to manufacture?[/] ")
    console.print('[yellow]manufacturing your gruvbox wallpaper...[/]')

    current_path = Path(__file__).parent.absolute()
    image = gruvbox_factory.open_image(str(current_path) + '/'+ image_file)
    gruvbox_factory.convert_image(image, save_path=(str(current_path) + '/'+ 'gruvbox_' + image_file))

    console.print("[bold green]Done![/] ")

def add_gruvbox_palette():
    palette = open('gruvbox.txt', "r")
    for line in palette.readlines():
        gruvbox_factory.add_color_to_palette(line[:-1])

if __name__ == '__main__':
    main()