#!/usr/local/bin/python3
import sys
import csv
import sqlite3

if __name__ == "__main__":

    csvfile_name = '/tmp/unique.csv'
    if len(sys.argv) == 2:
        csvfile_name = sys.argv[1]

    conn = sqlite3.connect('../edinburgh/db/showcase.db')

    with open(csvfile_name, 'rt') as csvfile:
        csvreader = csv.reader(csvfile)
        count = 0
        pageWorth = []
        for row in csvreader:
            results = conn.execute('select answer from users inner join question_link on users.id = question_link.user_id where name = ? and question_link.question_id = "20738922";', [row[0]])
            found=None
            for result in results:
                found = result[0]
            if not found:
                #print ("Failed to find %s" % row[0])
                print ('"%s","%s","%s","%s"' % (row[0],row[1],row[2],''))
            else:
                print ('"%s","%s","%s","%s"' % (row[0],row[1],row[2],found))

