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

    def do_find(self,arg):
        if arg == '':
            os.system('docker images ')
        else:
            os.system('docker images | grep ' + arg)

    def do_rmi(self,arg):
        # cmd=['docker', 'images']
        # p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        # output = subprocess.check_output(('grep', arg), stdin=p1.stdout)
        # ps.wait()
        # if arg != '':
        #     cmd.append()
        #     cmd += '| grep ' + arg

        # out = subprocess.Popen(['wc', '-l', 'dockysh.py'], 
        # stdout=subprocess.PIPE, 
        # stderr=subprocess.STDOUT)
        # print(out.stdout.read())

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
                print('Command not found') 
#endregion

#region Shel Cmd configuration

    # Custom library configuration
    shellVersion =" 1.0.0"

    # Python library Comnmand configuration
    do_EOF = do_exit
    help_EOF = help_exit       
    intro = 'Welcome to the Dockysh smart docker shell.  Type help or ? to list commands.\n'
    prompt = 'you@Dokysh$ '

#endregion

Dockysh().cmdloop()