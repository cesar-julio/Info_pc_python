from datetime import datetime
import psutil
import platform
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def getUnit(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

plataforma = platform.uname()
def listInfoPc (objPlt):
    list_info = ["system", "node", "release", "version", "machine", "processor"]
    indice = 0
    info = ""
    info += f"{datetime.today()}\n"
    for elm in objPlt:
        info += f"{list_info[indice]} : {elm}\n"
        indice += 1
    pc = psutil.cpu_count(logical=False)
    tc = psutil.cpu_count(logical=True)
    info += f"Physical cores: {pc}\n"
    info += f"Total cores: {tc}\n"

    particiones = psutil.disk_partitions()
    total_almacenamiento = 0
    for par in particiones:
        info += f"Divise: {par.device}\nMountpoint: {par.mountpoint}\nFile system type: {par.fstype}\n"
        try:
            par_usado = psutil.disk_usage(par.mountpoint)
        except PermissionError:
            continue
        total_almacenamiento += par_usado.total
        info += f"Total size: {getUnit(par_usado.total)}\nUsed: {getUnit(par_usado.used)}\nFree: {getUnit(par_usado.free)}\nPercentage: {par_usado.percent}%\n"
    info += f"Total storage: {getUnit(total_almacenamiento)}\n"
    info_disk = psutil.disk_io_counters()
    info += f"Total read: {getUnit(info_disk.read_bytes)}\nTotal write: {getUnit(info_disk.write_bytes)}\n"

    if_addrs = psutil.net_if_addrs()
    for internafe_name, interface_addres in if_addrs.items():
        for address in interface_addres:
            info += f"===== Interface: {internafe_name} =====\n"
            if str(address.family) == 'AddressFamily.AF_INET':
                info += f"IP Address: {address.address}\nNetmask: {address.netmask}\nBroadcast IP: {address.broadcast}\n"
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                info += f"MAC Address: {address.address}\nNetmask: {address.netmask}\nBroadcast MAC: {address.broadcast}\n"
    return info

def mostrarInfo ():
    return listInfoPc(plataforma)


