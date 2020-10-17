import ftplib
import optparse

def anonLogin(host):
    try:
            ftp = ftplib.FTP(host, timeout=100)
            ftp.login('anonymous', 'anonymous')
            print("[+] " + host + ' FTP anonymous login succeeded - machine is vulenrable.')
            ftp.quit()
            return True

    except Exception as e:
            print("[-] " + host + ' FTP Anonymous Login Failed.')


parser = optparse.OptionParser(
    'Usage of program: ' + '-H <target host>')
parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
(options, args) = parser.parse_args()

host = options.tgtHost

if host == None:
    print(parser.usage)
    exit(0)

anonLogin(host)