from subprocess import Popen, PIPE

p = Popen('echo "Hola"', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate(b"input data that is passed to subprocess' stdin")
print (output.decode('utf-8'))