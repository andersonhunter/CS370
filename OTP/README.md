To run:
    1. Make sure the qrcode package is installed, i.e. run `pip install qrcode[pil]` (or whatever package manager you like!)
    2. If this is the first time running, generate a QR code with `python3 andershu_otp.py --generate-qr`
        2a. The QR code should now be saved in the cwd as `totp_qr.png`, open and scan into GA
    3. Check current OTP against the one stored in GA by opening GA and running `python3 andershu_otp.py --get-otp` in whatever CLI you're on right now
    4. Check the OTP in GA against the one printed to the CLI

Implementation information:

This implementation uses sys to grab command line flags, then determines which functions to run based on them.

If the user requests a QR code with --generate-qr, it generates the client secret with the base64 library on a random number, then writes it to a local file called `"secret.txt"` (definitely not the most secure method, but without going through the stress of creating a Docker instance and storing it as an env variable, this works!)
The secret is then used to generate the URI, and the URI is used to make the QR code, which is saved as `"totp_qr.png"` locally.

If the user requests the OTP with --get-otp, the program checks if the secret.txt file has been saved, and, if so, opens it, reads in the secret, then uses that secret to call its generate_totp function. 

The generate_totp function creates a byte-encoded key from the secret, then calculates T from the current time floor'd with the 30-second timestep, which is then byte-encoded. A hash digest using HMAC SHA1 is created such that digest = (HMAC-SHA-1(Key, T)). The digest is then truncated to be 6 digits. This 6-digit code is 0-padded if necessary, and then printed to the CLI. 

GA will change the password every 30 seconds, so the OTP printed to the CLI will only be valid for 30 seconds, at which point the program will need to be run again. 

