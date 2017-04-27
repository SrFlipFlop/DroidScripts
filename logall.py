#!/usr/bin/python
from __future__ import print_function

import os
import argparse

def insert_log(file_name):
    lines = []
    with open(file_name, 'r') as smali:
        lines = smali.readlines()

    in_func = False
    class_name = ""
    num_vars = ""
    function_name = ""
    new_file = []
    for i, line in enumerate(lines):
        if '.class' in line:
            class_name = line.split('/')[-1].replace(';',"").replace('\n', '')
    
        if '.method' in line:
            in_fun = True
            function_name = line.split(' ')[-1].split('(')[0].replace('\n', '')
        
        if '.end method' in line:
            in_fun = False

        if '.locals' in line:
            num_vars = int(line.strip().split(' ')[1])
            if num_vars <= 2:
                num_vars = 2 
                new_file.append('    .locals 2')
                continue
            
        if i > 1 and '.prologue' in lines[i-1]:
            new_file.append('    const-string v{0}, "====Enter===="\n'.format(0))
            new_file.append('    const-string v{0}, "{1} -> {2}"\n'.format(1, class_name, function_name))
            new_file.append('    invoke-static {{v{0}, v{1}}}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I\n'.format(0, 1))
            new_file.append('    move-result v{0}\n'.format(0))

        new_file.append(line)
    
    with open(file_name, 'w') as smali:   
        for line in new_file:
            smali.write(line)         

def main():
    description = 'logall'
    examples = 'Example: logall -d /path/to/databases/ -r OR logall -f /path/to/database.smali'
    parser = argparse.ArgumentParser(description=description, epilog=examples)

    parser.add_argument('-r', '--recursive', help='First argument', action='store_true')
    parser.add_argument('-f', '--file', help='First argument')
    parser.add_argument('-d', '--directory', help='First argument')

    output = parser.parse_args()

    if output.directory and output.recursive:
        for root, dirs, files in os.walk('./'):
            try:
                map(insert_log, filter(lambda x: x.endswith('.smali'), map(lambda y: "{0}{1}".format(root,y) if root.endswith('/') else "{0}/{1}".format(root,y), files)))
            except:
                print("ERROR {0}".format(root))

    if output.directory and not output.recursive:
        for root, dirs, files in os.walk('./'):
            try:
                map(insert_log, filter(lambda x: x.endswith('.smali'), map(lambda y: "{0}{1}".format(root,y) if root.endswith('/') else "{0}/{1}".format(root,y), files)))
            except:
                print("ERROR {0}".format(root))
            break

    if output.file:
        insert_log(output.file)

if __name__ == "__main__":
    main()
