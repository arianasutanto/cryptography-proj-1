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

// Function to print the frequency of each letter
void print_frequency(int *letter_counts) {
    printf("Letter frequencies:\n");
    for (int i = 0; i < NUM_LETTERS; i++) {
        printf("%c: %d\n", 'a' + i, letter_counts[i]);
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

    // Calculate the most frequent letter in the ciphertext
    int max_count = 0;
    char most_frequent_letter;
    for (int i = 0; i < NUM_LETTERS; i++) {
        if (letter_counts[i] > max_count) {
            max_count = letter_counts[i];
            most_frequent_letter = 'a' + i;
        }
    }

    // Assuming the most frequent letter in English is 'e',
    // calculate the shift required to decrypt the ciphertext
    int shift = most_frequent_letter - 'e';

    // Apply the shift to generate the guessed key
    for (int i = 0; i < NUM_LETTERS; i++) {
        int index = (i + shift) % NUM_LETTERS;
        key_guess[i] = 'a' + index;
    }
    key_guess[NUM_LETTERS] = '\0';
}

// Function to decrypt the ciphertext using the guessed key
void decrypt_with_key(const char *ciphertext, const char *key, char *plaintext) {
    for (int i = 0; ciphertext[i] != '\0'; i++) {
        char c = ciphertext[i];
        if (isalpha(c)) {
            char lowercase_c = tolower(c);
            int index = c - 'a';
            char decrypted_char = key[index];
            if (isupper(c)) {
                plaintext[i] = toupper(decrypted_char);
            } else {
                plaintext[i] = decrypted_char;
            }
        } else {
            plaintext[i] = c;
        }
    }
    plaintext[strlen(ciphertext)] = '\0';
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

    // Decrypt the ciphertext using the guessed key
    decrypt_with_key(ciphertext, key_guess, decrypted_plaintext);

    // Print the decrypted plaintext
    printf("Decrypted Plaintext: %s\n", decrypted_plaintext);

    return 0;
}
