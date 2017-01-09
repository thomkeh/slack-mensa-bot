#!/usr/bin/env python

from __future__ import print_function
import cgi
import datetime
import httplib
import json

import cgitb
cgitb.enable()

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

response['text'] = text
print(json.dumps(response))
