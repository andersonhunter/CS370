# Name: Hunter Anderson
# Email: andershu@oregonstate.edu
# Date: 16 Nov 2025

import qrcode
import time
import os, base64, hmac, hashlib, struct, sys


TIMESTEP = 30
ISSUER = "Hunter Anderson CS332 OTP"
ACCOUNT = "test@gmail.com"

def generate_totp(secret):
    """Generate the TOTP"""
    # b32 decode the secret into the key
    key = base64.b32decode(secret)
    # Calculate t and encode
    t = int(time.time() // TIMESTEP)
    t = struct.pack(">Q", t)
    # Create hash
    digest = hmac.new(key, t, hashlib.sha1).digest()
    # Truncate hash
    offset = digest[-1] & 0x0F
    p = digest[offset:offset+4]
    n = struct.unpack(">I", p)[0] & 0X7FFFFFFF
    code = n % 1000000
    return code


def generate_secret():
    # Generate the secret
    secret = base64.b32encode(os.urandom(20)).decode()
    # Store it locally for later use
    with open("secret.txt", "w") as f:
        f.write(secret)
    return secret


def generate_code():
    # Generate the secret
    secret = generate_secret()
    # Generate the URI
    uri = f'otpauth://totp/{ISSUER}:{ACCOUNT}?secret={secret}&issuer={ISSUER}&period=30'
    # Create and save QR code
    qr = qrcode.make(uri)
    qr.save("totp_qr.png")
    print("QR Saved as \'totp_qr.png\'")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--generate-qr':
            print("Generating QR code!")
            generate_code()
        elif sys.argv[1] == '--get-otp':
            print("Generating OTP from saved secret")
            try:
                with open("secret.txt", 'r') as f:
                    secret = f.read().strip()
                    otp = generate_totp(secret)
                    print(f"OTP = {otp:06d}")
            except FileNotFoundError:
                print("Error: No OTP secret found, try generating a QR code first!")
        else:
            print("Error: Unknown command line arg supplied, please try with \'--get-otp\' or \'--generate-qr\'")
