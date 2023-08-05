"""
    Some functions for pdf handlings__

"""
import click
import os

def pages_pdf(inputfile):

    from PyPDF2 import PdfReader

    file = open(inputfile, 'rb')
    pdfReader = PdfReader(file)
    return len(pdfReader.pages)


def create_files(filepath, n, nf, extension):
	"""
	This function takes four inputs and returns tex filenames with proper path 
	
	    filepath -> path to be modified with filename
	    n -> nth of files to be produced
	    nf -> number of files to be produced
        extension -> file extension
	
	    Eg: filepath = "./test/main.tex" -> "./test/main-0.tex, main-1.tex" like that
	"""
	path = filepath.split('.')
	pathinit = filepath.split('/')
	if nf == 1:
	    if pathinit[0] == '.':
	        return '.' + path[len(path)-2] + '.' + extension
	    else:
	        return path[len(path)-2] + '.' + extension
	else:
	    if pathinit[0] == '.':
	        return '.' + path[len(path)-2] + '-' + str(n + 1) +  '.' + extension
	    else:
	        return path[len(path)-2] + '-' + str(n + 1) + '.' + extension
	

def extract_png_pdf(inputfile, first_page, last_page, outputfile, dpi, transparent):
    """
    keyword args:
        inputfile <- Path
        first_page <- Int
        last_page <- Int
        outputfile <- Path
        dpi <- Int
        transparent <- Bool
    """

    from PyPDF2 import PdfReader
    from pdf2image import convert_from_path

    pages = convert_from_path(
            "./{}".format(inputfile), 
            first_page=first_page,
            last_page=last_page,
            dpi=dpi,
            transparent = transparent,
            use_pdftocairo = True,
            thread_count=8
            )
    file = open(inputfile, 'rb')
    pdfReader = PdfReader(file)
    n_pages = len(pdfReader.pages)

    for i in range(first_page, last_page+1):
        file_name = create_files(
                outputfile,
                i-1,
                n_pages,
                'png'
                )
        pages[i-first_page].save(f'{file_name}', 'PNG')
        click.secho(f'\t{os.path.basename(inputfile)} [page {i}] -> {os.path.basename(file_name)}', fg='bright_blue')

