from PIL import Image
# import time
#
# current_time = int(time.time())
# generated_number = (current_time % 100) + 50
#
# if generated_number % 2 == 0:
#     generated_number += 10


# Open the image
img = Image.open('chapter1.jpg')

# Get image data as a list of pixel values (r, g, b)
pixels = img.load()

# The value of n from the algorithm (assumed, since it's not given in the document)
n = 143

# Create a new image to store the updated pixels
new_img = Image.new('RGB', img.size)

# Initialize the sum of red pixel values
red_sum = 0

# Loop through all the pixels
for i in range(img.width):
    for j in range(img.height):
        r, g, b = pixels[i, j]
        # Modify the pixel values by adding n
        new_r = r + n
        new_g = g + n
        new_b = b + n

        # Store the updated pixel values in the new image
        new_img.putpixel((i, j), (new_r, new_g, new_b))

        # Add the red value to the red_sum
        red_sum += new_r

# Save the modified image as 'chapter1out.png'
new_img.save('chapter1out.jpg')

# Print the sum of red values
print(f"Sum of all red pixel values: {red_sum}")
