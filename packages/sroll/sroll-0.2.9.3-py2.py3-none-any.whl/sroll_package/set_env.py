import sys
import os
import socket
import numpy as np
import platform
import fileinput
import site

if(sys.version_info[0]==3):
  import subprocess as sh
else:
  import commands as sh

# -------------------------------------------------------
def update_params(path,name):
  """
  Update output path in unit test parameters files,create a folder for the output and update paths
  """
  mapout =str(path)+"/MAP/"+str(name)+"_maps/"
  vecout = str(path)+"/VEC/"+str(name)+"_vecs/"
  
  os.system('mkdir -p '+str(mapout))
  os.system('mkdir -p '+str(vecout))
  
  # Read in the file
  with open(str(path)+"/srollex/sroll4/unit_test_"+str(name)+".py", 'r') as file :
    filedata = file.read()

  # Replace the target string
  filedata = filedata.replace(' MAP = ',' MAP = ["'+str(mapout)+'Nside%s_%s"%(Nside,i) for i in bolo_map]')
  filedata = filedata.replace('Out_VEC = ','Out_VEC = ["'+str(vecout)+'Nside%s_%s"%(Nside,i) for i in bolo]')
  filedata = filedata.replace('Out_Offset = ','Out_Offset = ["'+str(vecout)+'Nside%s_%s"%(Nside,i) for i in bolo]')
  filedata = filedata.replace('Out_Offset_corr = ','Out_Offset_corr = ["'+str(vecout)+'Nside%s_%s"%(Nside,i) for i in bolo]')
  filedata = filedata.replace('Out_xi2 = ','Out_xi2 = ["'+str(vecout)+'Nside%s_%s"%(Nside,i) for i in bolo]')
  filedata = filedata.replace('Out_xi2_corr = ','Out_xi2_corr = ["'+str(vecout)+'Nside%s_%s"%(Nside,i) for i in bolo]')


  # Write the file out again
  with open(str(path)+"/srollex/sroll4/unit_test_"+str(name)+".py", 'w') as file:
    file.write(filedata)

  
# -------------------------------------------------------
def clone_repository(path):
  """
    Clone SRoll repository from git using path given
  """
  os.system('git clone https://github.com/TF22559/SRoll.git '+str(path)+'/srollex')

  #os.system('git clone  https://gitlab.ifremer.fr/iaocea/srollex.git ' +str(path)+'/srollex')
# -------------------------------------------------------
def add_host(path):
  """ 
    Function to use to add a new host in the srollex_setenv.sh 
  """

  #get host info
  hostname = socket.gethostname()
  python_path =  str(path)+'/py_sroll/'
  ld_lib = str(path)+'/py_sroll/'
  
  modules =""
      
  # Read in the file
  with open(str(path)+"/srollex/setenv.sh", 'r') as file :
    filedata = file.read()

  # Replace the target string
  filedata = filedata.replace('  *)',"  "+str(hostname+"*)\n \techo \" "+hostname+" detected \" \n\texport SROLLHOST="+hostname+"\n\t "+modules+"\n\texport PYTHONPATH="+python_path+" \n\texport LD_LIBRARY_PATH="+python_path+":$LD_LIBRARY_PATH \n ;;\n  *)"))

  # Write the file out again
  with open(str(path)+"/srollex/srollex_setenv.sh", 'w') as file:
    file.write(filedata)

  print ("host =",hostname)    
  print("python path =",python_path)
  print("ld_library_path =",ld_lib)


# -------------------------------------------------------
def create_pyEnv(path):
  """
    Create sroll python virtual environement
  """
  current_path = os.path.dirname(os.path.abspath(__file__))
  
  #os.system('virtualenv -p python3.6 ' +str(path)+'/py_sroll')
  try:
    #os.system('python3.6 -m venv ' +str(path)+'/py_sroll')
    os.system('virtualenv -p python3.6 ' +str(path)+'/py_sroll')
    print("PASS")
    #os.system('virtualenv --python=3.6 ' +str(path)+'/py_sroll')
  except:
    try:
      os.system('virtualenv -p python3.6 ' +str(path)+'/py_sroll')
    except:
      #os.system('virtualenv -p python3 ' +str(path)+'/py_sroll')
      os.system('echo ERROR : failed to install python 3.6')
      exit()


  os.system('./py_sroll/bin/pip install -r '+str(current_path)+'/static/requirements.txt')

# -------------------------------------------------------
def update_Makefile(path,namedir):
  """
    Update Makefile path python and library to load for compilation
  """
  
  #Define path for python env
  DIRPYTHONPATH = str(path)+'/py_sroll/'

  #get includes path
  cmd = "from sysconfig import get_paths; info = get_paths(); print(info['include'])"
  status, output = sh.getstatusoutput('./py_sroll/bin/python -c "'+str(cmd)+'"')
  DIRPYTHONINC = output

  # get numpy path
  cmd = "from sysconfig import get_paths; info = get_paths(); print(info['purelib'])"
  status, output = sh.getstatusoutput('./py_sroll/bin/python -c "'+str(cmd)+'"')
  DIRNUMPYINC = output+'/numpy/core/include'
 

  #get python lib version
  status, output = sh.getstatusoutput('./py_sroll/bin/python-config --ldflags')

  LIBPYTHONLIB = DIRPYTHONINC.split('/')
  LIBPYTHONLIB = '-l'+str(LIBPYTHONLIB[len(LIBPYTHONLIB)-1])

  #get pythonlib dir
  #DIRPYTHONLIB = str(DIRPYTHONPATH) + 'lib'
  cmd = "from sysconfig import get_paths; info = get_paths(); print(info['stdlib'])"
  status, output = sh.getstatusoutput('./py_sroll/bin/python -c "'+str(cmd)+'"')


  idlib = LIBPYTHONLIB.lstrip('-lpython')
  DIRPYTHONLIB = output+'/config-'+str(idlib)+'-x86_64-linux-gnu/'


  OPTIONPYTHON = '-DPYTHON3'
  PYTHONCONF = '`python-config --ldflags` `python-config --cflags`'



  #DIRPYTHONPATH = str(path)+'/py_sroll/'
  #DIRPYTHONINC = str(path)+'/py_sroll/include/'+str(os.listdir(str(path)+'/py_sroll/include/')[0])
  #DIRNUMPYINC = str(path)+'/py_sroll/lib/'+str(os.listdir(str(path)+'/py_sroll/lib/')[0])+'/site-packages/numpy/core/include'
  #DIRPYTHONLIB = str(DIRPYTHONPATH) + 'lib'
  #LIBPYTHONLIB = str(os.listdir(str(path)+'/py_sroll/include/')[0])
  #OPTIONPYTHON = '-DPYTHON3'
  #PYTHONCONF = '`python-config --ldflags` `python-config --cflags`'

  

  ## replace values in Makefile
  for line in fileinput.input([str(path)+"/srollex/"+str(namedir)+"/Makefile"], inplace=True):
      if line.strip().startswith('DIRPYTHONPATH :='):
          line = 'DIRPYTHONPATH := '+str(DIRPYTHONPATH)+'\n'
      if line.strip().startswith('DIRPYTHONINC :='):
          line = 'DIRPYTHONINC := '+str(DIRPYTHONINC)+'\n'
      if line.strip().startswith('DIRNUMPYINC :='):
          line = 'DIRNUMPYINC := '+str(DIRNUMPYINC)+'\n'
      if line.strip().startswith('DIRPYTHONLIB :='):
          line = 'DIRPYTHONLIB := '+str(DIRPYTHONLIB)+'\n'
      if line.strip().startswith('DIRPYTHONLIB :='):
          line = 'DIRPYTHONLIB := '+str(DIRPYTHONLIB)+'\n'
      if line.strip().startswith('LIBPYTHONLIB :='):
          line = 'LIBPYTHONLIB := '+str(LIBPYTHONLIB)+'\n'
      if line.strip().startswith('OPTIONPYTHON :='):
          line = 'OPTIONPYTHON := '+str(OPTIONPYTHON)+'\n'
      if line.strip().startswith('PYTHONCONF :='):
          line = 'PYTHONCONF := '+str(PYTHONCONF)+'\n'
  
      sys.stdout.write(line)


  #print python values  
  python_params = 'DIRPYTHONPATH := '+str(DIRPYTHONPATH) +'\n'+'DIRPYTHONINC := '+str(DIRPYTHONINC)+'\n'+'DIRNUMPYINC := '+str(DIRNUMPYINC)+'\n'+'DIRPYTHONLIB := '+str(DIRPYTHONLIB)+'\n'+'LIBPYTHONLIB := '+str(LIBPYTHONLIB)+'\n'+'OPTIONPYTHON := '+str(OPTIONPYTHON)+'\n'+'PYTHONCONF := '+str(PYTHONCONF) 
  
  print('=> python_paths : \n'+python_params)

# -------------------------------------------------------
def list():
  """
    Print a list of the functions available with set_env
  """

  print('-> clone_repository(path_to_directory) \n')
  print('-> create_pyEnv(path_to_directory) \n')
  print('-> update_Makefile(path_to_makefile) \n')
  print('-> add_host(path_to_srollex_setenv) \n')
  print('-> update_params(path_to_srollex_setenv,name_param) \n')
  print('-> install() \n')

# -------------------------------------------------------
def install():
  """
    Run all routine to install SRoll at current path 
  """
             
  print('\t\t-------------------------\n\t\t## Start install SRoll ##\n\t\t-------------------------\n')
 
  path = os.path.abspath(os.getcwd())

  if(sys.version_info[0]==3):
    val = input("Install Sroll at "+str(path)+" (y/n) ?")
  else:
    val = raw_input("Install Sroll at "+str(path)+" (y/n) ?")
  
  
  if(val=="y"):

    ## git clone
    clone_repository(path)

    ##create pyEnv
    create_pyEnv(path)
    
    ## add host to srollex_setenv.sh
    add_host(path)  

    ## update Makefile -> init python path
    update_Makefile(path,'sroll4')
    update_Makefile(path,'stim')
    ## update unit test output
    update_params(path,'857')
    update_params(path,'cfosat')
    
  else:
    print("exit()")
  
  
# -------------------------------------------------------






