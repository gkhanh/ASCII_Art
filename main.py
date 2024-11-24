from PIL import Image

img = Image.open("img.png")
# img.show()

# Function to convert list of pixels to 2D array and return it as pixel matrix
def convert_list_of_pixels_to_2D_array(image):
    pixels = list(image.getdata())
    width, height = image.size
    pixel_matrix = [pixels[i:i+width] for i in range(0, len(pixels), width)]
    return pixel_matrix

# Function to access to a specific pixel
def access_to_pixel(pixel_matrix):
    pixel_value = []
    for x in range(len(pixel_matrix)):
        for y in range(len(pixel_matrix[x])):
            pixel = pixel_matrix[x][y]
            pixel_value.append(pixel)
    return pixel_value

# Function to convert rgb to brightness
def convert_to_brightness(pixel):
    return (pixel[0] * 0.3) + (pixel[1] * 0.59) + (pixel[2] * 0.11)

if __name__ == '__main__':
    rows = convert_list_of_pixels_to_2D_array(img)

    # Print success messages
    print("Successfully constructed pixel matrix!")
    print("Pixel matrix size:", img.width, "x", img.height)
    print("Iterating through pixels...")

    for pixel in access_to_pixel(rows):
        print(pixel)