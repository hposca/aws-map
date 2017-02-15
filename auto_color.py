#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import fileinput
import os
import re
import subprocess

# Full list of colors in:
# http://www.graphviz.org/doc/info/colors.html
colors = ['darkolivegreen2', 'cadetblue2', 'gold2', 'coral1', 'hotpink2', 'royalblue2']

def colorize(dotfile, nodes):
    colorizes_dotfile = dotfile + '.colorized'
    output_script = 'colorize-{}.sh'.format(dotfile)

    with open(output_script, 'w') as outfile:
        outfile.write("#!/usr/bin/env bash\n\n")
        outfile.write("cp {} {}\n\n".format(dotfile, colorizes_dotfile))

        with open(dotfile, 'r') as infile:
            for node in nodes:
                color = colors[nodes.index(node)]

                elements = [ node ]

                for element in elements:
                    if not element.startswith('subnet'):
                        text = 'sed -i "s/\({} -> [a-zA-Z0-9_]*\) ;/\\1 [penwidth=7;color={}] ;/" {}\n'.format(element, color, colorizes_dotfile)
                        outfile.write(text)

                        for line in infile:
                            next_elem_regex = re.compile('{} -> ([a-zA-Z0-9_]*) ;'.format(element))
                            match_result = next_elem_regex.search(line)
                            if match_result:
                                next_element = match_result.group(1)
                                if not next_element in elements:
                                    elements.append(next_element)

                        infile.seek(0,0)
                outfile.write('\n')
    os.chmod(output_script, 0o755)

def parse_arguments():
    description = '''Program created to get a generated dotfile, which represents
an AWS infrastructure, and colorize paths starting from the given node.'''

    epilog = '''After execution this script will generate a colorize-DOTFILE.sh script that
will actually modify (copy) the DOTFILE to colorize. And this new dotfile can
be sent to `dot` to generate a beautiful PNG image.

You can try to oneline everything with something like this:
./mapall.py --region us-east-1 --security > dotfile && ./auto_color.py --dotfile dotfile --nodes node1 node2 && ./colorize-dotfile.sh && dot -Tpng dotfile.colorized > dotfile.colorized.png '''

    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--dotfile', required=True, help='Dotfile to use')
    parser.add_argument('--nodes', nargs='+',
        required=True,
        help='''The list to use as starting nodes. Must be strings and in the
format that is in the dotfile, i.e. underscores instead
of dashes.''')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_arguments()
    colorize(args.dotfile, args.nodes)
