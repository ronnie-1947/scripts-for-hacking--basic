import subprocess
import re

interface = input("Which interface to take? > ")

res = subprocess.check_output(['ifconfig', interface], text=True)

mac_address_pattern = r'([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}'
mac = re.search(mac_address_pattern, res)


print(str(mac.group(0)))