import pexpect
import optparse

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

# connect into the server with ssh using arguements, including the first time with rsa key warning
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
            child.expect(PROMPT)
            return child
    if ret == 2:
        child.sendline(password)
        child.expect(PROMPT)
        return child


def main():

    # host = "10.0.0.8"
    # user = "msfadmin"
    # password = "msfadmin"
    # command = 'ls'

    # Create argumentes
    parser = optparse.OptionParser('Usage of program: ' + '-H <target host> -u <targets username> -p <target passwords> -c <command to execute>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-u', dest='tgtUser', type='string', help='specify target username')
    parser.add_option('-p', dest='tgtPass', type='string', help='specify target password')
    parser.add_option('-c', dest='tgtCommand', type='string', help='specify command to execute on host')
    (options, args) = parser.parse_args()

    # Set arguments
    host = options.tgtHost
    user = options.tgtUser
    password = options.tgtPass
    command = options.tgtCommand

    # Arguments validation
    if (host == None) and (user == None) and (password == None) and (command == None):
        print(parser.usage)
        exit(0)
    elif (host == None) or (user == None) or (password == None) or (command == None):
        parser.print_help()
        exit(0)

    child = connect(user, host, password)
    hostName = get_hostname(child,'hostname', user)
    send_command(child, command, user, hostName)

main()
