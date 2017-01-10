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

### content
# get mensa plan
weeknumber = datetime.date.today().isocalendar()[1]
conn = httplib.HTTPSConnection("www.stwno.de")
conn.request("GET", "/infomax/daten-extern/csv/UNI-P/{}.csv".format(weeknumber))
r = conn.getresponse()
data = r.read()
conn.close()
text = data.decode('latin-1')

# Parsing the text
c_soup = 'Soup'
c_main = 'Main dish'
c_side = 'Side dish'
c_dess = 'Dessert'
parsed = {c_soup: [], c_main: [], c_side: [], c_dess: []}
relevant_markers = {'V': 'vegetarian', 'VG': 'vegan'}
lines = text.split('\n')
for line in lines:
  fields = line.split(';')
  date_parts = fields[0].split('.')
  if not len(date_parts) == 3:
    # not a line with date
    continue
  # Is the date today
  now = datetime.datetime.now()
  if int(date_parts[0]) == now.day and int(date_parts[1]) == now.month and int(date_parts[2]) == now.year:
    category = fields[2]
    dish = fields[3]
    marker = fields[4]
    price = fields[5]
    if category.startswith('S'):
      c = c_soup
    elif category.startswith('H'):
      c = c_main
    elif category.startswith('B'):
      c = c_side
    elif category.startswith('N'):
      c = c_dess
    else:
      raise ValueError()
    parsed[c].append((dish.split('(')[0], marker.split(','), price))

# construct output
out_text = ''
for c in [c_soup, c_main, c_side, c_dess]:
  out_text += '*{}*\n'.format(c)
  for d in parsed[c]:
    out_text += '{}\t{}'.format(d[0], d[2])

    marker_list = [relevant_markers[k] for k in d[1] if k in relevant_markers]
    if marker_list:
      out_text += '\t({})'.format(','.join(marker_list))
    out_text += '\n'

response['text'] = out_text
print(json.dumps(response))
