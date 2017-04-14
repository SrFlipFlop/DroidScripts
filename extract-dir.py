#!/usr/bin/env python
from __future__ import print_function
from subprocess import Popen, PIPE

import os
import sys
import datetime

def is_package(name):
    cmd = 'adb shell "ls -al /data/data/{0}"'.format(name)
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
    r = p.communicate()[0]
    return ("No such file or directory" not in r)

def select_package():
    cmd = 'adb shell "ls /data/data/"'
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
    r = p.communicate()[0]
    packages = r.splitlines()

    print("[!] Incorrect application package, please selecte one in the following list:")
    for i, pkg in enumerate(packages, 1):
        print("\t[{0}] {1}".format(i, pkg))
        
        if i % 10 == 0:
            opt = raw_input("[?] Recongize the application package? [y/N] ")
            if opt in ['y','Y','yes','Yes']:
                num = raw_input("[?] Select the application using the number: ")
                return packages[int(num) - 1]

    opt = raw_input("[?] Recongize the application package? [y/N] ")
    if opt in ['y','Y','yes','Yes']:
        num = raw_input("[?] Select the application using the number: ")
        return packages[int(num) - 1]
    
    print("[x] Application package not specified")
    raise SystemExit

def get_dirs(package):
    cmd = 'adb shell "ls -al /data/data/{0}"'.format(package)
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
    r = p.communicate()[0]
    
    dirs = []
    for dir in r.splitlines():
        if not dir.startswith('l') and not "/data/app-lib/" in dir:
            dirs.append(dir.split(' ')[-1])
    return dirs        

def extract_dir(package, dir, out):
    cmd = 'adb pull /data/data/{0}/{1} ./{2}/'.format(package, dir, out)
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
    r = p.communicate()[0]
    print("[+] Extracted {0}".format(dir))

def create_folder(package):
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    name = "{0}_{1}".format(package, date)
    os.makedirs(name)
    print("[+] Created output folder {0}".format(name))
    return name

def main(argv):
    print("[^] Hello :D")
    pkg = argv[1] if len(argv) >= 2 else select_package()
    if not is_package(pkg):
        pkg = select_package()
    
    out = create_folder(pkg)
    for dir in get_dirs(pkg):
        extract_dir(pkg, dir, out)
    print ("[^] By :_(")

if __name__ == '__main__':
    main(sys.argv)
