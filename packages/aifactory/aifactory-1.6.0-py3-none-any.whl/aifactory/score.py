import os
import requests
import zipfile
import subprocess
import gdown
from IPython import get_ipython

api_url = "https://grade-bridge.aifactory.space/grade"

def make_zip(key, main_name, func):
  run_type = 0
  main_filename = ''
  main_pyfilename = ''
  current_cwd = os.getcwd()  

  if '.py' not in main_name:
    run_type = 1

  if run_type == 1 and 'google.colab' in str(get_ipython()):
    print('Running on CoLab')
    run_type =2
  
  if run_type == 0: 
    print("python")    
  elif run_type == 1:     
    print("jupyter notebook")    
  elif run_type == 2: 
    print("google colab")    
    strs = main_name.split('=')
    ipynb_url = 'https://drive.google.com/uc?id=' + strs[1]
    main_filename = 'task.ipynb'
    output = '/content/' + main_filename
    gdown.download(ipynb_url, output)
  else: 
    print("not supported environments")
    return 
    
  zip_file = zipfile.ZipFile("./aif.zip", "w")  
  for (path, dir, files) in os.walk("./"):
    for file in files:       
      if "train" not in path and "drive" not in path and "sample_data" not in path and "aif.zip" not in file :      
        zip_file.write(os.path.join(path, file), compress_type=zipfile.ZIP_DEFLATED)
  zip_file.close()
  
def submit(model_name, key, main_name, func):
  make_zip(key, main_name, func)
  
  values = {"key": key, "modelname": model_name}
  res = requests.post(api_url, files = {'file': open("./aif.zip",'rb', )}, data=values)  
  if res.status_code == 200 or res.status_code == 201: 
    print("success")
    return
  print(res.status_code)  
  print(res.text)
