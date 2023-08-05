import click

from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import AnnotationBuilder



@click.command(
        help="Annotates any pdf file."
        )
@click.option(
        '-i',
        '--inputfile',
        type=click.Path(),
        default='./main.pdf',
        show_default=True,
        help="Input file",
        )
@click.option(
        '-o',
        '--outputfile',
        type=click.Path(),
        default='./main_annotated.pdf',
        show_default=True,
        help="Output file"
        )
@click.option(
        '-s',
        '--size',
        is_flag=True,
        default=False,
        show_default=True,
        help="For checking size of the pdf"
        )
@click.option(
        '-t',
        '--text',
        type=click.STRING,
        default="Hello Sir!",
        show_default=True,
        help="Text to be placed"
        )
@click.option(
        '-p',
        '--position',
        type=click.Tuple([int, int, int, int]),
        default=(0, 0, 100, 100),
        show_default=True,
        help="Coordintes of the tex box"
        )
@click.option(
        '-f',
        '--foreground_color',
        default='000000',
        show_default=True,
        help='Foreground Color'
        )
@click.option(
        '-b',
        '--background_color',
        default='ffffff',
        show_default=True,
        help='Background Color'
        )
@click.option(
        '-F',
        '--font',
        default="Courier",
        type=click.STRING,
        show_default=True,
        help="Font type"
        )
@click.option(
        '--font_size',
        default=24,
        show_default=True,
        help='Font size'
        )
def overlay(inputfile, outputfile, size, text, font, position, foreground_color, background_color, font_size):

    inputpdf = open(inputfile, 'rb')
    reader = PdfReader(inputpdf)
    if size:
        for i in enumerate(reader.pages):
            w = i[1].artbox.width
            h = i[1].artbox.height
            print(f'Page: {i[0]+1} \t Height: {h} \t Width: {w}')

    else:
        writer = PdfWriter()
        text_box = AnnotationBuilder.free_text(
                text,
                rect=position,
                font="Courier",
                font_size=str(font_size)+'pt',
                font_color=foreground_color,
                border_color=foreground_color,
                background_color=background_color
                )

        rectangle_box = AnnotationBuilder.rectangle(
                rect=position,
                interiour_color=background_color,
                )
    
        for page in enumerate(reader.pages):
            writer.add_page(page[1])
            writer.add_annotation(page_number=page[0], annotation=text_box)
        with open(outputfile, 'wb') as outputpdf:
            writer.write(outputpdf)
