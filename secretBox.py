#!/usr/bin/env python

import nacl.secret
import nacl.utils
import nacl.hash
import nacl.encoding
import getpass
import binascii
import argparse
import sys
import os.path
import re

def encrypt(plaintext, nonce, key):
    box = nacl.secret.SecretBox(key)
    return box.encrypt(plaintext, nonce, encoder=nacl.encoding.Base64Encoder)

def decrypt(ciphertext, nonce, key):
    box = nacl.secret.SecretBox(key)
    return box.decrypt(ciphertext, nonce)

def promptlyEncryptFile(filename):
    """
    Encrypt file and return ciphertext.
    Prompt twice to set a passphrase/key.
    """
    passphrase = getpass.getpass("Enter passphrase:")
    passphrase2 = getpass.getpass("Enter passphrase:")
    if passphrase != passphrase2:
        print "passphrases don't match"
        sys.exit(-1)

    key = nacl.hash.sha256(passphrase, encoder=nacl.encoding.RawEncoder)

    # XXX never reuse a nonce; is this good enough? yeeup.
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    
    plaintext_fh = open(filename, 'r')
    plaintext = plaintext_fh.read()
    plaintext_fh.close()

    return encrypt(plaintext, nonce, key)

def promptlyDecryptFile(filename):
    """
    Decrypt file and return plaintext.
    Prompt for the passphrase.
    """
    passphrase = getpass.getpass("Enter passphrase:")
    key = nacl.hash.sha256(passphrase, encoder=nacl.encoding.RawEncoder)

    # XXX obviously for big ass files this will not work
    fh = open(filename, 'r')
    bin_ciphertext = binascii.a2b_base64(fh.read())
    fh.close()

    nonce = bin_ciphertext[0:24]
    ciphertext = bin_ciphertext[24:]

    return decrypt(ciphertext, nonce, key)


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

    if not args.encrypt and not args.decrypt:
        print "Must specify either encrypt or decrypt."
        parser.print_help()
        return -1

    for filename in files:
        if args.decrypt:
            if not filename.endswith('.secretbox'):
                print "Filename must end in .secretbox"
                sys.exit(-1)

            plaintext_file = url = re.sub('\.secretbox$', '', filename)

            if os.path.isfile(plaintext_file):
                print "%s already exists." % plaintext_file
                sys.exit(-1)

            plaintext = promptlyDecryptFile(filename)

            fh_plaintext = open(plaintext_file, 'w')
            fh_plaintext.write(plaintext)
            fh_plaintext.close()
        else:
            ciphertext_file = filename + '.secretbox'
            if os.path.isfile(ciphertext_file):
                print "%s already exists" % (ciphertext_file,)
                sys.exit(-1)

            ciphertext = promptlyEncryptFile(filename)

            fh_ciphertext = open(ciphertext_file, 'w')
            fh_ciphertext.write(ciphertext)
            fh_ciphertext.close()

    return 0

if __name__ == '__main__':
    sys.exit(main())
