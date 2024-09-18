import nltk
from nltk.corpus import words
import string

# Load the list of valid English words
english_words = set(words.words())

# Ciphered cryptogram
ciphered_quote = "VZ FRYSVFU VZCNGVRAG NAQ N YVGGYR VAFPRHER V NZ BHG BS PBAGEBY NAQNG GVZRF UNEQ GB UNAQYR OHG VS LBH PNAG UNAQYR ZR NG ZL JBEFG GURA LBH FHER NF URYYQBAG QRFRER ZR NG ZL ORFG ZNEVYL ZBAEBR"


# Function to decrypt using a shift key
def decrypt_caesar_cipher(cipher_text, shift):
    decrypted_text = []
    for char in cipher_text:
        if char.isalpha():
            shifted = ord(char) - shift
            if char.isupper():
                if shifted < ord('A'):
                    shifted += 26
            elif char.islower():
                if shifted < ord('a'):
                    shifted += 26
            decrypted_text.append(chr(shifted))
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)


# Function to check if the decrypted quote has valid English words
def evaluate_decryption(text):
    words_in_text = text.split()
    valid_word_count = 0
    total_word_length = 0
    for word in words_in_text:
        cleaned_word = word.strip(string.punctuation).lower()  # Clean punctuation and convert to lowercase
        if cleaned_word in english_words:
            valid_word_count += 1
            total_word_length += len(cleaned_word)

    # Weight the evaluation: more valid words and longer word length are better
    total_words = len(words_in_text)
    avg_word_length = total_word_length / total_words if total_words > 0 else 0
    return valid_word_count, avg_word_length


# Try all possible shift values to find the original quote
best_shift = None
best_score = 0
best_decryption = None

for s in range(1, 27):
    decrypted_quote = decrypt_caesar_cipher(ciphered_quote, s)
    valid_word_count, avg_word_length = evaluate_decryption(decrypted_quote)

    # Score the decryption based on the number of valid words and average word length
    score = valid_word_count * avg_word_length

    print(f"Shift {s}: {decrypted_quote}")
    print(f"  Valid words: {valid_word_count}, Average word length: {avg_word_length}, Score: {score}\n")

    if score > best_score:
        best_score = score
        best_shift = s
        best_decryption = decrypted_quote

print(f"\nBest Shift: {best_shift}")
print(f"Decrypted message: {best_decryption}")
