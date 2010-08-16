#!/usr/bin/env python

# Test program to play with sqlite
# Requires Python 2.5+ or (Python <2.5 and PySQLite)

# This is horribly insecure and totally open to SQL injection!
# Do not use as the basis for any sort of network programming!

import sys
import time
import csv
import codecs
import sqlite3

DATABASE = 'testdb.sqlite'
LOG = sys.stderr # alternately open('someFile','a') to append to a file

def log(message):
	LOG.write('[' + time.ctime() + ']: ' + message + '\n')


def main(inputfilename):
	log('Reading from ' + inputfilename)
	
	# Use codecs.open() to prevent UTF-8 BOM issue
	csvreader = csv.reader( codecs.open(inputfilename, 'r', encoding='utf-8-sig')  )
	L = []
	for i in csvreader:
		L.append(i)
	
	writetable(DATABASE, L, inputfilename.split('.')[0] )
	
	return 0


def writetable(databasefile, datalist, tablename):
	"""Create and write some data to an SQLite database"""
	
	# Create a 'Connection'
	connection = sqlite3.connect(databasefile)
	# Create a 'Cursor'
	c = connection.cursor()
		
	# Create a table
	#  This risks SQL injection but is unavoidable as tablenames can't be parameterized?
	log('''Creating table %s''' %tablename)
	c.execute('''CREATE TABLE %s (rowid INTEGER PRIMARY KEY)''' %tablename)
	
	cols = tuple(datalist.pop[0])
	
	# Alter the table and add the columns we need, from first row of CSV
	for col in cols:
		# Again, parameterization would be better but it doesn't seem to work
		log('''Adding column %s to table %s''' %(col, tablename))
		c.execute('''ALTER TABLE %s ADD COLUMN %s''' %(tablename, col))
	
	# Write the actual data rows in
	#  THIS DOES NOT ACTUALLY WORK!!
	for row in datalist:
		for i in range(0,len(row)):
			log('''Inserting (table, col, value) = (%s, %s, %s)''' % (tablename, cols[i], row[i]))
			c.execute('''INSERT INTO %s (%s) VALUES ("%s")''' % (tablename, cols[i], row[i]))
	
	# And commit.
	connection.commit()


# Interactive mode
if __name__ = "__main__":
	sys.exit( main(sys.argv[1]) )