import os
from ImageGoNord import GoNord

gruvbox_factory = GoNord()
gruvbox_factory.reset_palette()

path = os.getcwd()
gruvbox_factory.set_palette_lookup_path(path)

palette = open('gruvbox.txt', "r")
for line in palette.readlines():
  gruvbox_factory.add_color_to_palette(line[:-1]) 

image_file = input("wich image do you want to convert? ")
print('converting...')
image = gruvbox_factory.open_image(image_file)
gruvbox_factory.convert_image(image, save_path=('gruvbox_' + image_file))