#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

#define NUM_LETTERS 26

// Function to count the occurrences of each letter in the text
void count_letters(const char *text, int *letter_counts) {
    int i;
    for (i = 0; text[i] != '\0'; i++) {
        char c = text[i];
        if (isalpha(c)) {
            // Convert the letter to lowercase
            c = tolower(c);
            // Increment the corresponding count in the array
            letter_counts[c - 'a']++;
        }
    }
}

// Function to count the occurrences of each digram in the text
void count_digrams(const char *text, int *digram_counts) {
    int i;
    for (i = 0; text[i + 1] != '\0'; i++) {
        char c1 = tolower(text[i]);
        char c2 = tolower(text[i + 1]);
        if (isalpha(c1) && isalpha(c2)) {
            // Increment the corresponding count in the array
            digram_counts[(c1 - 'a') * NUM_LETTERS + (c2 - 'a')]++;
        }
    }
}

// Function to count the occurrences of each trigram in the text
void count_trigrams(const char *text, int *trigram_counts) {
    int i;
    for (i = 0; text[i + 2] != '\0'; i++) {
        char c1 = tolower(text[i]);
        char c2 = tolower(text[i + 1]);
        char c3 = tolower(text[i + 2]);
        if (isalpha(c1) && isalpha(c2) && isalpha(c3)) {
            // Increment the corresponding count in the array
            trigram_counts[(c1 - 'a') * NUM_LETTERS * NUM_LETTERS + (c2 - 'a') * NUM_LETTERS + (c3 - 'a')]++;
        }
    }
}

// Function to print the frequency of each letter
void print_frequency(int *letter_counts) {
    printf("Letter frequencies:\n");
    for (int i = 0; i < NUM_LETTERS; i++) {
        printf("%c: %d\n", 'a' + i, letter_counts[i]);
    }
}

// Function to print the frequency of each digram
void print_digram_frequency(int *digram_counts) {
    printf("Digram frequencies:\n");
    for (int i = 0; i < NUM_LETTERS; i++) {
        for (int j = 0; j < NUM_LETTERS; j++) {
            printf("%c%c: %d\n", 'a' + i, 'a' + j, digram_counts[i * NUM_LETTERS + j]);
        }
    }
}

// Function to print the frequency of each trigram
void print_trigram_frequency(int *trigram_counts) {
    printf("Trigram frequencies:\n");
    for (int i = 0; i < NUM_LETTERS; i++) {
        for (int j = 0; j < NUM_LETTERS; j++) {
            for (int k = 0; k < NUM_LETTERS; k++) {
                printf("%c%c%c: %d\n", 'a' + i, 'a' + j, 'a' + k, trigram_counts[i * NUM_LETTERS * NUM_LETTERS + j * NUM_LETTERS + k]);
            }
        }
    }
}

// Function to encrypt the plaintext with a random key
void encrypt_with_random_key(const char *plaintext, char *ciphertext, char *key) {
    srand(time(NULL)); // Seed the random number generator
    char alphabet[NUM_LETTERS];
    strcpy(alphabet, "abcdefghijklmnopqrstuvwxyz");

    // Shuffle the alphabet to create a random key
    for (int i = 0; i < NUM_LETTERS; i++) {
        int j = rand() % NUM_LETTERS;
        char temp = alphabet[i];
        alphabet[i] = alphabet[j];
        alphabet[j] = temp;
    }

    // Generate the random key
    strcpy(key, alphabet);

    // Generate the ciphertext using the random key
    for (int i = 0; plaintext[i] != '\0'; i++) {
        char c = plaintext[i];
        if (isalpha(c)) {
            char lowercase_c = tolower(c);
            int index = lowercase_c - 'a';
            if (isupper(c)) {
                ciphertext[i] = toupper(alphabet[index]);
            } else {
                ciphertext[i] = alphabet[index];
            }
        } else {
            ciphertext[i] = c;
        }
    }
    ciphertext[strlen(plaintext)] = '\0';
}

// Function to guess the random key based on frequency analysis
void guess_key(const char *ciphertext, char *key_guess) {
    int letter_counts[NUM_LETTERS] = {0};
    count_letters(ciphertext, letter_counts);

    int digram_counts[NUM_LETTERS * NUM_LETTERS] = {0};
    count_digrams(ciphertext, digram_counts);

    int trigram_counts[NUM_LETTERS * NUM_LETTERS * NUM_LETTERS] = {0};
    count_trigrams(ciphertext, trigram_counts);

    // Initialize variables to store the best score and key
    int best_score = 0;
    char best_key[NUM_LETTERS + 1];

    // Loop through all possible keys
    for (int shift = 0; shift < NUM_LETTERS; shift++) {
        char temp_key[NUM_LETTERS + 1];
        for (int i = 0; i < NUM_LETTERS; i++) {
            int index = (i + shift) % NUM_LETTERS;
            temp_key[i] = 'a' + index;
        }
        temp_key[NUM_LETTERS] = '\0';

        // Calculate score based on digram frequencies
        int score = 0;
        for (int i = 0; i < NUM_LETTERS; i++) {
            for (int j = 0; j < NUM_LETTERS; j++) {
                int index = i * NUM_LETTERS + j;
                char decrypted_char1 = temp_key[i];
                char decrypted_char2 = temp_key[j];
                int decrypted_index1 = decrypted_char1 - 'a';
                int decrypted_index2 = decrypted_char2 - 'a';
                score += digram_counts[index] * (letter_counts[decrypted_index1] + letter_counts[decrypted_index2]);
            }
        }

        // Calculate score based on trigram frequencies
        for (int i = 0; i < NUM_LETTERS; i++) {
            for (int j = 0; j < NUM_LETTERS; j++) {
                for (int k = 0; k < NUM_LETTERS; k++) {
                    int index = i * NUM_LETTERS * NUM_LETTERS + j * NUM_LETTERS + k;
                    char decrypted_char1 = temp_key[i];
                    char decrypted_char2 = temp_key[j];
                    char decrypted_char3 = temp_key[k];
                    int decrypted_index1 = decrypted_char1 - 'a';
                    int decrypted_index2 = decrypted_char2 - 'a';
                    int decrypted_index3 = decrypted_char3 - 'a';
                    score += trigram_counts[index] * (letter_counts[decrypted_index1] + letter_counts[decrypted_index2] + letter_counts[decrypted_index3]);
                }
            }
        }

        // Print score for the current key
        printf("Score for key '%s': %d\n", temp_key, score);

        // Update best score and key if necessary
        if (score > best_score) {
            best_score = score;
            strcpy(best_key, temp_key);
        }
    }

    // Copy the best key to the output variable
    strcpy(key_guess, best_key);
}


int main() {
    // Initialize an array to store the counts of each letter
    int letter_counts[NUM_LETTERS] = {0};

    // Example plaintext (replace this with your actual plaintext)
    const char *plaintext = "This is a secret message.";

    // Variables to store ciphertext and key
    char ciphertext[strlen(plaintext) + 1];
    char key[NUM_LETTERS + 1]; // +1 for null terminator
    char key_guess[NUM_LETTERS + 1]; // +1 for null terminator
    char decrypted_plaintext[strlen(plaintext) + 1];

    // Encrypt the plaintext with a random key
    encrypt_with_random_key(plaintext, ciphertext, key);

    // Print the random key
    printf("Random Key: %s\n", key);

    // Print the ciphertext
    printf("Ciphertext: %s\n", ciphertext);

    // Count the occurrences of each letter in the ciphertext
    count_letters(ciphertext, letter_counts);

    // Print the frequency of each letter in the ciphertext
    print_frequency(letter_counts);

    // Guess the random key based on frequency analysis
    guess_key(ciphertext, key_guess);

    // Print the guessed key
    printf("Guessed Key: %s\n", key_guess);

    return 0;
}
