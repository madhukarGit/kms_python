
#pip install pycryptodome

from Crypto.Cipher import AES
#import itertools

plain_text = "This is the text"
key = "0361231230000000"
key = bytes(key, "UTF-8")
cipher = AES.new(key, AES.MODE_ECB)
    

def encrypt(plain_text):
    print("Encryption Cipher: ", cipher)
    # When there is no padding, the block size must equal the cipher length
    # Padding is necessary for texts with length different from 16 bytes
    cbytes = cipher.encrypt(bytes(plain_text, "UTF-8"))
    return cbytes
 
result = encrypt(plain_text,key)  

print(result)

decrypt_result = cipher.decrypt(result)
print(decrypt_result.decode("utf-8"))

#b'U\x1d\xfd(8=\xfc\x89\xcd\xac#\xd9\xd1\xb5\xf2\xf1'