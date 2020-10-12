from subprocess import Popen, PIPE
p = Popen('df -h .', shell=True, stdout=PIPE, stderr=PIPE)
out, err = p.communicate()
ans = out.split()
print(ans[10].decode('utf-8'))
