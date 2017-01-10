#!/usr/bin/env python

from __future__ import print_function
import cgi
import datetime
import httplib
import json
import sys

import cgitb
cgitb.enable()
reload(sys)
sys.setdefaultencoding('utf-8')

### header
print("Content-Type: application/json")
print()

response = {'response_type': "in_channel"}
text = ""

### content
# get mensa plan
weeknumber = datetime.date.today().isocalendar()[1]
conn = httplib.HTTPSConnection("www.stwno.de")
conn.request("GET", "/infomax/daten-extern/csv/UNI-P/{}.csv".format(weeknumber))
r = conn.getresponse()
data = r.read()
conn.close()
text += data.decode('latin-1')


# Parsing the text
out_text = ''
lines = text.split('\n')
for line in lines:
  fields = line.split(';')
  # Is a line with date
  date_parts = fields[0].split('.')
  if len(date_parts) == 3:
    # Is the date today
    now = datetime.datetime.now()
    if int(date_parts[0]) == now.day and int(date_parts[1]) == now.month and int(date_parts[2]) == now.year:
      out_text += '{}\t{}\n'.format(fields[3], fields[5]) 
      
response['text'] = out_text
print(json.dumps(response))
