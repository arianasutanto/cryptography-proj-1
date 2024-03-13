# Applied Cryptography - Project 1

### Mono-alphabetic Cipher Cracking

This repo contains a script in C that utilizes various techniques to attack the one-to-one random shift done by the mono-alphabetic cipher. 

### Cracking Techniques

Utilizing the improved attack suggested in the [KL] textbook, pp. 13-14. We will implement the following equation:

$$\sum_{i=0}^{25} p_i^{2} \approx 0.065$$

Here, $p_i$ is the probability of English letter as it appears in a common frequency table, with $i$ being noted as the associated number to an english character where $i \in \{0,\ldots,25\}$.

The idea is to calculate the probability of english character by counting the number of occurences of that character in the ciphertext, divided by the length of the ciphertext. This probability will be denoted as $q_i$. Once we have the probabilities of each ciphertext character, we query through different shift values $k \in \{1,\ldots,26\}$ until we find a probability that matches $p_i$ such that the following summation holds:

$$\sum_{i=0}^{25} p_i * q_{i+k} \approx 0.065$$

for independent values of $k$ for each english character. If the right probabilities are found for each character, the overall summation should be close to 0.065 within a certain threshold.

### Current Challenges

Struggling find probabilities of english characters that match the common english letter frequency table found online. Each candidate plaintext has a different ordering of letter probabilities, making this attack inaccurate for a handful of english letters. 

