import click

from .split import split
from .overlay import overlay
#from .compress import compress
from .topng import topng
from .addbg import addbg
from .instagram import instagram
#from .blur import blur


CONTEXT_SETTINGS = dict(
        help_option_names = [
            '-h',
            '--help'
        ]
)

@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    pass


#main.add_command(blur)
main.add_command(instagram)
main.add_command(split)
main.add_command(overlay)
main.add_command(topng)
main.add_command(addbg)
#main.add_command(compress)
