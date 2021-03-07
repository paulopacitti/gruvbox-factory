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

    console.print(Panel('🏭 [bold green] Gruvbox Factory [/] 🏭', expand=False, border_style='yellow'))
    console.print('⚠️ WARNING ⚠️\n[italic]make sure you\'re in the same directory of the image you want to convert [/]\n')
    image_file = console.input('🖼️ [bold yellow]Which image do you want to manufacture?[/] ')

    try:
        image = gruvbox_factory.open_image(image_file)
    except:
        console.print('❌ [red]We had a problem in the pipeline! Make sure you\'re in the same path of the image you want to convert! [/]')
        sys.exit(0)
    console.print('🔨 [yellow]manufacturing your gruvbox wallpaper...[/]')
    gruvbox_factory.convert_image(image, save_path=('gruvbox_' + image_file))

    console.print('✅ [bold green]Done![/] [green](saved as gruvbox_' + image_file + ')[/]')

def add_gruvbox_palette():
    current_path = Path(__file__).parent.absolute()
    palette = open(str(current_path) + '/gruvbox.txt', 'r')
    for line in palette.readlines():
        gruvbox_factory.add_color_to_palette(line[:-1])

## handle CTRL + C
def signal_handler(signal, frame):
    print()
    sys.exit(0)

if __name__ == '__main__':
    main()