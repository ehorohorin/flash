from ticket import Ticket
import qrcode
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

t = Ticket()
data = json.dumps(t.__dict__, indent=4, sort_keys=True, default=str)
data = bytearray(data, 'utf-8')
img = qrcode.make(data)
img.save("json.png", format='PNG')


private_key = rsa.generate_private_key(public_exponent=65537,
                                       key_size=2048,
                                       backend=default_backend()
                                       )


from cryptography.hazmat.primitives import serialization
private_key_text = private_key.private_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PrivateFormat.TraditionalOpenSSL,
   encryption_algorithm=serialization.NoEncryption()
)
with open("private_key.rsa", "wb") as pkey:
    pkey.write(private_key_text)




public_key = private_key.public_key()
public_key_text = public_key.public_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open("public_key.rsa", "wb") as okey:
    okey.write(public_key_text)

digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
digest.update(data)
data = digest.finalize()
#
signature = private_key.sign(
    data,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
print(signature.hex())
