from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def preenchimento(plaintext):
    return plaintext + b"\0" * (AES.block_size - len(plaintext) % AES.block_size)


key = b'4c5c4f9dcad90930372885895168d87a'
IV = b'ad7903492be581e4'
print(IV)
mode = AES.MODE_CBC
encryptor = AES.new(key, mode, IV=IV)
text_original = 'eu amo minha vida'
text = bytes(text_original, 'utf-8')
text = preenchimento(text)
ciphertext = encryptor.encrypt(text)
print(f"Texto criptografado: {ciphertext}")
# ------------------------------------------------------


decryptor = AES.new(key, mode, IV=IV)
plaintext = decryptor.decrypt(ciphertext)
plaintext = str(plaintext)
final_texto_plano = len(text_original) + 2

print(f"Texto descriptografado: {plaintext[2:final_texto_plano]}")
