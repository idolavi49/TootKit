from urllib.request import urlopen
import hashlib

def tryOpenFile(passwordlist):
        try:
            passfile = open(passwordlist, "r")
            return passfile

        except:
            print("No such file")
            quit()



# md5Hash = "2e3817293fc275dbee74bd71ce6eb056".upper()
# passwordlist = "./passwords.txt"
md5Hash = input("Enter a md5 hash: ").upper()
passwordlist = input("Enter the password file: ")
print('running file check...')
file = tryOpenFile(passwordlist)

for password in file:
    enc_word = password.encode('utf-8')
    md5temp = hashlib.md5(enc_word.strip()).hexdigest().upper()
    if md5Hash == md5temp:
        print('password found: ' + password)
        quit()

print('password is not on list')