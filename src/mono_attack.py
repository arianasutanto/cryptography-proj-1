import random
import string
from os import path
import numpy as np
from collections import Counter

class Mono:
    """Class to generate a monoalphabetic key and encrypt a candidate plaintext using the key."""

    # SECTION 1: GLOBAL VARIABLES
    DICT_PATH = path.abspath(path.join(__file__, "..", "plaintext_dictionary.txt"))
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
    
    candidate_count = 0
    LETTER_FREQUENCY = {"Common Frequency": common_english_frequency}

    # SECTION 2: METHODS TO CREATE FREQUENCY TABLES
    def generate_frequency_table(self):
        """Find the frequency of each letter in the message and add it to the global list."""
        file_body = self.get_candidate()

        # Get the frequency of each letter in each plaintext
        for plaintext in file_body:

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
            self.candidate_count += 1
            self.LETTER_FREQUENCY[f"pt{self.candidate_count}"] =  letter_prob
    
    def get_candidate(self):
        """Get each of the candidate plaintext."""
        # Read a file of candidate plaintexts
        file_body = []
        with open(self.DICT_PATH, "r") as file:
            for line in file:
                file_body.append(line.strip())
            file_body = list(filter(None, file_body))
        return file_body
    
    def get_frequency_table(self):
        return self.LETTER_FREQUENCY
    
    def get_sum_squares(self, cipher_freq=None):
        """Simple test to check if the sum of the squares of the probabilities is 0.065."""
        if cipher_freq:
            freq_sum = 0
            for freq in cipher_freq.values():
                freq_sum += (freq) ** 2
            print(f"Sum of the squares of the probabilities for the cipher frequency: {freq_sum}\n")
        else:
            for candidate, values in self.LETTER_FREQUENCY.items():
                freq_sum = 0
                for letter, freq in values.items():
                    freq_sum += (freq) ** 2
                print(f"Sum of the squares of the probabilities for {candidate}: {freq_sum}\n")   
        print(freq_sum)

    # SECTION 3: METHODS TO MONO ENCRYPT A CANDIDATE PLAINTEXT
    def generate_monoalphabetic_key(self):
        """Generate a monoalphabetic key by shuffling the alphabet."""
        alphabet = list(string.ascii_lowercase)
        alphabet.insert(0, ' ')
        random.shuffle(alphabet)
        return ''.join(alphabet)
    
    def encrypt(self, text, key):
        """Encrypt the candidate plaintext using the generated key."""
        # Convert input text to lowercase
        alphabet = list(string.ascii_lowercase)
        alphabet.insert(0, ' ')
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
                idx = (ord(char) - ord('a') + 1)
                encrypted_text += key[idx]
            elif char == ' ':
                encrypted_text += key[0]
        return encrypted_text
    
    # SECTION 4: METHODS TO RANDOMLY INSERT CHARACTERS INTO THE CIPHERTEXT
    def coin_flip(self, prob, ciphertext):
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
                if message_pointer < len(ciphertext):
                    new_ciphertext += ciphertext[message_pointer]
                    message_pointer += 1
            elif 0 <= coin_value < prob and counter < num_of_rand_chars:
                rand_char = random.choice(" abcdefghijklmnopqrstuvwxyz")
                new_ciphertext += rand_char
                counter += 1
            cipher_pointer += 1

        print(f"Message pointer: {message_pointer}\nCipher pointer: {cipher_pointer}\n")
        return new_ciphertext
    
    def random_char_insertion(self, random_prob, ciphertext):
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

class Attack:
    """Class to perform an improved attack and compare distributions."""
    
    # SECTION 1: GLOBAL VARIABLES
    PLAINTEXT_PATH = path.abspath(path.join(__file__, "..", "candidate_files"))
    BIGRAM = {}
    CIPHER_FREQUENCY = {}

    # SECTION 2: METHODS TO IMPROVED ATTACK
    def __init__(self, ciphertext, LETTER_FREQUENCY):
        self.ciphertext = ciphertext
        self.LETTER_FREQUENCY = LETTER_FREQUENCY

    def generate_cipher_freqeuency(self):
        """Get the frequency of each letter in the ciphertext."""
        # Find the probability of each letter in the message
        letter_counts = [0] * 27
        total_letters = 0
        for char in self.ciphertext:
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
        self.CIPHER_FREQUENCY = letter_prob
        print(f"Cipher Frequency: {self.CIPHER_FREQUENCY}\n")
    
    def get_cipher_frequency(self):
        return self.CIPHER_FREQUENCY
    
    def compare_sum_squares(self, cipher_dist, candidate_dist):
        """Compare the distribution of letters in the candidate plaintext with the distribution of letters in the ciphertext."""

        # Create a list of the differences between the expected and actual frequencies
        cipher_freq = sorted(list(cipher_dist.values()))
        candidate_freq = sorted(list(candidate_dist.values()))

        sum_of_diffs = 0
        for i in range(len(cipher_freq)):
            freq_diff = (cipher_freq[i] - candidate_freq[i]) ** 2
            sum_of_diffs += freq_diff
        return sum_of_diffs
    
    def improved_attack(self):
        """Perform an improved attack to find the best shifts."""

        min_diff = 0
        self.generate_cipher_freqeuency()
        for candidate_name, candidate_dist in self.LETTER_FREQUENCY.items():
            # calculate the KL divergence between the expected and actual frequencies
            sum_diff = self.compare_sum_squares(self.CIPHER_FREQUENCY, candidate_dist)
            #print(f"Difference score between ciphertext and {key}: {sum_diff}\n")
            if min_diff == 0 or sum_diff < min_diff:
                # Compare the frequencies between the ciphertext and the expected frequencies
                # Most matches found in either expected frequency is the best guess for the plaintext
                if abs(min_diff - sum_diff) < 0.0001:
                    for letter, freq in candidate_dist.items():
                        if freq in self.CIPHER_FREQUENCY.values():
                            cipher_letter = [k for k, v in self.CIPHER_FREQUENCY.items() if v == freq]
                            print(f"Cipher Letter: {cipher_letter}, Cipher Frequency: {self.CIPHER_FREQUENCY[cipher_letter[0]]}\n")
                            print(f"Match found from freq table {candidate_name}\n")
                            found_freq_key = key # This is the frequency table that matches the frequency of our ciphertext
                        else:
                            print(f"No match found from freq table {candidate_name}\n")
                            break
                min_diff = sum_diff
                found_freq_key = candidate_name
                print(f"Found a better match: {found_freq_key}\nDifference score: {min_diff}\n")

        # Create a list of the differences between the expected and actual frequencies
        with open(self.PLAINTEXT_PATH + "/" + f"{found_freq_key}.txt", "r") as file:
            plaintext_body = file.read()
            return plaintext_body
        
    
    # SECTION 3: METHODS TO PERFORM BIGRAM ANALYSIS
        
    def get_candidates(self):
        """Get the frequency of each letter in each candidate plaintext."""
        # Read a file of candidate plaintexts
        file_body = []
        with open(self.DICT_PATH, "r") as file:
            for line in file:
                file_body.append(line.strip())
            file_body = list(filter(None, file_body))
        return file_body
    
    def compare_bigram_distributions(self, bigram_c):

        # Create a list of the differences between the expected and actual frequencies

        cipher_freq = list(bigram_c.values())
        cipher_freq.sort(reverse=True)
        
        for key, value in self.BIGRAM.items():

            candidate_freq = list(value.values())
            candidate_freq.sort(reverse=True)
            print(f"curr bigram: {candidate_freq}")
            sum_of_diffs = 0
            for i in range(0,15):
                #print(f"Cipher Frequency: {cipher_freq[i]}\n")
                #print(f"Candidate Frequency: {candidate_freq[i]}\n")
                freq_diff = (cipher_freq[i] - candidate_freq[i]) ** 2
                #print(f"Difference in frequency for pt {key} and ciphertext (bigram): {freq_diff}\n")

                sum_of_diffs += freq_diff
        
            print(f"Sum of differences for pt {key} and ciphertext: {sum_of_diffs}\n")

        #return sum_of_diffs

    def bigram(self, ciphertext):
        """Perform bigram analysis on the candidate plaintexts and the ciphertext."""
        file_body = self.get_candidates()
        candidate = 0
        for plaintext in file_body:
            candidate += 1
            bigram_plaintext = plaintext
            bigram_p = Counter(bigram_plaintext[idx : idx + 2] for idx in range(len(plaintext) -1))
            self.BIGRAM[candidate] = bigram_p
            print(f"Bigram Frequency for Plaintext {candidate}: {bigram_p}\n")

        bigram_ciphertext = ciphertext
        bigram_c = Counter(bigram_ciphertext[idx : idx + 2] for idx in range(len(plaintext) -1))
        #BIGRAM[ciphertext] = bigram_c
        print(f"Bigram Frequency for Ciphertext: {bigram_c}\n")
        self.compare_bigram_distributions(bigram_c)
    

if __name__ == "__main__":

    candidate_num = int(input("Enter the number of the candidate plaintext you would like to use (1-5): ")) - 1
    random_prob = float(input("Enter the probability of random character insertion (0 - 100): ")) / 100

    ## STEP 1: ENCRYPT THE CANDIDATE PLAINTEXT
    # Create an instance of the Mono class
    mono_cipher = Mono()

    # Generate the mono-alphabetic key
    key = mono_cipher.generate_monoalphabetic_key()
    print(f"Generated key pair:")
    print(" abcdefghijklmnopqrstuvwxyz")
    print(key + "\n")

    # Get the candidate plaintext
    candidate_list = mono_cipher.get_candidate()
    selected_candidate = candidate_list[candidate_num]
    print(f"Candidate plaintext: {selected_candidate}\n")

    # Encrypt the candidate plaintext
    encrypted_message = mono_cipher.encrypt(selected_candidate, key)
    print(f"Encrypted message: {encrypted_message}\n")

    # Apply randomness to the encrypted message
    randomized_cipher = mono_cipher.coin_flip(random_prob, encrypted_message)
    print(f"Randomized encrypted message: {randomized_cipher}\nLength of updated message: {len(randomized_cipher)}\n")

    ## STEP 2: CREATE FREQUENCY TABLES
    # Generate the frequency table for the candidate plaintext
    mono_cipher.generate_frequency_table()

    ## STEP 3: PERFORM AN ATTACK
    target_length = 660 # 10% of randomness on the ciphertext

    # Create an instance of the Attack class
    frequency_tables = mono_cipher.get_frequency_table()
    mono_attack = Attack(randomized_cipher, frequency_tables)

    # Check if the length of the randomness in the cipher is less than target percent
    if len(randomized_cipher) <= target_length:
        # Perform euclidean distance calculation between cipher and candidate distributions
        plaintext_guess = mono_attack.improved_attack()
    else:
        # Perform bigram/levenshtein comparison for more reliable attack
        plaintext_guess = mono_attack.bigram(randomized_cipher)

    # Print the plaintext guess
    print("++++++++++++++++++++++ PLAINTEXT GUESS +++++++++++++++++++++++\n")
    print(f"Plaintext guess from input {candidate_num + 1}: {plaintext_guess}\n")
    print(f"Guess made with random character insertion probability: {random_prob}\n")
    print("End of program.")
