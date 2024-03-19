import random
import string
from os import path
import numpy as np
import re
from collections import Counter
from Levenshtein import distance as lev

# CLASS 1: GENERATING MONOALPHABETIC KEY AND ENCRYPTING PLAINTEXT
class Mono:
    """Class to generate a monoalphabetic key and encrypt a candidate plaintext using the key."""

    # SECTION 1.1: GLOBAL VARIABLES
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

    # SECTION 1.2: METHODS TO CREATE FREQUENCY TABLES
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
                for freq in values.items():
                    freq_sum += (freq) ** 2
                print(f"Sum of the squares of the probabilities for {candidate}: {freq_sum}\n")   
        print(freq_sum)

    # SECTION 1.3: METHODS TO MONO ENCRYPT A CANDIDATE PLAINTEXT
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
    
    # SECTION 1.4: METHODS TO RANDOMLY INSERT CHARACTERS INTO THE CIPHERTEXT
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

# CLASS 2: PERFORMING ATTACK BASED ON DISTRIBUTIONS, BIGRAMS/TRIGRAMS, & STRING ANALYSIS
class Attack:
    """Class to perform an attack and compare distributions."""

    # SECTION 2.1: GLOBAL VARIABLES
    DICT_PATH = path.abspath(path.join(__file__, "..", "plaintext_dictionary.txt"))
    PLAINTEXT_PATH = path.abspath(path.join(__file__, "..", "candidate_files"))
    BIGRAM = {}
    TRIGRAM = {}
    CIPHER_FREQUENCY = {}
    LETTER_FREQUENCY_HALF = {}

    # SECTION 2.2: METHODS TO ATTACK THROUGH DISTRIBUTION/FREQUENCY ANALYSIS (randomness <= 15%)
    def __init__(self, ciphertext, LETTER_FREQUENCY):
        self.ciphertext = ciphertext
        self.LETTER_FREQUENCY = LETTER_FREQUENCY
        self.candidate_count = 0
        self.generate_cipher_freqeuency()

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
    
    def get_new_frequency(self, new_string):
        """Find the frequency of each letter in the new string."""
        # Find the probability of each letter in the message
        letter_counts = [0] * 27
        total_letters = 0
        for char in new_string:
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
        return letter_prob
    
    def get_sum_squares(self, cipher_dist, candidate_dist):
        """Compare the distribution of letters in the candidate plaintext with the distribution of letters in the ciphertext."""

        # Create a list of the differences between the expected and actual frequencies
        cipher_freq = sorted(list(cipher_dist.values()))
        candidate_freq = sorted(list(candidate_dist.values()))

        sum_of_diffs = 0
        for i in range(len(cipher_freq)):
            freq_diff = (cipher_freq[i] - candidate_freq[i]) ** 2
            sum_of_diffs += freq_diff
        return sum_of_diffs
    
    def get_all_diffs(self, plaintext_dist):
        """Get the sum of the squares of the differences between the expected and actual frequencies for each candidate plaintext."""
        diff_map = {}
        for candidate_name, candidate_dist in plaintext_dist.items():
            sum_diff = self.get_sum_squares(self.CIPHER_FREQUENCY, candidate_dist)
            print(f"Difference score between ciphertext and {candidate_name}: {sum_diff}\n")
            diff_map[candidate_name] = sum_diff
        return diff_map
    
    def improved_attack(self):
        """Perform an improved attack to find the best shifts."""
        # Create a map of the differences between the expected and actual frequencies
        difference_map = self.get_all_diffs(self.LETTER_FREQUENCY)
        
        # Get the minimum difference between the expected and actual frequencies
        found_freq_key = min(difference_map, key=difference_map.get)
        print(f"Best guess for the plaintext: {found_freq_key}\nDifference score: {difference_map[found_freq_key]}\n")

        # Create a list of the differences between the expected and actual frequencies
        with open(self.PLAINTEXT_PATH + "/" + f"{found_freq_key}.txt", "r") as file:
            plaintext_body = file.read()
            return plaintext_body
        
    # SECTION 2.3: METHODS TO ATTACK THROUGH STRING SUBSTITUTION/LEVENSHTEIN ALGORITHM (randomness > 15%)
    def substitute_single(self, ciphertext, idx1, idx2):
        """sub each letter of ciphertext with corresponding frequency of plaintext"""
        cipher_freq = list(dict(sorted(self.CIPHER_FREQUENCY.items(), key=lambda x: x[1], reverse=True)).keys())
        pt_freq_1 = list(dict(sorted(self.LETTER_FREQUENCY[idx1].items(), key=lambda x: x[1], reverse=True)).keys())
        pt_freq_2 = list(dict(sorted(self.LETTER_FREQUENCY[idx2].items(), key=lambda x: x[1], reverse=True)).keys())

        pt_1_pair = {}
        pt_2_pair = {}
        for i in range(len(cipher_freq)):
            pt_1_pair[cipher_freq[i]] = pt_freq_1[i]
            pt_2_pair[cipher_freq[i]] = pt_freq_2[i]

        new_ciphertext_1 = ""
        new_ciphertext_2 = ""

        for i in range(len(ciphertext)):
            char = ciphertext[i].upper()
            new_ciphertext_1 += pt_1_pair[char].lower()
            new_ciphertext_2 += pt_2_pair[char].lower()

        # Sum of squares of differences between the expected and actual frequencies
        ciphertext_1_freq = self.get_new_frequency(new_ciphertext_1)
        ciphertext_2_freq = self.get_new_frequency(new_ciphertext_2)

        sum_diff_1 = self.get_sum_squares(ciphertext_1_freq, self.LETTER_FREQUENCY[idx1])
        sum_diff_2 = self.get_sum_squares(ciphertext_2_freq, self.LETTER_FREQUENCY[idx2])

        print(f"Sum of differences for pt {idx1} and new ciphertext: {sum_diff_1}\n")
        print(f"Sum of differences for pt {idx2} and new ciphertext: {sum_diff_2}\n")

        return new_ciphertext_1, new_ciphertext_2

    def substitute_bigrams(self, ciphertext, idx1, idx2):
        """sub each bigram of ciphertext with corresponding bigram frequency of plaintext"""
        cipher_freq = self.bigram(ciphertext)
        cipher_freq = list(cipher_freq.keys())

        #cipher_freq = list(dict(sorted(self.CIPHER_FREQUENCY.items(), key=lambda x: x[1], reverse=True)).keys())
        pt_freq_1 = list(dict(sorted(self.BIGRAM[idx1].items(), key=lambda x: x[1], reverse=True)).keys())
        pt_freq_2 = list(dict(sorted(self.BIGRAM[idx2].items(), key=lambda x: x[1], reverse=True)).keys())

        #print(f"Cipher bigram frequencies: {cipher_freq} ")
        #print(f"PT 1 bigram frequencies: {pt_freq_1} ")
        #print(f"PT 2 bigram frequencies: {pt_freq_2} ")

        pt_1_pair = {}
        pt_2_pair = {}

        for i in range(0, 10):
            pt_1_pair[cipher_freq[i]] = pt_freq_1[i]
            pt_2_pair[cipher_freq[i]] = pt_freq_2[i]

        new_ciphertext_1 = ""
        new_ciphertext_2 = ""

        top10_1 = list(pt_1_pair.keys())[:10]
        top10_2 = list(pt_2_pair.keys())[:10]

        for i in range(0, len(ciphertext), 2):
            chars = ciphertext[i:i+2] 
            if ciphertext[i:i+2] in top10_1:
                new_ciphertext_1 += pt_1_pair[chars]
            else:
                new_ciphertext_1 += chars

        for i in range(0, len(ciphertext), 2):
            chars = ciphertext[i:i+2] 
            if ciphertext[i:i+2] in top10_2:
                new_ciphertext_2 += pt_2_pair[chars]
            else:
                new_ciphertext_2 += chars
        
        return new_ciphertext_1, new_ciphertext_2

    def substitute_trigrams(self, ciphertext, idx1, idx2):
        """sub each trigram of ciphertext with corresponding bigram frequency of plaintext"""
        cipher_freq = self.trigram(ciphertext)
        cipher_freq = list(cipher_freq.keys())

        #cipher_freq = list(dict(sorted(self.CIPHER_FREQUENCY.items(), key=lambda x: x[1], reverse=True)).keys())
        pt_freq_1 = list(dict(sorted(self.TRIGRAM[idx1].items(), key=lambda x: x[1], reverse=True)).keys())
        pt_freq_2 = list(dict(sorted(self.TRIGRAM[idx2].items(), key=lambda x: x[1], reverse=True)).keys())

        # print(f"Cipher trigram frequencies: {cipher_freq} ")
        # print(f"PT 1 trigram frequencies: {pt_freq_1} ")
        # print(f"PT 2 trigram frequencies: {pt_freq_2} ")

        pt_1_pair = {}
        pt_2_pair = {}

        for i in range(0, 10):
            pt_1_pair[cipher_freq[i]] = pt_freq_1[i]
            pt_2_pair[cipher_freq[i]] = pt_freq_2[i]

        new_ciphertext_1 = ""
        new_ciphertext_2 = ""

        top10_1 = list(pt_1_pair.keys())[:10]
        top10_2 = list(pt_2_pair.keys())[:10]

        for i in range(0, len(ciphertext), 3):
            chars = ciphertext[i:i+3] 
            if ciphertext[i:i+3] in top10_1:
                new_ciphertext_1 += pt_1_pair[chars]
            else:
                new_ciphertext_1 += chars

        for i in range(0, len(ciphertext), 3):
            chars = ciphertext[i:i+3] 
            if ciphertext[i:i+3] in top10_2:
                new_ciphertext_2 += pt_2_pair[chars]
            else:
                new_ciphertext_2 += chars

        return new_ciphertext_1, new_ciphertext_2
    
    def levenshtein(self, ciphertext, idx1, idx2):
        """Levenshtein algorithm analysis"""
        single_sub_1, single_sub_2 = self.substitute_single(ciphertext, idx1, idx2)
        bigram_sub_1, bigram_sub_2 = self.substitute_bigrams(ciphertext, idx1, idx2)
        trigram_sub_1, trigram_sub_2 = self.substitute_trigrams(ciphertext, idx1, idx2)

        print(f"Original Ciphertext: {ciphertext}\n")
        print(f"New Ciphertext 1: {single_sub_1}\n")
        print(f"New Ciphertext 2: {single_sub_2}\n")

        print(f"Original Ciphertext (BIGRAM): {ciphertext}\n")
        print(f"New Ciphertext 1 (BIGRAM): {bigram_sub_1}\n")
        print(f"New Ciphertext 2 (BIGRAM): {bigram_sub_2}\n")

        print(f"Original Ciphertext (TRIGRAM): {ciphertext}\n")
        print(f"New Ciphertext 1 (TRIGRAM): {trigram_sub_1}\n")
        print(f"New Ciphertext 2 (TRIGRAM): {trigram_sub_2}\n")

        # Calculate levenshtein distance
        # test_lev = lev(self.PLAINTEXT_PATH + "/" + f"pt1.txt", self.PLAINTEXT_PATH + "/" + f"pt.txt")
        control_lev = lev(ciphertext, self.PLAINTEXT_PATH + "/" + f"pt.txt")
        single_lev_dist_1 = lev(single_sub_1, self.PLAINTEXT_PATH + "/" + f"{idx1}.txt")
        single_lev_dist_2 = lev(single_sub_2, self.PLAINTEXT_PATH + "/" + f"{idx2}.txt")

        bigram_lev_dist_1 = lev(bigram_sub_1, self.PLAINTEXT_PATH + "/" + f"{idx1}.txt")
        bigram_lev_dist_2 = lev(bigram_sub_2, self.PLAINTEXT_PATH + "/" + f"{idx2}.txt")

        trigram_lev_dist_1 = lev(trigram_sub_1, self.PLAINTEXT_PATH + "/" + f"{idx1}.txt")
        trigram_lev_dist_2 = lev(trigram_sub_2, self.PLAINTEXT_PATH + "/" + f"{idx2}.txt")

        print(f"Levenshtein distance for control and new ciphertext: {control_lev}\n")
        print(f"Levenshtein distance for pt {idx1} and new ciphertext (SINGLE): {single_lev_dist_1}\n")
        print(f"Levenshtein distance for pt {idx2} and new ciphertext (SINGLE): {single_lev_dist_2}\n")
        print(f"Levenshtein distance for pt {idx1} and new ciphertext (BIGRAM): {bigram_lev_dist_1}\n")
        print(f"Levenshtein distance for pt {idx2} and new ciphertext (BIGRAM): {bigram_lev_dist_2}\n")
        print(f"Levenshtein distance for pt {idx1} and new ciphertext (TRIGRAM): {trigram_lev_dist_1}\n")
        print(f"Levenshtein distance for pt {idx2} and new ciphertext (TRIGRAM): {trigram_lev_dist_2}\n")

        # Choosing from single_lev as of now
        if single_lev_dist_1 < single_lev_dist_2:
            with open(self.PLAINTEXT_PATH + "/" + f"{idx1}.txt", "r") as file:
                plaintext_body = file.read()
                return plaintext_body
        elif single_lev_dist_1 > single_lev_dist_2:
            with open(self.PLAINTEXT_PATH + "/" + f"{idx2}.txt", "r") as file:
                plaintext_body = file.read()
                return plaintext_body
        # Placeholder for now
        else:
            print("Levenshtein values in candidate plaintexts are equal.")

    def get_candidates(self):
        """Get the frequency of each letter in each candidate plaintext."""
        # Read a file of candidate plaintexts
        file_body = []
        with open(self.DICT_PATH, "r") as file:
            for line in file:
                file_body.append(line.strip())
            file_body = list(filter(None, file_body))
        return file_body

    def get_candidates_half(self):
        """Get the frequency of each letter in each candidate plaintext (second half)."""
        # Read a file of candidate plaintexts
        file_body = []
        with open(self.DICT_PATH, "r") as file:
            for line in file:
                file_body.append(line.strip())
            file_body = list(filter(None, file_body))

            # split each element in our list of plaintexts
            file_body = [text[len(text) // 2:] for text in file_body]
        return file_body

    def bigram(self, ciphertext):
        """Perform bigram analysis on the candidate plaintexts and the ciphertext."""
        file_body = self.get_candidates()
        candidate = 0
        for plaintext in file_body:
            candidate += 1
            bigram_plaintext = plaintext
            bigram_p = Counter(bigram_plaintext[idx : idx + 2] for idx in range(len(plaintext) -1))
            self.BIGRAM[f"pt{candidate}"] = bigram_p
            #print(f"Bigram Frequency for Plaintext {candidate}: {bigram_p}\n")

        bigram_ciphertext = ciphertext
        bigram_c = Counter(bigram_ciphertext[idx : idx + 2] for idx in range(len(plaintext) -1))
        #BIGRAM[ciphertext] = bigram_c
        #print(f"Bigram Frequency for Ciphertext: {bigram_c}\n")
        #self.compare_bigram_distributions(bigram_c)

        return bigram_c
    
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

        # return sum_of_diffs
    
    def trigram(self, ciphertext):
        """Perform trigram analysis on the candidate plaintexts and the ciphertext."""
        file_body = self.get_candidates()
        candidate = 0
        for plaintext in file_body:
            candidate += 1
            trigram_plaintext = plaintext
            trigram_p = Counter(trigram_plaintext[idx : idx + 3] for idx in range(len(plaintext) -1))
            self.TRIGRAM[f"pt{candidate}"] = trigram_p
            # print(f"Trigram Frequency for Plaintext {candidate}: {trigram_p}\n")

        trigram_ciphertext = ciphertext
        trigram_c = Counter(trigram_ciphertext[idx : idx + 3] for idx in range(len(plaintext) -1))
        # print(f"Trigram Frequency for Ciphertext: {trigram_c}\n")

        return trigram_c

    # SECTION 2.4: METHODS TO ATTACK THROUGH STRING ANALYSIS ON HALF OF THE CIPHERTEXT
    def get_candidates_half(self):
        """Get the frequency of each letter in each candidate plaintext (second half)."""
        # Read a file of candidate plaintexts
        file_body = []
        with open(self.DICT_PATH, "r") as file:
            for line in file:
                file_body.append(line.strip())
            file_body = list(filter(None, file_body))

            # split each element in our list of plaintexts
            file_body = [text[len(text) // 2:] for text in file_body]
        return file_body

    def get_frequency_half(self, file_body):
        """Find the frequency of each letter in the second half of the candidate plaintext."""
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
            self.LETTER_FREQUENCY_HALF[f"pt{self.candidate_count}"] =  letter_prob
    
    def improved_attack_half(self):
        """Perform an improved attack to find the best shifts."""
        # Create a map of the differences between the expected and actual frequencies
        print("PRINTING HALF FREQUENCY DIFFERENCES\n")
        difference_map = self.get_all_diffs(self.LETTER_FREQUENCY_HALF)
        
        # Get the minimum difference between the expected and actual frequencies
        found_freq_key = min(difference_map, key=difference_map.get)
        print(f"Best guess for the plaintext: {found_freq_key}\nDifference score: {difference_map[found_freq_key]}\n")

        # Create a list of the differences between the expected and actual frequencies
        with open(self.PLAINTEXT_PATH + "/" + f"{found_freq_key}.txt", "r") as file:
            plaintext_body = file.read()
            return plaintext_body

class HillClimb():

    TRIGRAM = {}

    def __init__(self, ciphertext, plaintext_list, cipher_frequency):
        self.ciphertext = ciphertext
        self.plaintext_list = plaintext_list
        self.cipher_frequency = cipher_frequency
        self.candidate_count = 0
        self.pt_trigram()

    def get_initial_key(self, pt_frequency_1):
        """Pick the initial key based on the frequency of the ciphertext."""
        # Create a list of the differences between the expected and actual frequencies
        cipher_freq = list(dict(sorted(self.cipher_frequency.items(), key=lambda x: x[1], reverse=True)).keys())
        pt_freq = list(dict(sorted(pt_frequency_1.items(), key=lambda x: x[1], reverse=True)).keys())

        pt_pair = {}
        for i in range(len(cipher_freq)):
            pt_pair[cipher_freq[i]] = pt_freq[i]

        # Sort by the values in pt_pair
        initial_key = pt_pair
        print(initial_key)
        return initial_key
    
    def swap_keys(self, key, pointer_1, pointer_2):
        """Swap the char keys at the two pointers."""
        key_chars = list(key.keys())
        key_values = list(key.values())

        # Swap the keys at the two pointers
        temp = key_chars[pointer_2]
        key_chars[pointer_2] = key_chars[pointer_1]
        key_chars[pointer_1] = temp

        new_key = dict(zip(key_chars, key_values))
        print(f"New Key: {new_key}")
        return new_key
    
    def pt_trigram(self):
        """Perform trigram analysis on the candidate plaintexts and the ciphertext."""
        file_body = self.plaintext_list
        for plaintext in file_body:
            self.candidate_count += 1
            print(f"(HILLCLIMB) Plaintext {self.candidate_count}: {plaintext}")
            trigram_plaintext = plaintext
            trigram_p = Counter(trigram_plaintext[idx : idx + 3] for idx in range(len(plaintext) -1))
            self.TRIGRAM[f"pt{self.candidate_count}"] = trigram_p

    def ct_trigram(self, ciphertext):
        """Perform trigram analysis on the ciphertext."""
        trigram_ciphertext = ciphertext
        trigram_c = Counter(trigram_ciphertext[idx : idx + 3] for idx in range(len(ciphertext) -1))
        return trigram_c
    
    def decrypt_cipher(self, ciphertext, key):
        """Get the shifted ciphertext based on the key."""
        key = dict(sorted(key.items(), key=lambda x: x[1]))
        print(f"Sorted key: {key}")
        #alphabet = " abcdefghijklmnopqrstuvwxyz"
        decrypt_cipher = ""
        for i in range(len(ciphertext)):
            char = ciphertext[i].upper()
            decrypt_cipher += key[char].lower()
        return decrypt_cipher
    
    def get_fitness_score(self, key, trigram_c, trigram_p):
        """Get the fitness score of the plaintext based on the ciphertext and key."""

        # Calculate score between cipher trigrams and plaintext trigrams
        sum_diff = 0
        for key, value in trigram_c.items():
            sum_diff += (trigram_c[key] - trigram_p[key]) ** 2
        return sum_diff
    
    def hill_climb(self, ciphertext, plaintext_guess, plaintext_name):
        """Perform a hill climb to find the best shifts."""
        # Some code to pick best random key
        parent_key = self.get_initial_key(plaintext_guess)
        iterations = 5
        trigram_c = self.ct_trigram(ciphertext)
        trigram_p = self.TRIGRAM[plaintext_name]
        parent_score = self.get_fitness_score(parent_key, trigram_c, trigram_p)
        print(f"Hill climb parent score with parent key {parent_key}: {parent_score}\n")
        counter = 0
        for i in range(iterations):
            pointer_1 = counter
            pointer_2 = counter + 1
            child_key = parent_key
            child_key = self.swap_keys(child_key, pointer_1, pointer_2)
            new_ciph = self.decrypt_cipher(ciphertext, child_key)
            new_trigram_c = self.ct_trigram(new_ciph)
            child_score = self.get_fitness_score(child_key, new_trigram_c, trigram_p)
            print(f"Child score with child key {child_key}: {child_score}\n")
            if child_score < parent_score:
                parent_score = child_score
                parent_key = child_key
                print(f"Parent score updated to {parent_score} with key {parent_key}\n")
            counter += 2
        
        print("End of hill climb.")



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
    target_length = 690 # 15% of randomness on the ciphertext

    # Create an instance of the Attack class
    frequency_tables = mono_cipher.get_frequency_table()
    mono_attack = Attack(randomized_cipher, frequency_tables)

    # Check if the length of the randomness in the cipher is less than target percent
    if len(randomized_cipher) <= target_length:
        # Perform euclidean distance calculation between cipher and candidate distributions
        plaintext_guess = mono_attack.improved_attack()
    else:
        # Perform imroved attack on the second half of the ciphertext
        candidate_list_half = mono_attack.get_candidates_half()
        mono_attack.get_frequency_half(candidate_list_half)
        plaintext_guess = mono_attack.improved_attack_half()

        # Instantiate hill climb class
        cipher_freq = mono_attack.get_cipher_frequency()
        hill_attack = HillClimb(randomized_cipher, candidate_list, cipher_freq)

        difference_map = mono_attack.get_all_diffs(frequency_tables)
        sorted_diffs = sorted(difference_map.items(), key=lambda x: x[1])
        
        # Store the two lowest differences
        lowest_diff = sorted_diffs[0]
        lowest_plaintext_dist = frequency_tables[lowest_diff[0]]

        # Perform hill climb
        hill_attack.hill_climb(randomized_cipher, lowest_plaintext_dist, lowest_diff[0])

        print("End of test, ya moms")

        # # Perform bigram/levenshtein comparison for more reliable attack

        # # Get the two lowest sum of square differences
        # difference_map = mono_attack.get_all_diffs()
        # sorted_diffs = sorted(difference_map.items(), key=lambda x: x[1])
        
        # # Store the two lowest differences
        # lowest_diff, second_lowest_diff = sorted_diffs[0], sorted_diffs[1]
        # print(f"Lowest difference: {lowest_diff}\nSecond lowest difference: {second_lowest_diff}\n")

        # # Perform substitution on the ciphertext
        # mono_attack.substitute_single(randomized_cipher, lowest_diff[0], second_lowest_diff[0])

        # # plaintext_guess = mono_attack.bigram(randomized_cipher)
        # plaintext_guess = mono_attack.levenshtein(randomized_cipher, lowest_diff[0], second_lowest_diff[0])

        # mono_attack.substitute_bigrams(randomized_cipher, lowest_diff[0], second_lowest_diff[0])

        # # mono_attack.trigram(randomized_cipher)

        # mono_attack.substitute_trigrams(randomized_cipher, lowest_diff[0], second_lowest_diff[0])

    # Print the plaintext guess
    print("++++++++++++++++++++++ PLAINTEXT GUESS +++++++++++++++++++++++\n")
    print(f"Plaintext guess from input {candidate_num + 1}: {plaintext_guess}\n")
    print(f"Guess made with random character insertion probability: {random_prob}\n")
    print("End of program.")
