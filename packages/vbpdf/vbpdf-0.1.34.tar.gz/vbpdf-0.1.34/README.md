# vbpdf
Install using pip

```sh
pip install vbpdf
```

## Usage
```sh
vbpdf -h
```
```sh
Usage: vbpdf [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  overlay  Annotates any pdf file.
  split    Splits any pdf file.
  topng    Converts pdf pages into pngs
  addbg	   Adds background to pngs.
```

```sh
vbpdf split -h
```
```sh
Usage: vbpdf split [OPTIONS]

  Splits any pdf file.

Options:
  -i, --inputfile PATH            Input file  [default: ./main.pdf]
  -o, --outputfile PATH           Output file  [default: ./main_splited.pdf]
  -p, --pages <INTEGER INTEGER>...
                                  Pages range  [default: 0, 0]
  -h, --help                      Show this message and exit.
  
```

```sh
vbpdf overlay -h
```

```sh
Usage: vbpdf overlay [OPTIONS]

  Annotates any pdf file.

Options:
  -i, --inputfile PATH            Input file  [default: ./main.pdf]
  -o, --outputfile PATH           Output file  [default: ./main_annotated.pdf]
  -s, --size                      For checking size of the pdf
  -t, --text TEXT                 Text to be placed  [default: Hello Sir!]
  -p, --position <INTEGER INTEGER INTEGER INTEGER>...
                                  Coordintes of the tex box  [default: 0, 0,
                                  100, 100]
  -f, --foreground_color TEXT     Foreground Color  [default: 000000]
  -b, --background_color TEXT     Background Color  [default: ffffff]
  -F, --font TEXT                 Font type  [default: Courier]
  --font_size INTEGER             Font size  [default: 24]
  -h, --help                      Show this message and exit.

```

```sh
vbpdf topng -h
```
```sh
Usage: vbpdf topng [OPTIONS]

  Converts pdf pages into pngs

Options:
  -i, --inputfile PATH            Input file name  [default: ./main.pdf]
  -o, --outputfile PATH           Output file name  [default: ./main.png]
  -d, --dpi INTEGER               DPI -> density per inch for png  [default:
                                  320]
  -t, --transparent               Use this flag for transparent png
  -r, --ranges <INTEGER INTEGER>...
                                  Page range to be converted into png
                                  [default: 1, 1]
  -p, --pages                     Shows no of pages in a pdf file
  -h, --help                      Show this message and exit.

```
