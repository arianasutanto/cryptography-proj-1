import random
import sys

def gen_output(input_string):
    return input_string.replace(" ", "").upper()

if __name__ == "__main__":
    plaintext = input("please provide a string to convert:\n")
    results = gen_output(plaintext)
    print(results)