import requests, os, tempfile
from urllib.parse import urlparse

def download(url):
  get_request = requests.get(url)

  # Get the file name
  parsed_url = urlparse(url).path
  filename = os.path.basename(parsed_url)
  
  #Get temp dir and change the directory
  temp_dir = tempfile.gettempdir() 
  os.chdir(temp_dir)

  with open(filename, "wb") as out_file: # write binary "wb"
    out_file.write(get_request.content)
  


download('https://images.pexels.com/photos/268533/pexels-photo-268533.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500')