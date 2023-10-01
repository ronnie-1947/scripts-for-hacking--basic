import subprocess
import optparse
import re

def get_args():
    parser = optparse.OptionParser()

    parser.add_option('-i', '--interface', dest='interface', help='Declare an interface to change mac address')
    parser.add_option('-m', '--mac', dest='mac', help='Declare a new mac address')

    (options, argument) = parser.parse_args()

    if not options.interface:
        options.interface = input("Write interface ")

    if not options.mac:
        options.mac = input("write mac ")

    return options


def show_mac(int):
    ifconfigOutput = subprocess.check_output(['ifconfig', int])

    mac_address_pattern = r'([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}'
    mac = re.search(mac_address_pattern, str(ifconfigOutput))

    if not mac:
        return False
    return mac.group(0)


def mac_changer():
    
    subprocess.call(['ifconfig'])
    options = get_args()
    
    subprocess.call(['ifconfig', options.interface, 'down'])
    subprocess.call(['ifconfig', options.interface, 'hw', 'ether', options.mac])
    subprocess.call(['ifconfig', options.interface, 'up'])

    mac = show_mac(options.interface)
    print("")
    if mac:
        print(f"The new mac address is {mac}")
    else:
        print("Couldnot update mac address")


mac_changer()
