#! python


secret = ["williamroscoe"]
secret_phrases = ["7941","7950","010604"]

def cipheriser(secret, secret_phrases):
    for i,sp in enumerate(secret_phrases):
        enc  = []
        for c in sp:
            enc.append(secret[0][int(c)])
        print(''.join(enc))


cipheriser(secret, secret_phrases)