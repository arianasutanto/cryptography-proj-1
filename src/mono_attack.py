import random
import string
from os import path

# GLOBAL
DICT_PATH = path.abspath(path.join(__file__, "..", "plaintext_dictionary.txt"))
PLAINTEXT_PATH = path.abspath(path.join(__file__, "..", "candidate_files"))
common_english_frequency = {'E' : 12.0, 
                        'T' : 9.10, 
                        'A' : 8.12, 
                        'O' : 7.68, 
                        'I' : 7.31, 
                        'N' : 6.95, 
                        'S' : 6.28, 
                        'R' : 6.02, 
                        'H' : 5.92, 
                        'D' : 4.32, 
                        'L' : 3.98,
                        'U' : 2.88,
                        'C' : 2.71,
                        'M' : 2.61,
                        'F' : 2.30,
                        'Y' : 2.11,
                        'W' : 2.09,
                        'G' : 2.03,
                        'P' : 1.82,
                        'B' : 1.49,
                        'V' : 1.11,
                        'K' : 0.69,
                        'X' : 0.17,
                        'Q' : 0.11,
                        'J' : 0.10,
                        'Z' : 0.07 }

for key, value in common_english_frequency.items():
        common_english_frequency[key] = value / 100

LETTER_FREQUENCY = {"Common Frequency": common_english_frequency}
candidate_count = 0

def test_freq():
    """Simple test to check if the sum of the squares of the probabilities is 0.065."""
    freq_sum = 0

    for letter, freq in LETTER_FREQUENCY['Common Frequency'].items():
        prob = freq / 100
        freq_sum += prob ** 2

    print(freq_sum)


def freq_message(plaintext):
    """Find the frequency of each letter in the message and add it to the global list."""
    # Find the probability of each letter in the message
    letter_counts = [0] * 26
    total_letters = 0
    for char in plaintext:
        if char.isalpha():
            total_letters += 1
            letter_counts[ord(char.upper()) - ord('A')] += 1

    letter_prob = [count / total_letters for count in letter_counts]

    # Make a dictionary of the letter probabilities
    letter_prob = dict(zip([chr(i + ord('A')) for i in range(26)], letter_prob))
    
    # Add the letter probabilities to the global list
    global LETTER_FREQUENCY
    global candidate_count
    candidate_count += 1
    LETTER_FREQUENCY[f"pt{candidate_count}"] =  letter_prob

    # Print characters in letter_prob in order of probability
    #print("\nCharacters in order of probability: ", sorted(letter_prob, key=letter_prob.get, reverse=True))

    # Find the sum of the squares of the probabilities
    freq_sum = 0
    for prob in letter_prob.values():
        freq_sum += prob ** 2
    
    #print("Sum of the squares of the probabilities: ", freq_sum)

def generate_monoalphabetic_key():
    """Generate a monoalphabetic key by shuffling the alphabet."""
    alphabet = list(string.ascii_lowercase)
    random.shuffle(alphabet)
    return ''.join(alphabet)

def encrypt(text, key):
    """Encrypt the candidate plaintext using the generated key."""
    # Convert input text to lowercase
    text = text.lower()
    encrypted_text = ''
    for char in text:
        if char.isalpha():
            # Encrypt only alphabetic characters
            idx = ord(char) - ord('a')
            encrypted_text += key[idx]
        else:
            # Leave non-alphabetic characters unchanged
            encrypted_text += char
    return encrypted_text

def improved_attack(ciphertext):
    """Perform an improved attack to find the best shifts."""
    # Create a frequency table for ciphertext letters
    letter_counts = [0] * 26
    total_letters = 0
    for char in ciphertext:
        if char.isalpha():
            idx = ord(char.lower()) - ord('a')
            letter_counts[idx] += 1
            total_letters += 1

    # Calculate letter frequency of ciphertext and store in a dictionary
    cipher_freq = {chr(i + ord('A')): count / total_letters for i, count in enumerate(letter_counts)}
    print(f"Cipher Frequency: {cipher_freq}\n")

    match_count = 0
    character_mapping = {}
    found_freq_key = None
    # Compare the frequency of the ciphertext with frequencies in our global list
    for key, value in LETTER_FREQUENCY.items():
        print(f"Key: {key}, Value: {value}\n")
        for letter, freq in value.items():
            #print(f"Letter: {letter}, Frequency: {freq}\n")
            if freq in cipher_freq.values() and match_count < 5:
                print(f"Letter: {letter}, Frequency: {freq}\n")
                cipher_letter = [k for k, v in cipher_freq.items() if v == freq]
                print(f"Cipher Letter: {cipher_letter}, Cipher Frequency: {cipher_freq[cipher_letter[0]]}\n")
                print(f"Match found from freq table {key}\n")
                found_freq_key = key # This is the frequency table that matches the frequency of our ciphertext
                character_mapping[letter] = cipher_letter # Map the letter to the cipher letter
                match_count += 1
            else:
                print(f"Letter: {letter}, Frequency: {freq}\n")
                print(f"No match found from freq table {key}\n")
                break
        
        # Check if we have found a matching frequency table
        if found_freq_key:
            break
    
    # Create an expected frequency table based on the frequency table that matches the frequency of our ciphertext
    expected_frequencies = list(LETTER_FREQUENCY[found_freq_key].values())

    # Create a list of the differences between the expected and actual frequencies
    with open(PLAINTEXT_PATH + "/" + f"{found_freq_key}.txt", "r") as file:
        plaintext_body = file.read()
        return plaintext_body, character_mapping


if __name__ == "__main__":

    # Read a file of candidate plaintexts
    file_body = []
    candidate_num = 2
    with open(DICT_PATH, "r") as file:
        for line in file:
            file_body.append(line.strip())
        file_body = list(filter(None, file_body))
        #print(file_body, len(file_body))

    # Get the frequency of each letter in each plaintext
    for plaintext in file_body:
        freq_message(plaintext)
    
    # Print the global list of letter frequencies
    #print(LETTER_FREQUENCY)

    # Generate the mono-alphabetic key
    key = generate_monoalphabetic_key()
    print(f"Generated key: {key}\n")

    # Candidate plaintext
    print(f"Candidate plaintext: {file_body[candidate_num]}\n")

    # Encrypt the candidate plaintext
    encrypted_message = encrypt(file_body[candidate_num], key)
    print(f"Encrypted message: {encrypted_message}\n")

    # Perform improved attack to find the plaintext it matches
    plaintext_guess, char_mapping = improved_attack(encrypted_message)

    # Print the plaintext guess with character mapping
    print(f"Plaintext guess: {plaintext_guess}\n")
    print(f"Character mapping: {char_mapping}\n")
    print("End of program.")





