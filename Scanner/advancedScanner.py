from socket import *
import optparse
import threading

def retBanner(sock):
    try:
        banner = str(sock.recv(1024)).strip("b'{\}rn")
        return banner
    except:
        banner = "Coult not identity"
        return banner

# check if a specific port is open
def connScan(tgtHost, tgtPort, lock):
    try:
        with lock:
                sock = socket(AF_INET, SOCK_STREAM)
                sock.connect((tgtHost, tgtPort))
                banner = retBanner(sock)
                print('[+] %d/tcp Open  %s' % (tgtPort,banner))
    except:
            print('[+] %d/tcp Cloesd' % tgtPort)
    finally:
        sock.close()

# Scan the ports on the target host
def portScan(tgtHost, tgtPorts):
    try:
            tgtIP = gethostbyname(tgtHost)
    except:
            print('Unkown host %s' % tgtHost)

    try:
            tgtName = gethostbyaddr(tgtIP)
            print('[+] Scan Results For: ' + tgtName[0])
    except:
            print('[+] Scan Results for ' + tgtIP)

    setdefaulttimeout(1)
    lock = threading.Lock()
    threads = []
    for tgtPort in tgtPorts:
        t = threading.Thread(target=connScan, args=(tgtHost, int(tgtPort), lock,))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

# Start the program with help arguments
def main():
    parser = optparse.OptionParser('Usage of program: ' + '-H <target host> -p <target ports>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPorts', type='string', help='specify target port seperated by comma')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPorts).split(',')
    # tgtHost= "10.0.0.8"
    # tgtPorts = ["21","22","80"]

    if (tgtHost == None) and (tgtPorts[0] == 'None'):
        print(parser.usage)
        exit(0)
    elif (tgtHost == None) and (tgtPorts[0] != 'None'):
        parser.print_help()
        exit(0)
    # elif (tgtHost != None) and (tgtPorts[0] == 'None'):
    #     parser.print_help()
    #     exit(0)
    portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
    main()