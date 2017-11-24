import subprocess
import os

# ["tasklist","|","python"]
# res = subprocess.Popen(["tasklist","|","python"],stdout=subprocess.PIPE)
res = subprocess.Popen("tasklist | grep python", stdout=subprocess.PIPE, shell=True)
python_process = res.stdout.readlines()
counts = len(python_process)

print(python_process, counts)
# if counts < 4:
#     os.system('python /Users/mac/Desv7ktop/3-req.py')
