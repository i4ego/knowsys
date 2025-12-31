from platform import uname, architecture
from psutil import *
from socket import getfqdn, gethostbyname
from requests import get
from json import loads
from uuid import getnode

class Info:
    def __init__(self):
        self.update()

class OS(Info):
    def update(self):
        uname = uname()
        self.name = f"{uname.system} {uname.release} ({uname.version})"
class Processor(Info):
    def update(self):
        self.name = uname().machine
        self.architecture = architecture()[0]
        self.boottime = boot_time()
        freq = cpu_freq()
        self.freq = [freq.current, freq.min, freq.max]
        phys = cpu_count(False)
        logic = cpu_count()
        self.cores = [phys, logic, logic//phys]
        self.percent = cpu_percent()
class RAM(Info):
    def update(self):
        usage = virtual_memory()
        self.total = usage.total
        self.used = usage.used
        self.free = usage.free
        self.percent = usage.percent
class Battery(Info):
    def update(self):
        info = sensors_battery()
        if info.secsleft <= 0: self.discharge = None
        else: self.discharge = info.secsleft
        if info.power_plugged != True | False: self.ispower = info.power_plugged
        else: self.ispower = None
class Network(Info):
    def update(self):
        hostname = getfqdn()
        self.hostname = hostname
        localip = gethostbyname(hostname)
        self.local_ip = localip
        pubipinfo = loads(get('http://ipinfo.io/json').text)
        self.public_ip = pubipinfo["ip"]
        mac = getnode()
        self.mac = mac
        self.ipinfo = pubipinfo
class PublicIP(Info):
    def update(self):
        net = Network()
        pubipinfo = net.ipinfo
        self.country = pubipinfo["country"]
        self.region = pubipinfo["region"]
        self.city = pubipinfo["city"]
        self.postal = pubipinfo["postal"]
        self.timezone = pubipinfo["timezone"]

if __name__ == "__main__":
    pass