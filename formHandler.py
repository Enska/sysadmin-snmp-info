#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
#
# Test class to handle forms with python

import cgi
import os
import cgitb; cgitb.enable()

values = {}
path = ['']
if os.environ.has_key('PATH_INFO'):
   path = os.environ['PATH_INFO'].split('/')[1:]

values['name'] = ""
values['ip'] = ""
values['dns'] = ""
values['snmpver'] = ""
values['snmpcomm'] = ""
values['1'] = ""
values['2'] = ""

form = cgi.FieldStorage()
key = "id=newdata"

print "Content-Type: text/html \n"
print "<html><head> </head><body><h4>formHandler.py</h4>"
print "debug: path: %s \n <br>" % path
if not (form.has_key(key)):
   print "ERROR, no key \"%s\" on the form we got... <br> \n" % key
re = form.getfirst(key, "ERR: nada...")
print "Debug: getfirst: key -> %s : %s <br> \n" % (key, re)

for valname in (values):
   tt1 = form.getfirst(valname, "ERR: got nothing from html-form")
   tt2 = form.getlist(valname)
   print "debug: input: getfirst: (name) %s -> (value) %s \n <br>" % (valname, tt1)
   print "debug: input: list of values: %s \n <br>" % tt2
   for pl in (tt2):
      print "Debug: values for-loop: %s <br><br> \n" % pl

print "</body></html>"