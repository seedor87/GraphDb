import re
# from cryptography.fernet import Fernet
#
#
#
# #must make sure to install cryptography package (pip install cryptography)
#
# key = Fernet.generate_key()
# cipher_suite = Fernet(key)
# cipher_text = cipher_suite.encrypt(b"A really secret message. Not for prying eyes.") #encryption
# plain_text = cipher_suite.decrypt(cipher_text) #decryption

time = r"([0-2]\d:[0-5]\d:[0-5]\d)(AM|PM)" #regex for time, date, and latitude
date = r"([0-1]\d/[0-3]\d/\d{4})"
latitude = r"(\+|\-)?(\d{2}\.\d+.(N|S))"
longitude = r"(\+|\-)?(\d{2}\.\d+.(E|W))"
email = r".+@.+\.\w+"

if re.search(time, "09:54:00PM"):
    print ("time OK")

if re.search(date, "09/24/1990"):
    print("date OK")

if re.search(latitude, "+54.9864.N"):
    print ("latitude OK")

if re.search(longitude, "-33.9864.E"):
    print ("longitude OK")