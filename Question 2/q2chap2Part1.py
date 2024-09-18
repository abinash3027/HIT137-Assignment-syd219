# Given string
s = '56aAww1984sktr235270aYmn145ss785fsq31D0'

# Separate into numbers and letters
number_string = ''.join([char for char in s if char.isdigit()])
letter_string = ''.join([char for char in s if char.isalpha()])

# Convert even numbers in number string to ASCII code
even_numbers = [num for num in number_string if int(num) % 2 == 0]
ascii_even_numbers = [ord(num) for num in even_numbers]

# Convert uppercase letters in letter string to ASCII code
uppercase_letters = [char for char in letter_string if char.isupper()]
ascii_uppercase_letters = [ord(char) for char in uppercase_letters]

# Print the results
print(f"Number String: {number_string}")
print(f"Letter String: {letter_string}")
print(f"Even Numbers: {even_numbers}")
print(f"ASCII Code of Even Numbers: {ascii_even_numbers}")
print(f"Uppercase Letters: {uppercase_letters}")
print(f"ASCII Code of Uppercase Letters: {ascii_uppercase_letters}")
