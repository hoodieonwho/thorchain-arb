from xchainpy_crypto import crypto

words = crypto.generate_mnemonic()
out = open("secret/real_mnemonic", "w+")
out.write(words)
out.close()