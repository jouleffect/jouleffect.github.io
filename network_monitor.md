---
layout: post
title: Network connections monitor
date: 01/03/2022
tags: networking - nmap - wifi - lan
---

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![made-with-bash](https://img.shields.io/badge/Made%20with-Bash-1f425f.svg)](https://www.gnu.org/software/bash/)

## Python script to monitor connections to private network, using Nmap

This script is thinked in order to find if new devices connect to a private access point, in a single specific lan network.\
It is possible to define a list of allowed devices (MAC addresses) in a text file, so that they can be distinguished by the unknowed ones.\
The main script, named "monitor.py" is the following:

```python
import subprocess
import datetime
import re
import pandas as pd

networks = pd.DataFrame(columns=["ID","MAC"])
networks.set_index("ID", inplace=True)

output = subprocess.check_output(f"nmap -sn 192.168.0.0/24", shell=True).decode()
scan_mac = re.findall("MAC Address: (.*)",output)

mac_list = pd.read_csv('networks.csv')

allowed_devices = pd.read_csv('allowed_devices.csv')

i = 0
for mac in scan_mac:
	m = mac.split()[0]
	networks.loc[i] = (m)
	if m not in mac_list.values:
		if m in allowed_devices.values:
			device = allowed_devices.loc[allowed_devices['MAC'] == m]
			name = device.NAME.item()
			f = open('log_connections', 'a')
			log = (f"[{datetime.datetime.now().strftime('%Y/%m/%d %H:%m:%S')}] {name} is connected\n")
			f.write(log)
			print(log)
			f.close()
		else:			
			f = open('log_connections', 'a')
			log = (f"[{datetime.datetime.now().strftime('%Y/%m/%d %H:%m:%S')}] Unknow device connected: {m}")
			f.write(log)
			print(log)
			f.close()
	i +=1
  
networks.to_csv('networks.csv')

```

* * *

