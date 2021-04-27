import signal
import argparse
import sys
import os
from pathlib import Path

from ImageGoNord import GoNord

from rich.console import Console
from rich.panel import Panel


def main():

    signal.signal(signal.SIGINT, signal_handler)
    console = Console()

    # Checks if there's an argument
    if len(sys.argv) > 1:
        image_file = fromCommandArgument(console)
    else:
        image_file = fromTui(console)
    process_image(image_file, console)



# Gets the file path from the Argument
def fromCommandArgument(console):

    command_parser = argparse.ArgumentParser(
        description='A simple cli to manufacture a gruvbox themed wallpaper.'
    )
    command_parser.add_argument('Path',
                       metavar='path',
                       type=str,
                       help='The path to the image.')
    args = command_parser.parse_args()

    if args.Path is None:
        console.print('❌ [red]We had a problem in the pipeline! Make sure you\'re in the same path of the image you want to convert! [/]')
        sys.exit(0)
    else:
        return args.Path


# Gets the file path from user input
def fromTui(console):

    console.print(Panel('🏭 [bold green] Gruvbox Factory [/] 🏭', expand=False, border_style='yellow'))
    console.print('⚠️ WARNING ⚠️\n[italic]make sure you\'re in the same directory of the image you want to convert [/]\n')
    return console.input('🖼️ [bold yellow]Which image do you want to manufacture?[/] ')

def process_image(image_file, console):
    gruvbox_factory = GoNord()
    gruvbox_factory.reset_palette()
    add_gruvbox_palette(gruvbox_factory)
    try:
        image = gruvbox_factory.open_image(image_file)
    except:
        console.print('❌ [red]We had a problem in the pipeline! Make sure you\'re in the same path of the image you want to convert or the Path is correct! [/]')
        sys.exit(0)
    console.print('🔨 [yellow]manufacturing your gruvbox wallpaper...[/]')
    

    #TODO: might be a better idea to save the new Image in the same directory the command is being run from
    dirname = os.path.join(os.path.dirname(image_file),'') # Gets the dirname of the file and appends a trailing slash if needed
    filename = os.path.basename(image_file) # Gets the name of the file

    # Resulting save_path
    save_path =  dirname + 'gruvbox_' + filename

    gruvbox_factory.convert_image(image, save_path=(save_path))
    console.print('✅ [bold green]Done![/] [green](saved as ' + save_path + ')[/]')


def add_gruvbox_palette(gruvbox_factory):
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
