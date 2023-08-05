
import click
import os
import sys
import PyPDF2
import time
from rich.console import Console
from .functions_pdf import pages_pdf
from .functions_pdf import extract_png_pdf



@click.command(
        help="Converts pdf pages into pngs"
        )
@click.option(
        '-i',
        '--inputfile',
        type=click.Path(),
        default="./main.pdf",
        show_default=True,
        help="Input file name"
        )
@click.option(
        '-o',
        '--outputfile',
        type=click.Path(),
        default="./main.png",
        show_default=True,
        help="Output file name"
        )
@click.option(
        '-d',
        '--dpi',
        default=320,
        type=click.INT,
        show_default=True,
        help="DPI -> density per inch for png"
        )
@click.option(
        '-t',
        '--transparent',
        is_flag=True,
        default=False,
        show_default=True,
        help="Use this flag for transparent png"
        )
@click.option(
        '-r',
        '--ranges',
        nargs=2,
        default=([1, 1]),
        type=click.Tuple([int, int]),
        show_default=True,
        help="Page range to be converted into png"
        )
@click.option(
        '-p',
        '--pages',
        default=False,
        is_flag = True,
        show_default=True,
        help="Shows no of pages in a pdf file"
        )
def topng(inputfile, outputfile, dpi, transparent, ranges, pages):
    mydict = {
            'inputfile': inputfile,
            'first_page': ranges[0],
            'last_page': ranges[1],
            'outputfile': outputfile,
            'dpi': dpi,
            'transparent': transparent
            }

    time_init = int(time.strftime('%s'))
    if pages == True:
        n_pages = pages_pdf(inputfile)
        print(f'Total number of pages is {n_pages}')
    else:
        console = Console(width=50)
        with console.status("Processing ...", spinner="dots"):
            extract_png_pdf(**mydict)
        time_finish = int(time.strftime('%s'))
        #print(f'Took {time_finish - time_init} seconds to do it')



