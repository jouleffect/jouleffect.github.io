---
layout: post
title: LAN Access Control Script
date: 01/03/2022
tags: networking - cybersecurity - wifi - lan
---

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

## Python script to monitor private network access, using Nmap

This script is thinked in order to detect new connections to a private access point, of a single specific lan network.\
A list of allowed devices (withelist) is defined in a text file.\
The first thing to do is to install the requirements:

```
> pip install padas
> sudo apt-get install nmap
```

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

We create a dataframe with a column named "MAC".\
The subprocess function "check_output" runs the **nmap** tool, in which the private network is the argument (in this example is 192.168.0.0/24)\
The output of nmap is dirty, so the **re** (regular expression) function python library could catch the desired string (we need to take the Mac address string of the output).
The _mac_list_ variable takes the lines of the online devices, saved at the end of the script in the _newtworks.csv_ file, to compare them with the new scanned devices.\
This comparation is made in the for loop, where every device that is not contained in the list is the new connected device, and it's connection is logged in a file. Furthermore, if the device is an allowed one listed in a text file, the log printed in the file specifies the name of the device connected, and the word "Unknown" otherwise.\
Since the script has to be run about every minute, in order to discover new changes, the final step to do is to put it in a crontab. Another solution is to change the script, by adding an infinite loop with a sleep time for each iteration, but is not recomended, because it could die or be killed without realizing it.

* * *

