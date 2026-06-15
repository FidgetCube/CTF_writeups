#!/usr/bin/env python3
"""
Created for NSWPol HTB CTF challenge Imposter (crypto)

This script works for any AES CTR with a weak implementation such as:
- AES-CTR nonce reuse
- stream cipher key reuse
- reused one-time pads
- XOR keystream recovery attacks

Requires known plaintext, resulting known ciphertext, which will recover the keystream, and then the target ciphertext to decrypt
"""

from binascii import unhexlify


def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


known_plaintext = input("Known plaintext (Created password): ").encode()

known_ciphertext = unhexlify(
    input("Known ciphertext (resulting cipher in hex): ").strip()
)

target_ciphertext = unhexlify(
    input("Target ciphertext to decrypt (hex): ").strip()
)

keystream = xor_bytes(known_ciphertext, known_plaintext)

print(f"\n[+] Recovered keystream: {keystream.hex()}")

plaintext = xor_bytes(target_ciphertext, keystream)

try:
    print(f"[+] Decrypted plaintext: {plaintext.decode()}")
except UnicodeDecodeError:
    print(f"[+] Plaintext bytes: {plaintext.hex()}")