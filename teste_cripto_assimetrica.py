import rsa

message = 'teste de cripto assimetrica'

samuel_pu, samuel_pr = rsa.newkeys(2048)
print(samuel_pu, samuel_pr)

encryption = rsa.encrypt(message.encode(), samuel_pu)

print(f"Mensagem criptografada: {encryption}")

decryption = rsa.decrypt(encryption, samuel_pr).decode()

print(f"Mensagem descriptografada: {decryption}")
