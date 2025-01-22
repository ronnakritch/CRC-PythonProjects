import pyautogui
import time

def find_color_on_screen(target_color, tolerance=10):
    """
    Search for a specified color anywhere on the screen.
    :param target_color: Tuple of RGB values to find (R, G, B).
    :param tolerance: Allowable deviation for color matching.
    :return: Tuple (x, y) if the color is found, None otherwise.
    """
    screenshot = pyautogui.screenshot()
    screen_width, screen_height = screenshot.size
    for x in range(screen_width):
        for y in range(screen_height):
            pixel = screenshot.getpixel((x, y))
            if all(abs(pixel[i] - target_color[i]) <= tolerance for i in range(3)):
                return x, y
    return None

def click_color_continuously(target_color, tolerance=10):
    """
    Continuously searches for a color and clicks the position when found.
    :param target_color: Tuple of RGB values to find.
    :param tolerance: Allowable deviation for color matching.
    """
    print(f"Starting to look for color: {target_color}")
    while True:
        position = find_color_on_screen(target_color, tolerance)
        if position:
            print(f"Color {target_color} found at {position}. Clicking...")
            pyautogui.click(position)
            # Add a short delay after clicking to prevent multiple rapid clicks
            time.sleep(0.5)
        else:
            print("Color not found. Continuing to search...")
        # Reduce CPU usage slightly
       

# Define the target color to search for (R, G, B)
target_color = (42, 191, 255)  # Example color to detect
tolerance = 10  # Adjust this based on the shading tolerance

# Start the infinite search-and-click loop
click_color_continuously(target_color, tolerance)
