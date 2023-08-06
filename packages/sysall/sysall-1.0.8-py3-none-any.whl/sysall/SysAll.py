"""
SysAll is a tool that allows you to retrieve information about the environment, 
such as the name of the operating system, processor, RAM, IP address, MAC address of the machine.

It gathers the functionalities of several libraries such as 
wmi, psutil, platform, getmac, socket in one to facilitate the use/manipulation of environment data
for Python programmers.
"""

__version__ = '1.0.8'
__title__ = 'SysAll'
__description__ = "Tool to easily retrieve information from the environment and the network"
__autor__ = 'LixNew'
__twitter__ = '@LixNew2'
__url__ = "https://github.com/LixNew2/SysAll"

#Import
import os
import platform
import cpuinfo
import psutil
import socket
import getmac
import wmi
import requests
import multiprocessing
import ctypes
import subprocess


#System

#Functions
def get_os(name : bool = True, version : bool = True, release : bool = True) -> dict:
    """
    Returns operating system name (Window, Linux, MacOS)
    
    Args:
        name (bool): To return os name. Defaults to True.
        version (bool): To return os version. Defaults to True.
        release (bool): To return os release. Defaults to True.
    """
    
    #Dictionary that saves the returned information
    os_infos = {}
    
    #If name (True) add name in os_infos
    if name:
        os_infos['OS'] = platform.system()
    #If version (True) add version in os_infos
    if version:
        os_infos['version'] = platform.version()
    #If release (True) add release in os_infos
    if release:
        os_infos['release'] = platform.release()
    
    #If one or more (True) returns os_infos
    if (name or version or release):
        return os_infos
    else:
        #Returns None
        return None

def get_device_name() -> str:
    """Returns device name"""
    return socket.gethostname()

def get_hostname() -> str:
    """Returns the name of the account currently connected to the operating system."""
    return os.getlogin()

def get_appdata(hostname : bool = True, appdata_path : bool = True) -> dict:
    """
    Returns appdata hostname
    
    Args:
        hostname (bool) : To return appdata hostname. Defautls to True.
        appdata_path (bool): To return appdata path. Defaults to True.
    """
    
    #Dictionary that saves the returned information
    appdata_infos = {}
    
    appdata_hostname = os.environ['APPDATA']
    
    #If hostname (True) add hostname in appdata_infos
    if hostname:
        appdata_infos["hostname"] = appdata_hostname.split('\\')[2]
    #If appdata_path (True) add path in appdata_infos 
    if appdata_path:
        appdata_infos["appdata_path"] = appdata_hostname
    
    #If one or more (True) return appdata_infos   
    if (hostname or appdata_path):  
        return appdata_infos
    else:
        #Return None
        return None

def get_memory() -> float:
    """Returns the memory size : Mo"""
    
    memory_size = psutil.virtual_memory().total
    memory_size = memory_size / (1024**2)
    
    return memory_size

def get_cpu_info(brand: bool = True, cpu_frequency: bool = True, cores : bool = True) -> dict:
    """
    Return the processor brand (Intel, AMD) and frequency.
        
    Args:
        brand (bool): To return processor brand. Defaults to True.
        cpu_frequency (bool): To return processor frequency. Defaults to True.
        cores (bool): To retrun number of processor cores
    """
    #Dictionary that saves the returned information
    processor_infos = {}
    
    #If brand (True) add brand in processor_infos
    if brand:
        processor_infos["brand"] = cpuinfo.get_cpu_info()['brand_raw']
    #If cpu_frequency (True) add cpu_frequency in processor_infos
    if cpu_frequency:
        processor_infos["frequency"] = cpuinfo.get_cpu_info()['hz_actual_friendly']
        #If cores (True) add number of processor cores in processor_infos
    if cores:
        processor_infos["cores"] = multiprocessing.cpu_count()
        
    #If one or more (True) returns processor _infos
    if (brand or cpu_frequency or cores):
        return processor_infos
    else:
        #Returns None
        return None
            
def get_gpu_info(name: bool = True, ram: bool = True, driver_version: bool = True) -> dict:
    """
    Returns the informations of the graphics card.

    Args:
        name (bool, optional): To return graphics card name. Defaults to True.
        ram (bool, optional): To return graphics card ram. Defaults to True.
        driver_version (bool,To return graphics card driver verion. Defaults to True.
    """

    #Variable
    AMOUNT = 0
    
    #WMI object initialisation
    wmi_obj = wmi.WMI()
    
    #Get all GPU on the system
    gpus = wmi_obj.Win32_VideoController()
    
    #Dictionary that saves the returned information
    gpu_infos = {}
    
    #For all GPU in GPUS get info
    for gpu in gpus:
        AMOUNT+=1
        #If name (True) add name in gpu_infos
        if name:
            gpu_infos[f"Name GPU{AMOUNT}"] = gpu.Name
        #If ram (True) add ram in gpu_infos    
        if ram:
            gpu_infos[f"RAM GPU{AMOUNT}"] = gpu.AdapterRAM
        #If driver_version (True) add driver_version in gpu_infos
        if driver_version:
            gpu_infos[f"Driver_Version GPU{AMOUNT}"] = gpu.DriverVersion
    
    #If one or more (True) returns gpu_infos
    if (name or ram or driver_version):         
        return gpu_infos
    else:
        #Returns None
        return None

def get_disk_infos(path: str = 'C', total : bool = True, free: bool = True, used: bool = True):
    """
    Returns the informations of the disk : total free, used

    Args:
        path (str): Reader's letter. Defaults to 'C'.
        total (bool, optional): To return full size of the disk. Defaults to True.
        free (bool, optional): To return free size of the disk. Defaults to True.
        used (bool, optional): To return used size of the disk. Defaults to True.

    """
    #Returns information about the disk
    path = f'{path}:'
   
    #Dictionary that saves the returned information
    disk_infos = {}
    
    #Get dick space
    total_bytes = ctypes.c_ulonglong(0)
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(path), None, ctypes.pointer(total_bytes), ctypes.pointer(free_bytes))
    
    total_space = total_bytes.value
    free_space = free_bytes.value
    used_space = total_space - free_space
    
    #If total (True) add infos in disk_infos
    if total:
        disk_infos['total'] = f"{total_space / (1024**3):.2f}"
    #If free (True) add infos in disk_infos
    if free:
        
        disk_infos['free'] = f"{free_space / (1024**3):.2f}"
    #If used (True) add infos in disk_infos
    if used:
        disk_infos['used'] =  f"{used_space / (1024**3):.2f}"
    
    #If one or more (True) return gpu_infos
    if (total or free or used):
        return disk_infos
    else:
        #Return None
        return None
    
#Network

def get_IPv4() ->str:
    """Returns the IPv4 address"""
    return socket.gethostbyname(socket.gethostname())

def get_MAC() -> str:
    """Returns the MAC address"""
    return getmac.get_mac_address()

def get_public_ip():
    """Returns the public address"""
    ip = requests.get('https://api64.ipify.org').text
    return ip

def _network_infos():
    """Do not call"""
    
    net = subprocess.check_output('ipconfig /all')

    return net

def get_gateway(net=_network_infos()) -> str:
    """Returns the default gateway address"""
    
    for line in net.split(b'\r\n'):
        if b'Default Gateway' in line or b'Passerelle par d' in line:
            gateway = line.split(b':')[1].decode('utf-8').strip()
            if gateway != "":
                return gateway
            
def get_submask(net=_network_infos()) -> str:
    """Returns the address of the sub-mask"""
    
    for line in net.split(b'\r\n'):
        if b'Subnet Mask' in line or b'Masque de sous-r' in line:
            submask = line.split(b':')[1].decode('utf-8').strip()
            return submask
    
def get_DNS(net=_network_infos()) -> str:
    """Returns the address of the DNS server"""
    
    for line in net.split(b'\r\n'):
        if b'DNS Servers' in line or b'Serveurs DNS' in line:
            dns = line.split(b':')[1].decode('utf-8').strip()
            if dns != "fec0":
                return dns
            
def get_DHCP_status(net=_network_infos()) -> str:
    """Returns the DHCP status
    
    If the function returns "True" it means that DHCP is enabled.
    On the contrary, if the function returns "False", it means that DHCP is disabled.
    """
    
    for line in net.split(b'\r\n'):
        if b'DHCP Enabled' in line or b'DHCP activ' in line:
            dhcp_st = line.split(b':')[1].decode('utf-8').strip()
            if dhcp_st == "Yes" or dhcp_st == "Oui":
                return True
            else:
                return False  
    
def get_DHCP(net=_network_infos()) -> str:
    """Returns the address of the DNS server"""
    
    for line in net.split(b'\r\n'):
        if b'DHCP Server' in line or b'Serveur DHCP' in line:
            dhcp = line.split(b':')[1].decode('utf-8').strip()
            if dhcp != "":
                return dhcp