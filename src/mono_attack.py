import random
import string

# GLOBAL
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
    LETTER_FREQUENCY[f"Candidate {candidate_count}"] =  letter_prob

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

def improved_attack(ciphertext, letter_frequency):
    """Perform an improved attack to find the best shifts."""
    # Create a frequency table for ciphertext letters
    letter_counts = [0] * 26
    total_letters = 0
    for char in ciphertext:
        if char.isalpha():
            idx = ord(char.lower()) - ord('a')
            letter_counts[idx] += 1
            total_letters += 1

    # Calculate expected letter frequencies based on provided table
    expected_frequencies = [letter_frequency.get(chr(ord('a') + i).upper(), 0) / 100 for i in range(26)]

    # Compute the correlation for each shift
    correlations = []
    for shift in range(26):
        correlation = sum(letter_counts[(i + shift) % 26] * expected_frequencies[i] for i in range(26)) / total_letters
        correlations.append(correlation)

    # Find the best shifts (keys)
    best_shifts = [i for i, corr in enumerate(correlations) if corr > 0.15]  # Adjust threshold as needed
    return best_shifts

if __name__ == "__main__":
    # # Get plaintext from user
    # plaintext = input("Enter your message: ")
    # freq_message(plaintext)

    # Read a file of candidate plaintexts
    file_body = []
    with open("plaintext_dictionary.txt", "r") as file:
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
    print(f"Candidate plaintext: {file_body[0]}\n")

    # Encrypt the candidate plaintext
    encrypted_message = encrypt(file_body[0], key)
    print(f"Encrypted message: {encrypted_message}\n")

    # Perform improved attack to find the best shifts
    for key, value in LETTER_FREQUENCY.items():
        print(f"Key: {key}, Value: {value}\n")
        best_shifts = improved_attack(encrypted_message, value)
        print(f"Best shifts: {best_shifts}\n")



