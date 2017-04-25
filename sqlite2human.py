#!/usr/bin/pyhon
# -*- coding: utf-8 -*-
import sqlite3 as sql
import os
import sys

def analyze_db(db_path):
    connection = sql.connect(db_path)
    cursor = connection.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    all_tables = []
    for table in tables:
        table_content = []

        cursor.execute("pragma table_info('{0}');".format(table[0]))
        info_table = cursor.fetchall()
        table_head = []
        for i in info_table:
           table_head.append('{0}({1})'.format(i[1], i[2]))

        cursor.execute("SELECT * FROM {0};".format(table[0]))
        data_table = cursor.fetchall()
        for row in data_table:
            line = []
            for element in row:
                line.append(element)
            table_content.append(row)
        
        all_tables.append({'name': table[0], 'head': table_head, 'content': table_content})

    name = db_path.split('/')[-1]
    print_db(name, all_tables)

def print_db(name, db):
    scripts = ''
    html_body = ''
    for table in db:
        html_body += '''<div class="row"><div class="col-md-10"><h2>{0}</h2><table id="{1}" class="table table-striped table-bordered table-hover dataTable no-footer dtr-inline" width="100%" cellspacing="0" role="grid"><thead><tr>'''.format(table['name'], table['name'])
       
        head = table['head']
        for element in head:
            html_body += '''<th>{0}</th>'''.format(element)
        html_body += '''</tr></thead><tbody>'''

        body = table['content']
        for row in body:
            html_body += '''<tr>'''
            for element in row:
                if type(element) == unicode:
                    html_body += '''<td>{0}</td>'''.format(element.encode('utf-8'))
                else:
                    html_body += '''<td>{0}</td>'''.format(element)
            html_body += '''</tr>'''
        html_body += '''</tbody></table></div></div>'''

        scripts += '''$("#{0}").dataTable({{scrollX: true}});'''.format(table['name'])
        

    html_head = '''<!DOCTYPE html><html><head><title>{0}</title><meta charset="utf-8" /></head><body>'''.format(name)
    html_script = '''<script type="text/javascript" src="https://cdn.datatables.net/v/bs-3.3.7/jq-2.2.4/dt-1.10.13/datatables.min.js"></script><script>$(document).ready(function(){{{0}}});</script><link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/bs-3.3.7/jq-2.2.4/dt-1.10.13/datatables.min.css"/>'''.format(scripts)
    html_tail = '''</body></html>'''
    with open('{0}.html'.format(name), 'w') as web:
        web.write(html_head)
        web.write(html_body)
        web.write(html_script)
        web.write(html_tail)

def main(file):
    #try:
    analyze_db(file)
    #except Exception as e:
    #    print("[-] Error: {0}".format(e))
        
    #for root, dirs, files in os.walk('./'):
    #    try:  
    #        map(analyze_db, filter(lambda x: x.endswith('.sqlite'), files))
    #    except Exception as e:
    #        print e

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("[-] Usage: sqlite2human.py /path/to/db/")
