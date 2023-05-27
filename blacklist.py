#!/usr/bin/python

import requests
import re
import subprocess
import os

r = requests.get("http://www.malwaredomainlist.com/mdl.php?search=&colsearch=All&quantity=All")

data = r.text

datasplit=data.split('\n')

malIP=[]

for d in datasplit:
    d1=d.split('')

    if len(d1) > 3:
        s=re.search('\d+\.\d+\.\d+\.\d+', d1[2])

        if hasattr(s, 'group'):
            malIP.append(str(s.group(0)))

malIP1=malIP[:100]

print(len(malIP1))

for IP in malIP1:
    os.system("ufw deny from "+IP)

os.system("ufw enable")
