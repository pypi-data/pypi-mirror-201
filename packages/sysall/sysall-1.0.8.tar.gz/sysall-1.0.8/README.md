# SysAll

[![Downloads](https://static.pepy.tech/personalized-badge/sysall?period=month&units=international_system&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/sysall)
[![sysall Version](https://img.shields.io/pypi/v/sysall)](https://pypi.org/project/sysall/)
[![sysall Python Version](https://img.shields.io/pypi/pyversions/sysall)](https://pypi.org/project/sysall/)

SysAll is a tool that allows you to retrieve information about the environment, 
such as the name of the operating system, processor, RAM, IP address, MAC address of the machine.

It gathers the functionalities of several libraries such as 
wmi, psutil, platform, getmac, socket in one to facilitate the use/manipulation of environment data
for Python programmers.

## Set up
----
### Install

~~~python
pip install sysall
~~~

### Upgrade
~~~~python
pip install --upgrade sysall
~~~~

## Support

If you want to contact me for questions, bugs, or problems or other : lixnew2@gmail.com

## Python version

Sysall was written for python 3.

## Functions


### System
Returns operating system name, version, release.
~~~python
get_os()
# You can use the arguments of the function to return or not certain elements. By default they are all on True.
# If you put them all on False, the function will return 'None'.
args = name, version, release
~~~


Returns device name
~~~python
get_device_name()
~~~


Returns the name of the account currently connected to the operating system.
~~~python
get_hostname()
~~~


Returns appdata hostname and path
~~~python
get_appdata()
# You can use the arguments of the function to return or not certain elements. By default they are all on True.
# If you put them all on False, the function will return 'None'.
args = hostname, appdata_path
~~~


Returns the memory size : Mo
~~~python
get_memory()
~~~


Returns the processor brand (Intel, AMD), frequency and cores.
~~~python
get_cpu_info()
# You can use the arguments of the function to return or not certain elements. By default they are all on True.
# If you put them all on False, the function will return 'None'.
args = brand, cpu_frequency, cores
~~~


Returns the type of the graphics card
~~~python
get_gpu_info()
# You can use the arguments of the function to return or not certain elements. By default they are all on True.
# If you put them all on False, the function will return 'None'.
args = name, ram, driver_version
~~~


Returns the informations of the disk : total free, used
~~~python
get_disk_infos()
# You can use the arguments of the function to return or not certain elements. By default they are all on True.
# If you put them all on False, the function will return 'None'.
args = path, total, free, used
~~~

### Network

Returns the IPv4 address
~~~python
get_IPv4()
~~~


Returns the MAC address
~~~python
get_MAC()
~~~


Returns the public address
~~~python
get_public_ip()
~~~


Returns the default gateway address
~~~python
get_gateway()
~~~


Returns the address of the sub-mask
~~~python
get_submask()
~~~


Returns the address of the DNS server
~~~python
get_DNS()
~~~


Returns the DHCP status
~~~python
get_DHCP_status()
~~~


Returns the address of the DHCP server
~~~python
get_DHCP()
~~~