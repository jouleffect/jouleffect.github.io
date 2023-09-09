"""
Caesar.py

This script takes as input a shift key and a plaintext and returns the relative ciphertext

args:
	-k : shift key
	-t : plaintext

"""

import argparse
import string

parser = argparse.ArgumentParser()
parser.add_argument('-k', help="The key of caesar cipher (number of shift)", required=True)
parser.add_argument('-t', help="The plaintext", required=True)

args = parser.parse_args()

key_shift = int(args.k)
plaintext = args.t

clear_alph = string.ascii_lowercase
cipher_alph = clear_alph[key_shift:] + clear_alph[:key_shift]
table = str.maketrans(clear_alph,cipher_alph)

ciphertext = plaintext.translate(table)

print(ciphertext)
