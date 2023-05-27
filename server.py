#!/usr/bin/python

from flask import Flask
from flask import render_template
from flask import request
import subprocess,os
import sys,requests
import re
app = Flask(__name__)

# Todo: Implement connect function

Ilist = None

wlan = subprocess.check_output("ifconfig | awk '{print $1}' | grep wlan| head -n 1",shell = True).rstrip()
print "Wlan interface : %s"%wlan
cmd = "wifi -i " + wlan + " scan"
print cmd
while True:
    try:
        Ilist = subprocess.check_output(cmd,shell=True)
        arr = Ilist.split("\n")
        break
    except:
        continue

for i in range(len(arr)):
    arr[i] = str(i+1) + ".  " + arr[i]

def connect(network):
    for i in range(len(arr)):
        if re.findall("^%s\."%network,arr[i]):
            SSID = arr[i]
            break
    print SSID
    return SSID
        

@app.route("/")
def hello():
    return  render_template('index.html',networks = arr)

@app.route("/connect", methods = ['POST'])
def conn():
        network = connect(12)
        return "Connecting to the network..." + network
        nw = request.form['url']
#    try:
        nw = request.form['url']
        r = requests.get(rw)
        print r.text
#    except:
        print "Error!"
        return "Connecting to the network.."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
