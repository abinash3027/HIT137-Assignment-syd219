# Initialize total to 0
total = 0

# Outer loop runs 5 times (i from 0 to 4)
for i in range(5):
    # Inner loop runs 3 times (j from 0 to 2)
    for j in range(3):
        # Add (i+j) to total if the sum is 5
        if i + j == 5:
            total += i + j
        # Otherwise, subtract (i - j) from total
        else:
            total -= i - j

# Initialize a counter variable to 0
counter = 0

# A loop that runs until counter reaches 5
while counter < 5:
    # Increment total until it reaches 13
    if total < 13:
        total += 1
    # Decrease total if it's above 13
    elif total > 13:
        total -= 1
    # If total equals 13, increment counter by 2
    else:
        counter += 2

# After this loop, total will be 13 (the key for decryption)
key = total
print("Key for decryption:", key)
