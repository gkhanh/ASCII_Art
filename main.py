from PIL import Image


ASCII_CHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$" #67 chars
MAX_BRIGHTNESS_VALUE = 255


# Function to convert list of pixels to 2D array and return it as pixel matrix
def get_pixels_matrix(image):
    pixels = list(image.getdata())
    width, height = image.size
    pixels_matrix = [pixels[i:i+width] for i in range(0, len(pixels), width)]
    return pixels_matrix

# Function to get the specific RGB values of each pixel
def get_pixel_values(pixels_matrix):
    pixel_values = []
    for x in range(len(pixels_matrix)):
        for y in range(len(pixels_matrix[x])):
            pixel = pixels_matrix[x][y]
            pixel_values.append(pixel)
    return pixel_values

# Function to calculate the brightness of each pixel based on RGB values
def get_brightness_values_matrix(pixels_matrix, algorithm="average"):
    brightness_values_matrix = []
    for row in pixels_matrix:
        brightness_value_row = []
        for pixel in row:
            if algorithm == "average":
                brightness = (pixel[0] + pixel[1] + pixel[2])/3
            elif algorithm == "min_max":
                brightness = (max(pixel[0], pixel[1], pixel[2]) + min(pixel[0], pixel[1], pixel[2]))/2
            elif algorithm == "luminosity":
                brightness = (0.21*pixel[0] + 0.72*pixel[1] + 0.07*pixel[2])
            else:
                raise Exception("Invalid algorithm: %s" % algorithm)
            brightness_value_row.append(brightness)
        brightness_values_matrix.append(brightness_value_row)

    return brightness_values_matrix

def convert_bright_mode_to_dark_mode(brightness_values_matrix):
    inverted_brightness_values_matrix = []
    for row in brightness_values_matrix:
        inverted_brightness_value_row = []
        for pixel in row:
            brightness = int(MAX_BRIGHTNESS_VALUE - pixel)
            # print(f"Original: {pixel}, Inverted: {brightness}")
            inverted_brightness_value_row.append(brightness)
        inverted_brightness_values_matrix.append(inverted_brightness_value_row)

    return inverted_brightness_values_matrix

# Function to normalize brightness values
def normalize_brightness_values_matrix(intensity_matrix):
    normalized_intensity_matrix = []
    max_pixel = max(map(max, intensity_matrix))
    min_pixel = min(map(min, intensity_matrix))
    for row in intensity_matrix:
        rescaled_row = []
        for p in row:
            r = MAX_BRIGHTNESS_VALUE * (p - min_pixel) / float(max_pixel - min_pixel)
            rescaled_row.append(r)
        normalized_intensity_matrix.append(rescaled_row)

    return normalized_intensity_matrix

# function to convert brightness to ASCII chars
def convert_brightness_value_to_ASCII_char(brightness_values_matrix, ascii_chars):
    ascii_matrix = []
    for row in brightness_values_matrix:
        ascii_row = []
        for brightness in row:
            index = int((brightness / MAX_BRIGHTNESS_VALUE) * (len(ascii_chars) - 1))
            ascii_row.append(ascii_chars[index])
        ascii_matrix.append(ascii_row)
    return ascii_matrix

def print_ascii_matrix(ascii_matrix):
    for row in ascii_matrix:
        print("".join(row))



def resize_image(image, new_width=230):
    # Resize the image to fit terminal width, maintaining aspect ratio.
    original_width, original_height = image.size
    aspect_ratio = original_height / original_width
    new_height = int(aspect_ratio * new_width * 0.5) # shrink the height to 50% of original
    return image.resize((new_width, new_height))


if __name__ == "__main__":
    filepath = "images/test4.jpg"

    # Process the captured image
    img = Image.open(filepath)
    img = resize_image(img, new_width=230)  # Resize to fit terminal
    # img = img.convert("RGB")  # Ensure it's in RGB mode
    pixels = get_pixels_matrix(img)

    # algorithm_mode = "average"
    # algorithm_mode = "min_max"
    algorithm_mode = "luminosity"


    intensity_matrix = get_brightness_values_matrix(pixels, algorithm_mode)

    intensity_matrix = normalize_brightness_values_matrix(intensity_matrix)

    inverted_intensity_matrix = convert_bright_mode_to_dark_mode(intensity_matrix)

    # Bright mode
    # ascii_matrix = convert_brightness_value_to_ASCII_char(intensity_matrix, ASCII_CHARS)

    # Dark mode
    ascii_matrix = convert_brightness_value_to_ASCII_char(inverted_intensity_matrix, ASCII_CHARS)

    print_ascii_matrix(ascii_matrix)