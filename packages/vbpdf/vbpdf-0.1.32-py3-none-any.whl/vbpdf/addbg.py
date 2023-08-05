
import click
import os
from PIL import Image
from .choice_option import ChoiceOption


bg_path = "/Users/vaibhavblayer/10xphysics/backgrounds/bg_instagram.jpg"
bg_path_parent = "/Users/vaibhavblayer/10xphysics/backgrounds/"


@click.command(
        help="Adds background to any transparent image"
        )
@click.option(
        '-i', 
        '--image', 
        type=click.Path(),
        default="./main.png",
        help="Front Image"
        )
@click.option(
        '-b', 
        '--background', 
        type=click.Choice(['paper_texture', 'pencil_paper']),
        default='paper_texture',
        cls=ChoiceOption,
        help="Background Image"
        )
@click.option(
        '-o',
        '--outputfile',
        type=click.Path(),
        default="./new.png",
        show_default=True,
        help="Output file name"
        )
def addbg(image, background, outputfile):
    bg = background
    background = os.path.join(bg_path_parent, background)
    background = Image.open(background)
    frontImage = Image.open(image)
    frontImage = frontImage.convert("RGBA")
    background = background.convert("RGBA")
    background = background.resize((frontImage.width, frontImage.height))
    width = (background.width - frontImage.width) // 2
    height = (background.height - frontImage.height) // 2
    background.paste(frontImage, (width, height), frontImage)
    background.save(outputfile, format="png")

    click.secho(
            f'\t{os.path.basename(image)} is stacked on {os.path.basename(bg)} -> {os.path.basename(outputfile)}',
            #fg='bright_green'
            )

#    with click.progressbar([1, 2, 3]) as bar:
#        for x in bar:
#            print(f"sleep({x})...")
#            time.sleep(x)







