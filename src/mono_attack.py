import random
import string
import os
from os import path
from datetime import datetime
from collections import Counter
from Levenshtein import distance as lev


global candidate_dict
candidate_dict = {
    "pt1": "unconquerable tropical pythagoras rebukingly price ephedra barmiest hastes spades fevers cause wisped overdecorates linked smitten trickle scanning cognize oaken casework significate influenceable precontrived clockers defalcation fruitless splintery kids placidness regenerate harebrained liberalism neuronic clavierist attendees matinees prospectively bubbies longitudinal raving relaxants rigged oxygens chronologist briniest tweezes profaning abeyances fixity gulls coquetted budgerigar drooled unassertive shelter subsoiling surmounted frostlike jobbed hobnailed fulfilling jaywalking testabilit",
    "pt2": "protectorates committeemen refractory narcissus bridlers weathercocks occluding orchectomy syncoms denunciation chronaxy imperilment incurred defrosted beamy opticopupillary acculturation scouting curiousest tosh preconscious weekday reich saddler politicize mercerizes saucepan bifold chit reviewable easiness brazed essentially idler dependable predicable locales rededicated cowbird kvetched confusingly airdrops dreggier privileges tempter anaerobes glistened sartorial distrustfulness papillary ughs proctoring duplexed pitas traitorously unlighted cryptographer odysseys metamer either meliorat",
    "pt3": "incomes shoes porcine pursue blabbered irritable ballets grabbed scything oscillogram despots pharynxes recompensive disarraying ghoulish mariachi wickerwork orientation candidnesses nets opalescing friending wining cypher headstrong insubmissive oceanid bowlegs voider recook parochial trop gravidly vomiting hurray friended uncontestable situate fen cyclecars gads macrocosms dhyana overruns impolite europe cynical jennet tumor noddy canted clarion opiner incurring knobbed planeload megohm dejecting campily dedicational invaluable praecoces coalescence dibbuk bustles flay acuities centimeters l",
    "pt4": "rejoicing nectar asker dreadfuls kidnappers interstate incrusting quintessential neglecter brewage phosphatic angle obliquely bean walkup outflowed squib tightwads trenched pipe extents streakier frowning phantasmagories supinates imbibers inactivates tingly deserter steerages beggared pulsator laity salvageable bestrode interning stodgily cracker excisions quanted arranges poultries sleds shortly packages apparat fledge alderwomen halvah verdi ineffectualness entrenches franchising merchantability trisaccharide limekiln sportsmanship lassitudes recidivistic locating iou wardress estrus potboi",
    "pt5": "headmaster attractant subjugator peddlery vigil dogfights pixyish comforts aretes felinities copycat salerooms schmeering institutor hairlocks speeder composers dramatics eyeholes progressives reminiscent hermaphrodism simultaneous spondaics hayfork armory refashioning battering darning tapper pancaked unaffected televiewer mussiness pollbook sieved reclines restamp cohosh excludes homelier coacts refashioned loiterer prospectively encouragers biggest pasters modernity governorships crusted buttoned wallpapered enamors supervisal nervily groaning disembody communion embosoming tattles pancakes",
    "pt6": "reptilian buzzer transitive frowziest sockpuppet limericks fathomless kibbutzim morbidly omnivores quagmires vendetta quatrain rambling telemetric harbinger epistolary bedazzled tourniquet phlegmatic obsequious modularity finessed congeniality foxglove mystique trampoline vivacity dichotomy sycophantic nectarine quixotic zeitgeist waltzing cosmopolitan gobbledygook coriander virtuoso phosphorescent juxtapose flabbergasted octopus ephemeral loquacious juggernaut procrastinate labyrinthine polyglot serendipitous audacious moonstruck sanctimonious capitulate antidisestablishmentarianism zephyr in",
    "pt7": "anticipation layout myth smooth reckless rhythm torch photography circumstance species vein island cake incident trouser welcome compete suspect shortage generation trance sum quest viable variant blonde node bread executrix ethnic access nervous formation coincidence payment cigarette despise amuse fold debate medicine ministry meal bait draft transmission wood suit comfortable define character squeeze freshman council activity executive concede charge surgeon suntan vain offensive innovation habitat friendly lot projection policy treat sausage active admiration summit reproduction formation ",
    "pt8": "charm heel glimpse palace point damn econobox teach ostracize faint deliver bride remain ton pioneer navy nature steam resist costume north hole hypothesis birthday convention traction civilization eye pot banquet customer patience joy fix reserve structure suffering protection value taxi straw museum trait century overeat chemistry table squash swarm mention distort nationalist residence by guitar pair weight absence discourage ego provincial spot aware stun rest horizon origin establish dilute archive term dealer administration coincidence punch capture meat choke magnetic degree incongruous",
    "pt9": "concern cell overeat addicted precede bundle stock install dark hostility cart arrest arena excavation spare theft continental disaster inflation blow justify thoughtful path prejudice seasonal pipe eat trade demand blade stay crosswalk deputy civilian triangle migration critical genuine rehabilitation chemistry collect south computer primary wait variant priority old church ambiguity unrest tiger platform storm patrol television tax medieval risk glove race board stadium arrange family cooperation convulsion franchise make gear killer aquarium domination news inn cash table push requests felt",
    "pt10": "elaborate statement draw burst elephant gallery beneficiary salmon guarantee arrow excess rape conscious magnetic half vigorous gloom work freckle shrink build quiet cross act gas hell wisecrack safe obligation fisherman knife staircase opposition relationship freshman tense light fuel education onion late correction cup royalty promotion symptom hover revenge cluster duty mutual dominant treasurer leaflet houseplant discriminate fair member overall classroom buttocks explosion horse socialist discuss net voice show mother brown snatch brink revive ant regular sniff heel applied lighter trend"
}


# CLASS 1: GENERATING MONOALPHABETIC KEY AND ENCRYPTING PLAINTEXT
class Mono:
    """Class to generate a monoalphabetic key and encrypt a candidate plaintext using the key."""

    # SECTION 1.1: GLOBAL VARIABLES
    DICT_PATH = path.abspath(path.join(__file__, "..", "plaintext_dictionary.txt"))
    
    candidate_count = 0
    LETTER_FREQUENCY = {}

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
        # read all candidate plaintexts from the dictionary
        return list(candidate_dict.values())
    
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

        return candidate_dict[found_freq_key]
        
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
        control_lev = lev(ciphertext, candidate_dict["pt1"])
        single_lev_dist_1 = lev(single_sub_1, candidate_dict[idx1])
        single_lev_dist_2 = lev(single_sub_2, candidate_dict[idx2])

        bigram_lev_dist_1 = lev(bigram_sub_1, candidate_dict[idx1])
        bigram_lev_dist_2 = lev(bigram_sub_2, candidate_dict[idx2])

        trigram_lev_dist_1 = lev(trigram_sub_1, candidate_dict[idx1])
        trigram_lev_dist_2 = lev(trigram_sub_2, candidate_dict[idx2])

        print(f"Levenshtein distance for control and new ciphertext: {control_lev}\n")
        print(f"Levenshtein distance for pt {idx1} and new ciphertext (SINGLE): {single_lev_dist_1}\n")
        print(f"Levenshtein distance for pt {idx2} and new ciphertext (SINGLE): {single_lev_dist_2}\n")
        print(f"Levenshtein distance for pt {idx1} and new ciphertext (BIGRAM): {bigram_lev_dist_1}\n")
        print(f"Levenshtein distance for pt {idx2} and new ciphertext (BIGRAM): {bigram_lev_dist_2}\n")
        print(f"Levenshtein distance for pt {idx1} and new ciphertext (TRIGRAM): {trigram_lev_dist_1}\n")
        print(f"Levenshtein distance for pt {idx2} and new ciphertext (TRIGRAM): {trigram_lev_dist_2}\n")

        # Choosing from single_lev as of now
        if single_lev_dist_1 < single_lev_dist_2:
            return candidate_dict[idx1]
        elif single_lev_dist_1 > single_lev_dist_2:
            return candidate_dict[idx2]
        # Placeholder for now
        else:
            print("Levenshtein values in candidate plaintexts are equal.")

    def get_candidates(self):
        """Get the frequency of each letter in each candidate plaintext."""
        # get all candidate plaintexts
        return list(candidate_dict.values())

    def get_candidates_half(self):
        """Get the frequency of each letter in each candidate plaintext (second half)."""
        # split each element in our list of plaintexts
        file_body = [text[len(text) // 2:] for text in list(candidate_dict.values())]
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
        bigram_c = Counter(bigram_ciphertext[idx : idx + 2] for idx in range(len(plaintext) -1))\

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
                freq_diff = (cipher_freq[i] - candidate_freq[i]) ** 2
                sum_of_diffs += freq_diff
        
            #print(f"Sum of differences for pt {key} and ciphertext: {sum_of_diffs}\n")

        return sum_of_diffs
    
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
        # Create a map of the differences between the expected and actual frequencies\
        difference_map = self.get_all_diffs(self.LETTER_FREQUENCY_HALF)
        
        # Get the minimum difference between the expected and actual frequencies
        found_freq_key = min(difference_map, key=difference_map.get)
        print(f"Best guess for the plaintext: {found_freq_key}\nDifference score: {difference_map[found_freq_key]}\n")

        # Create a list of the differences between the expected and actual frequencies
        return candidate_dict[found_freq_key]

class HillClimb():

    PLAINTEXT_PATH = path.abspath(path.join(__file__, "..", "candidate_files"))
    PLAINTEXT_FREQUENCY = {}
    TRIGRAM = {}

    def __init__(self, ciphertext, plaintext_list, cipher_frequency, plaintext_frequency):
        self.ciphertext = ciphertext
        self.plaintext_list = plaintext_list
        self.cipher_frequency = cipher_frequency
        self.PLAINTEXT_FREQUENCY = plaintext_frequency
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
        #print(initial_key)
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
        #print(f"New Key: {new_key}")
        return new_key
    
    def pt_trigram(self):
        """Perform trigram analysis on the candidate plaintexts and the ciphertext."""
        file_body = self.plaintext_list
        for plaintext in file_body:
            self.candidate_count += 1
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
        #print(f"Sorted key: {key}")
        #alphabet = " abcdefghijklmnopqrstuvwxyz"
        decrypt_cipher = ""
        for i in range(len(ciphertext)):
            char = ciphertext[i].upper()
            decrypt_cipher += key[char].lower()
        return decrypt_cipher

    def get_lev_score(self, ciphertext):
        """Get the levenshtein distance between the ciphertext and all plaintext."""
        lev_dict = {}
        for plaintext_name, plaintext_body in candidate_dict.items():
            lev_score = lev(ciphertext, plaintext_body)
            print(f"Levenshtein distance between {plaintext_name} and the ciphertext: {lev_score}\n")
            lev_dict[plaintext_name] = lev_score
        return lev_dict
    
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
        print("HILL CLIMB STARTING WITH " + plaintext_name)
        parent_key = self.get_initial_key(plaintext_guess)
        iterations = len(parent_key) // 2
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
           # print(f"Child score with child key {child_key}: {child_score}\n")
            if child_score < parent_score:
                parent_score = child_score
                parent_key = child_key
           #     print(f"Parent score updated to {parent_score} with key {parent_key}\n")
            
            counter += 2
        
        print(f"Final parent key: {parent_key}\n")
        print(f"Final parent score: {parent_score}\n")

        # Get the final substitution of the ciphertext
        final_cipher = self.decrypt_cipher(ciphertext, parent_key)
        print(f"The final substitition of the ciphertext: {final_cipher}\n")

        # Get the levenstein distance between all the candidate plaintext and the ciphertext
        final_dist = self.get_lev_score(final_cipher)
        print(f"The levenstein distance between all plaintext and the ciphertext: {final_dist}\n")

        # Return the lowest levenstein distance
        lowest_dist = min(final_dist, key=final_dist.get)
        lowest_dist_val = final_dist[lowest_dist] #get actual int val 
        #print("lowest dist val: " + str(lowest_dist_val))
        print(f"The lowest levenstein distance: {lowest_dist}\n")

        print("End of hill climb.")
        return lowest_dist_val, lowest_dist

class Verify(HillClimb):

    def check_lev(self, threshold, lowest_lev_val, sorted_diffs, initial_guess_name):
        # if the levy score doesnt meet the threshold, try again with next candidate
        print("Start of check_lev")
        global_min = 0
        global_min_name = initial_guess_name
        if lowest_lev_val > threshold:
            global_min = lowest_lev_val

            for i in range(1, len(sorted_diffs)):
                next_lowest_diff = sorted_diffs[i]
                print(f"debug: {next_lowest_diff}")

                next_lowest_dist = self.PLAINTEXT_FREQUENCY[next_lowest_diff[0]]
                print("hello from check lev")
                lowest_lev_val, plaintext_guess_name = self.hill_climb(self.ciphertext, next_lowest_dist, next_lowest_diff[0])
                print("hello from check lev")
                global_min_name = plaintext_guess_name
                if global_min > lowest_lev_val:
                    global_min = lowest_lev_val
                    global_min_name = plaintext_guess_name
                if lowest_lev_val <= 550:
                    print("Final guess made from running multiple rounds of hill climbing: " + global_min_name)
                    break
                else:
                    print(f"Levenshtein distance still too high. Best guess so far is: {global_min} from candidate {global_min_name}")
        else:
            global_min = lowest_lev_val
            global_min_name = initial_guess_name
        return global_min, global_min_name

if __name__ == "__main__":

    # Measure the length of time it takes to run the attack
    start_time = datetime.now()

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
        hill_attack = HillClimb(randomized_cipher, candidate_list, cipher_freq, frequency_tables)

        difference_map = mono_attack.get_all_diffs(frequency_tables)
        sorted_diffs = sorted(difference_map.items(), key=lambda x: x[1])
        #print(f"debug: {sorted_diffs}")

        
        # Store the lowest difference
        lowest_diff = sorted_diffs[0]
        #print(f"debug: {lowest_diff}")
        lowest_plaintext_dist = frequency_tables[lowest_diff[0]]

        #lowest_plaintext_dist_debug = frequency_tables[lowest_diff[1]]
        #print(f"debug: {lowest_plaintext_dist}")

        # Perform hill climb

        lowest_lev_val, plaintext_guess_name = hill_attack.hill_climb(randomized_cipher, lowest_plaintext_dist, lowest_diff[0])

        

    # Run Test
    test_results = {"0": 0, "10": 0, "20": 0, "30": 0, "40": 0, "50": 0}
    for rand_prob in [0, 10, 20, 30, 40, 50]:
        for _ in range(100):
            key = mono_cipher.generate_monoalphabetic_key()
            rand_cand_num = random.randint(0, 4)
            selected_candidate = candidate_list[rand_cand_num]
            randomized_cipher = mono_cipher.coin_flip(rand_prob / 100, mono_cipher.encrypt(selected_candidate, key))
            mono_attack = Attack(randomized_cipher, frequency_tables)
            if rand_prob <= 10:
                plaintext_guess = mono_attack.improved_attack()
                if plaintext_guess == selected_candidate:
                    test_results[str(rand_prob)] += 1
            else:
                cipher_freq = mono_attack.get_cipher_frequency()
                hill_attack = HillClimb(randomized_cipher, candidate_list, cipher_freq, frequency_tables)
                difference_map = mono_attack.get_all_diffs(frequency_tables)
                sorted_diffs = sorted(difference_map.items(), key=lambda x: x[1])

                lowest_diff = sorted_diffs[0]
                lowest_plaintext_dist = frequency_tables[lowest_diff[0]]
                lowest_lev_val, plaintext_guess_name = hill_attack.hill_climb(randomized_cipher, lowest_plaintext_dist, lowest_diff[0])
                print("print pre check_lev")
                # check lev
                verify_attack = Verify(randomized_cipher, candidate_list, cipher_freq, frequency_tables)
                best_score, plaintext_guess_name = verify_attack.check_lev(550, lowest_lev_val, sorted_diffs, plaintext_guess_name)

                if candidate_dict[plaintext_guess_name] == selected_candidate:
                    test_results[str(rand_prob)] += 1
        
    for key, value in test_results.items():
        print(f"Randomness: {key}, Accuracy: {value / 100}\n")
    
    # End time of program and get the total time
    end_time = datetime.now()
    print(f"Total time of program: {end_time - start_time}\n")

        
        
        #plaintext_guess_body = candidate_dict[plaintext_guess_name]

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
   # print(f"Plaintext guess from input {candidate_num + 1}: {plaintext_guess_body}\n")
    print(f"Guess made with random character insertion probability: {random_prob}\n")
    print("End of program.")
