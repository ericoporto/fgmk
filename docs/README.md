# Docs on docs

If you are looking for the FGMK documentation, 
[you can read it here](Markdown/index.md).


## Building the documentation

The docs should be written in Markdown, inside the Markdown folder.

When updated, just run the script `make_all_docs.sh`.


## How it works

This script will create rst files, place them in the `source` folder and then
fix the links (switching .md to .html) and then it will use **Sphinx** to
generate the html files. The html files are going to be used in the webpage.

After it will use **Sphinx** again to generate the QtHelp file to be used inside
FGMK itself.


# Dependencies

The script requires: sphinx (python3) and pandoc installed.
