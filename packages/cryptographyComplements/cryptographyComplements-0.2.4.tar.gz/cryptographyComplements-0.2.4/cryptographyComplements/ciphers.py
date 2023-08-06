def MonoalphabeticCipher():
    "This function generates a cipher using the monoalphabetic encryption"
    import string, random
    elements = string.ascii_letters + string.digits + string.punctuation + "àèéìòù" + " "
    cipher = {elements[i]: None for i in range(len(elements))}

    already_sorted = []
    element_sorted = None

    for i in cipher.keys():
        while True:
            sort = random.randint(0, len(elements) -1)
            if sort in already_sorted:
                continue
            else:
                break

        already_sorted.append(sort)
        element_sorted = elements[sort]

        cipher[i] = element_sorted

    writeCipher(cipher)
    return cipher


def CaesarCipher():
    "This functions generate the Caesar Cipher with a random sequence, or if enabled by the user in the script, the original one."
    import string, random
    elements = string.ascii_letters + string.digits + string.punctuation + "àèéìòù" + " "
    cipher = {elements[i]: None for i in range(len(elements))}

    # sequence = 3 # use this for the original Caesar cipher
    sequence = random.randint(0, len(cipher)) # use this for a random Caesar cipher

    modulo = int(len(cipher))
    for i in cipher.keys():
        index = sequence % modulo
        cipher[i] = elements[index]
        sequence += 1

    writeCipher(cipher)
    return cipher
    
def writeCipher(cipher):
    "This function writes a cipher, from a one executed, into a text file."
    
    import json
    with open("cipher.txt","w") as file:
        json.dump(cipher, file)