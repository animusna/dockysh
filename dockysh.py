import os
import subprocess
import sys
from cmd    import Cmd
from typing import cast


class Dockysh(Cmd):

#region Utils methods
    def do_clear(self,arg):
        os.system('clear')

    def do_c(self,arg):
        self.do_clear(arg)

    def do_shellver(self,arg):
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
    def __filter(self,items,arg) :        
        filtered_list=[]
        for item in items:
            if arg in item:
                filtered_list.append(item)
        return filtered_list            
#endregion

#region Images

    def do_lsi(self,arg):
        if not arg:
            os.system('docker images ')
        else:
            os.system('docker images | grep -i ' + arg)

    def do_rmi(self,arg):
        cmd=['docker', 'images', '--format',  "{{.ID}}\\t{{.Tag}}\\t{{.Size}}\\t{{.Repository}}"]
        p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        images=p1.stdout.read().decode()

        if arg:
            images=self.__filter(images.splitlines(),arg)
        else:
            images=images.splitlines()

        if not images:
            print("No results found!")
        else:
            print("\nFound {imgs} images in base your filter '{filter}'. Please confirm the deletion of the images found.".format(imgs=len(images),filter=arg))
            for image in images:
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
    def do_idc(self,arg):
        sh='docker container ls -a '

        if arg:
            sh+= ' | grep -i ' + arg            
        
        sh+=' | cut -c1-12'

        os.system(sh)

    def do_psh(self,arg):
        sh="C:\\Windows\\System32\WindowsPowerShell\\v1.0\\powershell.exe"
        id = ""
        if arg:
            id=arg
        else:
            id = input("Please tell me the container id: ")            
        
        if id:
            os.system("docker exec -it " + id + " " + sh)
        else:
            print("Id not provided!")

    def do_rmc(self,arg):
        cmd=['docker', 'container', 'ls', '--format', "{{.ID}}${{.Image}}${{.Status}}${{.Command}}"]
        p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)

        containers=p1.stdout.read().decode()

        if arg:
            containers=self.__filter(containers.splitlines(),arg)
        else:
            containers=containers.splitlines()

        if not containers:
            print("No results found!")
        else:
            print("\nFound {cntrs} containers in base your filter '{filter}'. Please confirm the deletion of the containers found.".format(cntrs=len(containers),filter=arg))
            for container in containers:
                
                info=container.split("$")
                print(f'{container}==>{len(info)}')
                answer=input(f'\nDo you want eliminate the container with id "{info[0]}" based on image with ID "{info[1]}" ?\n([Y]=> yes/ [N]=>no / [E]=> exit from this operation): ')

                if answer.lower() == "y":
                    try:
                        os.system("docker container rm " + info[0])
                    except:
                        print(f'Problems during the deletion of the container "{info[0]}". Check prevoius messages.\n')
                elif answer.lower() == "e":
                    print('\n')
                    break
                else:
                    print(f'Container "{info[0]}" not removed!\n')

    def do_sh(self,arg):
        sh="/bin/bash"
        id = ""
        if arg:
            id=arg
        else:
            id = input("Please tell me the container id: ")
        
        os.system("docker exec -it " + id + " " + sh)

    def do_start(self,arg):
        id = ""
        if arg:
            id=arg
        else:
            id = input("Please tell me the container id: ")
        
        os.system("docker container start {id_container}".format(id_container=id))

    def do_stop(self,arg):
        id = ""
        if arg:
            id=arg
        else:
            id = input("Please tell me the container id: ")
        
        os.system("docker kill {id_container}".format(id_container=id))

    def do_lsc(self,arg):
        if arg:
            os.system('docker container ls -a | grep -i ' + arg)
        else:
            os.system('docker container ls -a ')

#endregionqui

#region exit methods
    def do_exit(self, inp):
        print("Bye")
        return True

    def do_q(self, inp):        
        return self.do_exit(self)
#endregion

#region Help methods
    def help_clear(self):
        print('Clear the screen')        
    def help_c(self):
        self.help_c()          
    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')
    def help_idc(self):
        print('usage: idc [filter]\nGet id of containers corresponding the provided filter.')        
    def help_lsc(self):
        print('usage: lsc [filter]\nList all containers corresponding the provided filter.')
    def help_lsi(self):
        print('usage: lsi [filter]\nList all images corresponding the provided filter.')     
    def help_psh(self):
        print('usage: psh [container id]\nRun a powershell on Windows container.')            
    def help_rmc(self):
        print('usage: rmc [filter]\nRun an interactive deletion of all containers corresponding the filter provided.')                    
    def help_rmi(self):
        print('usage: rmi [filter]\nRun an interactive deletion of all images corresponding the filter provided.')            
    def help_sh(self):                
        print('usage: sh [container id]\nRun a bash shell on Linux container.')     
    def help_shellver(self):
        print('Get the version of Dockysh')    
    def help_start(self):
        print('usage: start [container id]\nStart a stopped container.')            
    def help_stop(self):
        print('usage: stop [container id]\nStop a running container.')                                
    def help_q(self):
        self.help_exit()           
    def help_ver(self):
        print('Get the version of the Docker client and the Docker Engine')
#endregion

    def default(self, inp):
        if inp == 'q':
            return self.do_exit(inp)     
        else:
            try:
                os.system('docker ' + inp)
            except:
                print('Command not found or something went wrong') 

#region Shell Cmd configuration

    # Custom library configuration
    shellVersion ="0.0.1"
    # Header configuration
    border='\n**********************************************************************\n'
    title="Welcome to the Dockysh a friendly wrapper to Docker shell."
    subTitle ='                 Type help or ? to list commands.'
    # Python library Command configuration
    do_EOF = do_exit
    help_EOF = help_exit       
    intro = f'{border}***** Welcome to the Dockysh a friendly wrapper to Docker shell. *****{border}{subTitle}{border}'
    prompt = 'you@Dokysh$ '

#endregion

try:
    Dockysh().cmdloop()
except KeyboardInterrupt:
    print('Bye!') 
except BaseException as e:
    print("\n:( This is embarrassing! Somenthing went wrong... Please report the error below!\n")
    print(e.message)
