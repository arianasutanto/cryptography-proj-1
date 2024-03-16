import random
import string
from os import path
import numpy as np
from scipy.stats import entropy
from collections import Counter


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
                        'Z' : 0.07,
                        ' ' : 18.00}

for key, value in common_english_frequency.items():
        common_english_frequency[key] = value / 100

LETTER_FREQUENCY = {"Common Frequency": common_english_frequency}
candidate_count = 0

BIGRAM = {}

def test_freq(cipher_freq=None):
    """Simple test to check if the sum of the squares of the probabilities is 0.065."""
    #freq_sum = 0
    if cipher_freq:
        freq_sum = 0
        for freq in cipher_freq.values():
            freq_sum += (freq) ** 2
        #print(f"Sum of the squares of the probabilities for the cipher frequency: {freq_sum}\n")
    else:
        for candidate, values in LETTER_FREQUENCY.items():
            freq_sum = 0
            for letter, freq in values.items():
                #print(f"Letter: {letter}, Frequency: {freq}\n")
                freq_sum += (freq) ** 2
                #print(freq_sum)
            
            #print(f"Sum of the squares of the probabilities for {candidate}: {freq_sum}\n")
    #print(freq_sum)

def coin_flip(prob, ciphertext):
    """Use coin flip to insert random characters in ciphertext."""
    num_of_rand_chars = prob * len(ciphertext)
    cipher_pointer = 0
    message_pointer = 0
    counter = 0
    new_ciphertext = ""
    while cipher_pointer < (len(ciphertext) + num_of_rand_chars):
        coin_value = random.uniform(0,1)
        #print(f"Coin value: {coin_value}\n")
        if prob <= coin_value <= 1 or counter == num_of_rand_chars:
            # Encrypt the candidate plaintext using the generated key
            new_ciphertext += ciphertext[message_pointer]
            message_pointer += 1
        elif 0 <= coin_value < prob and counter < num_of_rand_chars:
            rand_char = random.choice(" abcdefghijklmnopqrstuvwxyz")
            new_ciphertext += rand_char
            counter += 1
        cipher_pointer += 1

    print(f"Message pointer: {message_pointer}\nCipher pointer: {cipher_pointer}\n")
    return new_ciphertext

def bigram(plaintext_name, plaintext):
    global BIGRAM
    bigram_test = plaintext
    res = Counter(bigram_test[idx : idx + 2] for idx in range(len(plaintext) -1))
    BIGRAM[plaintext_name] = res
    print(f"Bigram Frequency for {plaintext_name}: {res}")

def random_char_insertion(random_prob, ciphertext):
    """Insert a random character into the ciphertext based on a random probability."""
    # list of chars to pick from
    chars = "abcdefghijklmnopqrstuvwxyz "

    ciphertext_length = len(ciphertext)
    print(f"Length of ciphertext (pre-randomness): {ciphertext_length}\n")
    num_of_rand_chars = int(random_prob * ciphertext_length)
    for _ in range(num_of_rand_chars):
        rand_char = random.choice(chars)
        rand_index = random.randint(0, ciphertext_length - 1)
        ciphertext = ciphertext[:rand_index] + rand_char + ciphertext[rand_index:]
        ciphertext_length += 1
    print(f"Random character insertion: {ciphertext}\n")
    print(f"Length of ciphertext: {len(ciphertext)}\n")
    return ciphertext

def freq_message(plaintext):
    """Find the frequency of each letter in the message and add it to the global list."""
    # Find the probability of each letter in the message
    letter_counts = [0] * 27
    total_letters = 0
    for char in plaintext:
        if char.isalpha():
            total_letters += 1
            letter_counts[ord(char.upper()) - ord('A')] += 1
        elif char == ' ':
            total_letters += 1
            letter_counts[26] += 1

    letter_prob = [count / total_letters for count in letter_counts]

    # Make a dictionary of the letter probabilities
    letter_prob = dict(zip([chr(i + ord('A')) for i in range(27)], letter_prob))
    letter_prob[' '] = letter_prob.pop('[')
    
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
    alphabet.append(' ')
    random.shuffle(alphabet)
    return ''.join(alphabet)

def encrypt(text, key):
    """Encrypt the candidate plaintext using the generated key."""
    # Convert input text to lowercase
    alphabet = list(string.ascii_lowercase)
    alphabet.append(' ')
    text = text.lower()
    encrypted_text = ''
    space_idx = key.index(' ')
    char_map_space = alphabet[space_idx]
    #print(f"Space index: {space_idx}\n")
    #print(f"Character mapping for space: {char_map_space}\n")
    for char in text:
        if char.isalpha():
            # Encrypt alphabetic characters and spaces     
            if char == char_map_space:
                encrypted_text += ' '
                continue
            idx = ord(char) - ord('a')
            encrypted_text += key[idx]
        elif char == ' ':
            encrypted_text += key[-1]
    return encrypted_text

def compare_distributions(cipher_dist, candidate_dist):
    """Compare the distribution of letters in the candidate plaintext with the distribution of letters in the ciphertext."""
    #print(f"Cipher Distribution: {cipher_dist}\n")
    #print(f"Candidate Distribution: {candidate_dist}\n")

    # Create a list of the differences between the expected and actual frequencies
    cipher_freq = sorted(list(cipher_dist.values()))
    candidate_freq = sorted(list(candidate_dist.values()))

    sum_of_diffs = 0
    for i in range(len(cipher_freq)):
        #print(f"Cipher Frequency: {cipher_freq[i]}\n")
        #print(f"Candidate Frequency: {candidate_freq[i]}\n")
        freq_diff = (cipher_freq[i] - candidate_freq[i]) ** 2
        #print(f"Difference in frequency: {freq_diff}\n")
        sum_of_diffs += freq_diff
    
    #print(f"Sum of differences: {sum_of_diffs}\n")

    # Calculate the mean of the cipher frequency and the candidate frequency
    mean_cipher_freq = np.mean(cipher_freq)
    mean_candidate_freq = np.mean(candidate_freq)
    #print(f"Mean of cipher frequency: {mean_cipher_freq}\n")
    #print(f"Mean of candidate frequency: {mean_candidate_freq}\n")

    # Calculate the standard deviation of the cipher frequency and the candidate frequency
    std_cipher_freq = np.std(cipher_freq)
    std_candidate_freq = np.std(candidate_freq)
    #print(f"Standard deviation of cipher frequency: {std_cipher_freq}\n")
    #print(f"Standard deviation of candidate frequency: {std_candidate_freq}\n")
    return sum_of_diffs

def improved_attack(ciphertext):
    """Perform an improved attack to find the best shifts."""
    # Create a frequency table for ciphertext letters
    letter_counts = [0] * 27
    total_letters = 0
    for char in ciphertext:
        if char.isalpha():
            idx = ord(char.lower()) - ord('a')
            letter_counts[idx] += 1
            total_letters += 1
        elif char == ' ':
            letter_counts[26] += 1
            total_letters += 1


    # Calculate letter frequency of ciphertext and store in a dictionary
    cipher_freq = {chr(i + ord('A')): count / total_letters for i, count in enumerate(letter_counts)}
    print(f"Cipher Frequency: {cipher_freq}\n")

    # Compare the frequencies of the ciphertext with the expected frequencies
    test_freq(cipher_freq)

    min_diff = 0
    for key, value in LETTER_FREQUENCY.items():
        #print(f"Key: {key}, Value: {value}\n")
        # calculate the KL divergence between the expected and actual frequencies
        sum_diff = compare_distributions(cipher_freq, value)
        #print(f"Difference score between ciphertext and {key}: {sum_diff}\n")
        if min_diff == 0 or sum_diff < min_diff:
            # Compare the frequencies between the ciphertext and the expected frequencies
            # Most matches found in either expected frequency is the best guess for the plaintext
            if abs(min_diff - sum_diff) < 0.0001:
                for letter, freq in value.items():
                    #print(f"Letter: {letter}, Frequency: {freq}\n")
                    if freq in cipher_freq.values():
                        #print(f"Letter: {letter}, Frequency: {freq}\n")
                        cipher_letter = [k for k, v in cipher_freq.items() if v == freq]
                        print(f"Cipher Letter: {cipher_letter}, Cipher Frequency: {cipher_freq[cipher_letter[0]]}\n")
                        print(f"Match found from freq table {key}\n")
                        found_freq_key = key # This is the frequency table that matches the frequency of our ciphertext
                        match_count += 1
                    else:
                        #print(f"Letter: {letter}, Frequency: {freq}\n")
                        print(f"No match found from freq table {key}\n")
                        break
            min_diff = sum_diff
            found_freq_key = key
            print(f"Found a better match: {found_freq_key}\nDifference score: {min_diff}\n")

    # Create a list of the differences between the expected and actual frequencies
    with open(PLAINTEXT_PATH + "/" + f"{found_freq_key}.txt", "r") as file:
        plaintext_body = file.read()
        return plaintext_body


if __name__ == "__main__":

    candidate_num = int(input("Enter the number of the candidate plaintext you would like to use (1-5): ")) - 1
    random_prob = float(input("Enter the probability of random character insertion (0 - 100): ")) / 100

    # Read a file of candidate plaintexts
    file_body = []
    with open(DICT_PATH, "r") as file:
        for line in file:
            file_body.append(line.strip())
        file_body = list(filter(None, file_body))

    # Get the frequency of each letter in each plaintext and run bigram analysis
    candidate = 0
    for plaintext in file_body:
        candidate += 1
        bigram(candidate, plaintext)
        freq_message(plaintext)
    
    # Print the global list of letter frequencies
    #print(LETTER_FREQUENCY)

    # Test the sum of the squares of the probabilities
    test_freq()

    # Generate the mono-alphabetic key
    key = generate_monoalphabetic_key()
    print(f"Generated key: {key}\n")

    # Candidate plaintext
    print(f"Candidate plaintext: {file_body[candidate_num]}\n")

    # Encrypt the candidate plaintext
    encrypted_message = encrypt(file_body[candidate_num], key)
    print(f"Encrypted message: {encrypted_message}\n")

    # Insert a random character into the ciphertext
    updated_encrypted_message = coin_flip(random_prob, encrypted_message)
    print(f"Updated encrypted message: {updated_encrypted_message}\nLength of updated message: {len(updated_encrypted_message)}\n")

    # Perform improved attack to find the plaintext it matches
    plaintext_guess = improved_attack(updated_encrypted_message)

    # Print the plaintext guess with character mapping
    print("++++++++++++++++++++++ PLAINTEXT GUESS +++++++++++++++++++++++\n")
    print(f"Plaintext guess from input {candidate_num + 1}: {plaintext_guess}\n")
    print(f"Guess made with random character insertion probability: {random_prob}\n")
    print("End of program.")





