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

### 4- Set to run every 5 minutes
`crontab -e`
Add a rule at the bottom:
```
*/5 * * * * /usr/bin/python /home/pi/scriptname.py
```

### 5- Set up Flask web server

### 6- Create HTML page for server

