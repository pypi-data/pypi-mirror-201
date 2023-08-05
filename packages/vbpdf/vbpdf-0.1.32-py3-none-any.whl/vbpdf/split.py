import click
import os
import time

from PyPDF2 import PdfReader, PdfWriter


@click.command(
        help="Splits any pdf file."
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
        default='./main_splited.pdf',
        show_default=True,
        help="Output file"
        )
@click.option(
        '-p',
        '--pages',
        type=click.Tuple([int, int]),
        default=(0, 0),
        show_default=True,
        help="Pages range"
        )
def split(inputfile, outputfile, pages):

    inputpdf = open(inputfile, 'rb')
    reader = PdfReader(inputpdf)

    writer = PdfWriter()
    for i in range(pages[0], pages[1]+1):
        writer.add_page(reader.pages[i-1])
    with open(outputfile, 'wb') as outputpdf:
        writer.write(outputpdf)

