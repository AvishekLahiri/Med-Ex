import random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

class Crypt:

    def __init__(self, salt='SlTKeYOpHygTYkP3'):
        self.salt = salt.encode('utf8')
        self.enc_dec_method = 'utf-8'

    def encrypt(self, str_to_enc, str_key):
        try:
            aes_obj = AES.new(str_key, AES.MODE_CFB, self.salt)
            hx_enc = aes_obj.encrypt(str_to_enc.encode('utf8'))
            mret = b64encode(hx_enc).decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Encryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError('Encryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                raise ValueError(value_error)

def encode(string):

	# LEVEL 0 - Can we add a Vernam XOR Cipher here without giving different outputs every time?	

	# LEVEL 1 - Convert the string into a string of ASCII numerals and random seed to get a float
	new_str = ""
	for c in string:
		new_str = new_str + str(ord(c))
	pwd = int(new_str)
	random.seed(pwd)
	string = str(random.random())
	
	# LEVEL 2 - AES encrypt the string using pycrypto
	crpt = Crypt()
	string = crpt.encrypt(string, string[:16])

	# LEVEL 3 - Convert the float to a string of squares of ASCII numerals, split into two and add, then random seed to get a float, then concatenate with itself and shuffle
	new_str = ""
	for c in string:
		new_str = new_str + str(ord(c)*ord(c))
	pwd = int(new_str[:int(len(new_str)/2)])+int(new_str[int(len(new_str)/2):])
	random.seed(pwd)
	string = str(random.random())+str(random.random())
	x = list(string)
	random.shuffle(x)
	string = ''.join(x)

	# LEVEL 4 - AES encrypt using pycrypto
	string = crpt.encrypt(string, string[:24])

	# LEVEL 5 - Convert this string into a string of ASCII numerals and random seed as a given equation to get a float, then concatenate with itself thrice and shuffle
	new_str = ""
	for c in string:
		new_str = new_str + str(ord(c))
	pwd = int(new_str)*int(new_str) - int(new_str) + 2*int(new_str[:int(len(new_str)/2)])
	random.seed(pwd)
	string = str(random.random())+str(random.random())+str(random.random())+str(random.random())
	x = list(string)
	random.shuffle(x)
	string = ''.join(x)

	# LEVEL 6 - AES encrypt using pycrypto
	string = crpt.encrypt(string, string[:32])

	# LEVEL 7 - Random Shuffle
	x = list(string)
	random.shuffle(x)
	string = ''.join(x)

	# Level 8 - May be we can also add a Vernam XOR Cipher layer here?

	return string