#!/usr/bin/env python
from __future__ import print_function, unicode_literals
from os.path import isfile, join

import os
import argparse

def log(msg, level):
	if level == 0:
		print("[+] {0}".format(msg))
	elif level == 1:
		print("[-] {0}".format(msg))
	elif level == 2:
		print("[!] {0}".format(msg))
		raise SystemExit

class SmaliAnalyzer:
	def __init__(self, arg):
		self.arg = arg

	def analyze(self, path):
		log("Analyzing {0}".format(path), 0)

def get_smali_files(path):
	return [join(path, s) for s in os.listdir(path) if isfile(join(path, s)) and s.endswith('smali')]

def get_smali_files_recursive(path):
	smali_files = []
	for root, dirs, files in os.walk(path):
		smali_files += [join(root, s) for s in files if s.endswith('smali')]
	return smali_files

def main():
	description = 'smaly2human'
	examples = 'example'
	parser = argparse.ArgumentParser(description=description, epilog=examples)

	parser.add_argument('-v', '--visual', help='First argument', action='store_true')
	parser.add_argument('-a', '--analyze', help='First argument', action='store_true')
	parser.add_argument('-r', '--recursive', help='First argument', action='store_true')

	parser.add_argument('-f', '--file', help='First argument')
	parser.add_argument('-d', '--directory', help='First argument')

	output = parser.parse_args()

	analyzer = SmaliAnalyzer("")

	if output.analyze and not output.directory and output.recursive:
		log("It is necessary to specify a directory when is used the recursive option", 2)

	if output.analyze and output.directory and output.recursive:
		files = get_smali_files_recursive(output.directory)
		map(analyzer.analyze, files)

	if output.analyze and output.directory and not output.recursive:
		files = get_smali_files(output.directory)
		map(analyzer.analyze, files)

	if output.analyze and output.file:
		analyzer.analyze(output.file)

if __name__ == '__main__':
    main()
