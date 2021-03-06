import re
from cryptography.fernet import Fernet

# must make sure to install cryptography package (pip install cryptography)
# This file consisted of tests and exercises for me to both learn how to implement regular expressions in Python,
# and to figure out the regular expressions for the main categories of information we were expecting.

# This section dealt specifically with encrypting the regular expressions with the Fernet Crypography package
# This was going to be used to translate the string regular expression into integers, so that the pickle learner
# could utilize it, but this was never used, both because it cannot encrypt into an integer, and because it was
# deemed unnecessary for the project.
key = Fernet.generate_key()
cipher_suite = Fernet(key)
cipher_text = cipher_suite.encrypt(b"A really secret message. Not for prying eyes.") #encryption
plain_text = cipher_suite.decrypt(cipher_text) #decryption

cipher_text_time = cipher_suite.encrypt(b"([0-2]\d:[0-5]\d:[0-5]\d)(AM|PM)")
cipher_text_date = cipher_suite.encrypt(b"([0-1]\d/[0-3]\d/\d{4})")
cipher_text_latitude = cipher_suite.encrypt(b"(\+|\-)?(\d{2}\.\d+.(N|S))")
cipher_text_longitude = cipher_suite.encrypt(b"(\+|\-)?(\d{2}\.\d+.(E|W))")
cipher_text_email = cipher_suite.encrypt(b".+@.+\.\w+")

# These are the regular expressions for the categories as named by the variable names. These were pretty extensively
# tested for accuracy, with some of the tests below.
time = r"(([0-1]\d|2[0-3]):[0-5]\d:[0-5]\d)(AM|PM)?" #regex for time, date, and latitude
date = r"((0\d|1[0-2])/([0-2]\d|3[0-1])/(\d{2}|\d{4})|([0-2]\d|3[0-1])/(0\d|1[0-2])/(\d{2}|\d{4}))"
date_time = r"((0\d|1[0-2])/([0-2]\d|3[0-1])/(\d{2}|\d{4})|" \
            r"([0-2]\d|3[0-1])/(0\d|1[0-2])/(\d{2}|\d{4})) (([0-1]\d|2[0-3]):[0-5]\d:[0-5]\d)(AM|PM)?"
latitude = r"(\+|\-)?(\d{2}\.\d+(N|S))"
longitude = r"(\+|\-)?(([0-8\d|90|1[0-7]\d|180)\.\d+(E|W))"
email = r".+@.+\.\w+"
phone = r"(\()?\d{3}(\))?( )?\d{3}(-)?\d{4}(\d{4})?"

# Tests for the regular expressions for accuracy
if re.search(time, "09:59:00 PM"):
    print ("time OK")

if re.search(date, "01/30/2015"):
    print("date OK")

if re.search(date_time, "30/01/2013 00:28:56"):
    print("date_time OK")

if re.search(latitude, "+54.9864N"):
    print ("latitude OK")

if re.search(longitude, "-133.9864E"):
    print ("longitude OK")

if re.search(phone, "(908) 797-7554"):
    print ("phone OK")

