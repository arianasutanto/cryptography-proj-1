import random

def generate_monoalphabetic_key():
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    shuffled_alphabet = alphabet.copy()
    random.shuffle(shuffled_alphabet)
    return dict(zip(alphabet, shuffled_alphabet))

def encode_with_monoalphabetic(text, key):
    encoded_text = ''
    for char in text:
        if char.lower() in key:
            if char.islower():
                encoded_text += key[char]
            else:
                encoded_text += key[char.lower()].upper()
        else:
            encoded_text += char
    return encoded_text

def main():
    plaintext = input("Enter the plaintext: ")

    # Generate a random monoalphabetic key
    key = generate_monoalphabetic_key()

    # Encode the plaintext using the generated key
    ciphertext = encode_with_monoalphabetic(plaintext, key)

    print("Ciphertext:", ciphertext)
    print("Key:", key)

if __name__ == "__main__":
    main()
