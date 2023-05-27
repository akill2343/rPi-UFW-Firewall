## Configuring a Firewall on a Raspebrry Pi using UFW (Uncomplicated Firewall)

**Notes:**

- UFW is disabled by default (after installing). It must be enabled after configuration to use it.  
- Rules are created for TCP and UDP using IPv4 and IPv6. Rules should be created based on the protocol that the service is using.  
- A deny-all rule is created by default.  
- For good measure, enable SSH as the first rule.  


#installation  
`sudo apt install ufw`

### 1- Configure pi as gateway:

`sudo nano /etc/network/interfaces`

```
auto lo
iface lo inet loopback

auto eth0
allow-hotplug eth0
iface eth0 inet static
address 192.168.0.1
netmask 255.255.255.0
network 192.168.0.0
broadcast 192.168.0.255
post-up ufw allow in on eth0 from any to any port 22 # allow ssh traffic
post-up ufw allow in on eth0 from any to any port 50000 # allow traffic to port 50000
post-up ufw default deny incoming # block all other incoming traffic
post-up ufw default allow outgoing # allow all outgoing traffic

auto wlan0
allow-hotplug wlan0
iface wlan0 inet manual
wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```

### Enable IP forwarding

`sudo nano -w /etc/ufw/sysctl.conf`

Uncomment the line  
`net.ipv4.ip_forward=1`


### Configure dnsmasq

Install with `sudo apt install dnsmasq`  

`sudo nano -w /etc/dnsmasq.conf`

```
interface=eth0

listen-address=127.0.0.1

domain=proxynetwork.com

dhcp-range=192.168.0.1,192.168.0.110,12h
```
Reboot to apply changes.

### 2- Configure UFW nat and filter

### 3- Script to get blacklisted IP and drop connection

```
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
```

### 4- Set to run every 5 minutes
`crontab -e`
Add a rule at the bottom:
```
*/5 * * * * /usr/bin/python /home/pi/scriptname.py
```

### 5- Flask web server
`pip install flask`  
`pip install wifi`
```
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
```

### 6- HTML page for server
```
<html>
  <head>
    {% if title %}
    <title>{{ title }} - titlewa</title>
    {% else %}
    <title>List of Wifi Networks</title>
    {% endif %}
  </head>
  <body>
    <h2>List of Available Wifi Networks :</h2>
      <form role="form" method='POST' action='/connect'>
        <div class="form-group">
          <input type="text" name="Network" class="form-control" id="url-box" placeholder="Enter Wifi Network Number To be Connected..." style="max-width: 700px;">
        </div>
        <div class="form-group">
          <input type="password" name="Password" class="form-control" id="url-box" placeholder="Password" style="max-width: 700px;">
        </div>
        <button type="submit" class="btn btn-default">Submit</button>
      </form>
     {% for ssid in networks %}
    <div><p>{{ ssid }}</p></div>
    {% endfor %}
  </body>
</html>
```
