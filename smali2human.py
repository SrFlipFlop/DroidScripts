#!/usr/bin/env python
from __future__ import print_function, unicode_literals
from os.path import isfile, join

import os
import re
import json
import argparse

SMALI_ENCODE = {
	'B': 'byte',
	'C': 'char',
	'D': 'double',
	'F': 'float',
	'I': 'int',
	'J': 'long',
	'S': 'short',
	'V': 'void',
	'Z': 'boolean',
}

def log(msg, level):
	if level == 0:
		print("[+] {0}".format(msg))
	elif level == 1:
		print("[-] {0}".format(msg))
	elif level == 2:
		print("[!] {0}".format(msg))
		raise SystemExit

class SmaliAnalyzer:
	def __init__(self, output):
		self.output = output
		self.json = {}
		self.actual_json = None

	def analyze(self, path):
		log("Analyzing {0}".format(path), 0)
		with open(path, 'r') as smali:
			content = smali.read()
			self.info(content)
			self.methods(content)
			self.fields(content)

	def info(self, content):
		regex1 = r'(\.class.*;)'
		r1 = re.findall(regex1, content)
		aux = r1[0].split(' ')
		class_path = aux[-1].replace(';', '')
		class_type = aux[-2]
		
		regex2 = r'(\.super.*;)'
		r2 = re.findall(regex2, content)
		class_parent = "None"
		if len(r2) > 0:
			class_parent = r2[0].split(' ')[-1].replace(';', '')

		self.create_class_path(class_path)
		self.actual_json['name'] = class_path.split('/')[-1]
		self.actual_json['parent'] = class_parent
		self.actual_json['package'] = class_path
		self.actual_json['type'] = class_type

	def create_class_path(self, path):
		class_path = path.split('/')
		aux = self.json.setdefault(class_path[0], {})
		for k in class_path[1:]:
			aux = aux.setdefault(k,{})
		self.actual_json = aux

	def methods(self, content):
		if 'methods' not in self.actual_json:
			self.actual_json['methods'] = []

		regex = r'(\.method.*)'
		functions = re.findall(regex, content)
		for f in functions:
			method = {
				'name': self.method_name(f),
				'type': self.method_type(f),
				'params': self.method_params(f),
				'return': self.method_return(f),
				'content': self.method_content(f),
			}
			self.actual_json['methods'].append(method)

	def method_name(self, name):
		return ""

	def method_type(self, name):
		return ""

	def method_params(self, name):
		params = []
		r1 = re.findall(r'\((.*)\)', name)
		if r1 != ['']:
			r2 = re.findall(r'(L.*);|(\[L.*);|(\[[BCDFIJSZ])|([BCDFIJSZ])', r1[0])
			for group in r2:
				for field in group:
					if field != '':
						if field.startswith('['):
							param = field.replace('[','')
							if param in SMALI_ENCODE:
								params.append(SMALI_ENCODE[param] + '[]')
							else:
								params.append(param + '[]')
						elif field.startswith('L'):
							params.append(field)
						elif field in SMALI_ENCODE:
							params.append(SMALI_ENCODE[field])

		return params

	def method_return(self, name):
		ret = name.split(')')[-1]
		if ret in SMALI_ENCODE:
			return SMALI_ENCODE[ret]
		return ret

	def method_content(self, name):
		#TODO: do the same with a regex
		return []

	def fields(self, content):
		regex = r'(\.field.*)'
		fields = re.findall(regex, content)
		#print(fields)

	def charge_output(self):
		if isfile(self.output):
			with open(self.output, 'r') as out:
				self.json = json.loads(out.read())
	
	def write_output(self):
		with open(self.output, 'w') as out:
			out.write(json.dumps(self.json))

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
	parser.add_argument('-o', '--output', help='First argument')

	output = parser.parse_args()

	out_name = output.output if output.output else "default_smali2human.json"
	analyzer = SmaliAnalyzer(out_name)
	analyzer.charge_output()

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

	#analyzer.write_output()

if __name__ == '__main__':
    main()
