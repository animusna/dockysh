import os
import subprocess
import sys
from cmd import Cmd
from typing import cast


class Dockysh(Cmd):

#region Utils methods
    def do_clear(self,arg):
        os.system('clear')

    def do_c(self,arg):
        self.do_clear(arg)

    def do_shellver(self):
        print(self.shellVersion)

    def do_ver(self,arg):
        if arg == '':
            os.system('docker version')
        elif arg == 'client':
             os.system('docker version --format ''{{.Server.Version}}''') 
        elif arg == 'server':
            os.system('docker version --format ''{{.Client.Version}}''')            
        else:
            print('wrong rgument')
#endregion

#region Images

    def do_lsi(self,arg):
        if arg == '':
            os.system('docker images ')
        else:
            os.system('docker images | grep -i ' + arg)
         

    def do_rmi(self,arg):
        cmd=['docker', 'images', '--format',  "{{.ID}}\\t{{.Tag}}\\t{{.Size}}\\t{{.Repository}}"]
        p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        images=p1.stdout.read().decode()
        for image in images.splitlines():
            info=image.split("\t")
            
            answer=input(f'\nDo you want eliminate the image with id "{info[0]}" with tag "{info[1]}" of size "{info[2]}" from repository "{info[3]}"" ?\n([Y]=> yes/ [N]=>no / [E]=> exit from this operation): ')

            if answer.lower() == "y":
                try:
                    os.system("docker rmi " + info[0])
                except:
                    print(f'Problems during the deletion of the image "{info[0]}". Check prevoius messages.\n')
            elif answer.lower() == "e":
                print('\n')
                break
            else:
                print(f'Image "{info[0]}" not removed!\n')

#endregion

#region Containers
    def do_idforc(self,arg):
        sh='docker container ls -a '

        if arg != '':
            sh+= ' | grep -i ' + arg            
        
        sh+=' | cut -c1-12'

        os.system(sh)

    def do_powershell(self,arg):
        sh="C:\\Windows\\System32\WindowsPowerShell\\v1.0\\powershell.exe"
        id = ""
        if arg == '':
            print("Please tell me the container id")
            id = input("Please tell me the container id")
        else:
            id=arg
        
        os.system("docker exec -it " + id + " " + sh)

    def do_shell(self,arg):
        sh="/bin/bash"
        id = ""
        if arg == '':
            print("Please tell me the container id")
            id = input("Please tell me the container id")
        else:
            id=arg
        
        os.system("docker exec -it " + id + " " + sh)

    def do_lsc(self,arg):
        if arg == '':
            os.system('docker container ls -a ')
        else:
            os.system('docker container ls -a | grep -i ' + arg)               
#endregion

#region exit methods
    def do_exit(self, inp):
        print("Bye")
        return True

    def do_q(self, inp):        
        return self.do_exit(self)
#endregion

#region Help methods
    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')
    def help_q(self):
        self.help_exit()
    def default(self, inp):
        if inp == 'q':
            return self.do_exit(inp)     
        else:
            try:
                os.system('docker ' + inp)
            except:
                print('Command not found or something went wrong') 
#endregion

#region Shel Cmd configuration

    # Custom library configuration
    shellVersion =" 1.0.0"

    # Python library Comnmand configuration
    do_EOF = do_exit
    help_EOF = help_exit       
    intro = '\n**********************************************************************\n***** Welcome to the Dockysh a friendly wrapper to Docker shell. *****\n**********************************************************************\n                 Type help or ? to list commands.\n**********************************************************************\n'
    prompt = 'you@Dokysh$ '

#endregion

try:
    Dockysh().cmdloop()
except KeyboardInterrupt:
    print('Bye!') 
except BaseException as e:
    print("\n:( This is embarrassing! Somenthing went wrong... Report the error below!\n")
    print(e.message)
