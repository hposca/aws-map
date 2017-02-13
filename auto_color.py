#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import fileinput
import re

dot_file = "dotfile_auto_color"
new_file = "dotfile_auto_color.new"
with open(dot_file, 'r') as infile, open('multi_sed.sh', 'w') as outfile:
    initial_string = "awseb_e_rhivxhxfy4_stack_AWSEBAutoScalingGroup_WZUHOPA8XW3C"
    color = "darkolivegreen2"

    array = [ initial_string ]

    outfile.write("#!/usr/bin/env bash\n\n")
    outfile.write("cp {} {}\n\n".format(dot_file, new_file))
    for element in array:
        if not element.startswith('subnet'):
            text = 'sed -i "s/\({} -> [a-zA-Z0-9_]*\) ;/\\1 [penwidth=7;color={}] ;/" {}\n'.format(element, color, new_file)
            outfile.write(text)

            for line in infile:
                next_elem_regex = re.compile('{} -> ([a-zA-Z0-9_]*) ;'.format(element))
                match_result = next_elem_regex.search(line)
                if match_result:
                    next_element = match_result.group(1)
                    if not next_element in array:
                        array.append(next_element)

            infile.seek(0,0)

    initial_string = "awseb_e_spxwp5tmjz_stack_AWSEBAutoScalingGroup_J10G3OFJY0OA"
    color = "cadetblue2"
    array = [ initial_string ]

    for element in array:
        if not element.startswith('subnet'):
            text = 'sed -i "s/\({} -> [a-zA-Z0-9_]*\) ;/\\1 [penwidth=7;color={}] ;/" {}\n'.format(element, color, new_file)
            outfile.write(text)

            for line in infile:
                next_elem_regex = re.compile('{} -> ([a-zA-Z0-9_]*) ;'.format(element))
                match_result = next_elem_regex.search(line)
                if match_result:
                    next_element = match_result.group(1)
                    if not next_element in array:
                        array.append(next_element)

            infile.seek(0,0)
