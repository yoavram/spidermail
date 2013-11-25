import certifi
import shutil
import os.path

print "Attempting to copy certification file"

path = certifi.where()
shutil.copyfile(path,"cacert.pem")
if not os.path.exists("cacert.pem"):
	print "Failure"
else:
	print "Success"
