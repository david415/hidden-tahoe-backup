#!/usr/bin/env python

import nacl.secret
import nacl.utils
import nacl.hash
import getpass
import binascii
import argparse
import sys
import os.path
import re

def encrypt(plaintext, nonce, key):
    box = nacl.secret.SecretBox(key)
    return box.encrypt(plaintext, nonce)

def decrypt(ciphertext, nonce, key):
    box = nacl.secret.SecretBox(key)
    return box.decrypt(ciphertext, nonce)

def encryptFile(filename):
    """Prompt user for a passphrase and use that as key to encrypt the file
    """
    if os.path.isfile(filename + '.secretbox'):
        print "%s already exists" % (filename + '.secretbox')
        sys.exit(-1)

    passphrase = getpass.getpass("Enter passphrase:")
    key = nacl.hash.sha256(passphrase, encoder=nacl.encoding.RawEncoder)

    # XXX never reuse a nonce; is this good enough? nope.
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)

    plaintext_fh = open(filename, 'r')
    plaintext = plaintext_fh.read()
    plaintext_fh.close()

    ciphertext = encrypt(plaintext, nonce, key)
    fh_ciphertext = open(filename + '.secretbox', 'w')
    fh_ciphertext.write(ciphertext)
    fh_ciphertext.close()

def decryptFile(filename):

    if not filename.endswith('.secretbox'):
        print "Filename must end in .secretbox"
        sys.exit(-1)

    plaintext_file = url = re.sub('\.secretbox$', '', filename)

    if os.path.isfile(plaintext_file):
        print "%s already exists" % (plaintext_file,)
        sys.exit(-1)

    passphrase = getpass.getpass("Enter passphrase:")
    key = nacl.hash.sha256(passphrase, encoder=nacl.encoding.RawEncoder)
    fh = open(filename, 'r')
    nonce = fh.read(24)
    ciphertext = fh.read()
    fh.close()

    plaintext = decrypt(ciphertext, nonce, key)
    fh_plaintext = open(plaintext_file, 'w')
    fh_plaintext.write(plaintext)
    fh_plaintext.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--decrypt', dest='decrypt', default=False, action="store_true", help="perform secretBox decrypt operation")
    parser.add_argument('--encrypt', dest='encrypt', default=False, action="store_true", help="perform secretBox encrypt operation")
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    files = args.args

    if args.encrypt and args.decrypt:
        print "Must specify either encrypt or decrypt."
        parser.print_help()
        return -1

    for file in files:
        if args.decrypt:
            decryptFile(file)
        else:
            encryptFile(file)

    return 0

if __name__ == '__main__':
    sys.exit(main())
