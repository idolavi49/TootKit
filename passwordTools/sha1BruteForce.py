from urllib.request import urlopen
import hashlib

sha1Hash = input("Enter a sha1 hash: ").upper()
print('running check in our database...')

# get all the passwords from the list online
passlist = str(urlopen('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt').read(), 'utf-8')

# check if one of the passwords match to the wanted hash (sha1 hash)
for password in passlist.split('\n'):
    hashguess = hashlib.sha1(bytes(password, 'utf-8')).hexdigest().upper()
    if hashguess == sha1Hash:
        print('[+] The password is: ' + str(password))
        quit()

print('password is not on list')