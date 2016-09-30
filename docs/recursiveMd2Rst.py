#!/usr/bin/env python

'''
Recursively and destructively creates a .rst file for all Markdown
files in the target directory and below.

Created to deal with PyPa without changing anything in setup based on
the idea that getting proper Markdown support later is worth waiting
for rather than forcing a pandoc dependency in sample packages and such.

Vote for
(https://bitbucket.org/pypa/pypi/issue/148/support-markdown-for-readmes)

'''

import sys, os, re

markdown_sufs = ('.md','.markdown','.mkd')
markdown_regx = '\.(md|markdown|mkd)$'

target = 'Rst'

md_files = []
for root, dirnames, filenames in os.walk(target):
    for name in filenames:
        if name.endswith(markdown_sufs):
            md_files.append(os.path.join(root, name))

for md in md_files:
    bare = re.sub(markdown_regx,'',md)
    cmd='pandoc --from=markdown --to=rst "{}" -o "{}.rst"'
    print(cmd.format(md,bare))
    os.system(cmd.format(md,bare))
    os.remove(md)
