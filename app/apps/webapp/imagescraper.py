from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from PIL import Image
from io import BytesIO

def get_largest_image(url):
    # Set up headless Chrome browser
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the webpage
        driver.get(url)

        # Execute JavaScript to get all images and their sizes
        images = driver.execute_script('''
            const images = [...document.getElementsByTagName('img')];
            return images.map(img => {
                return {
                    src: img.src,
                    width: img.naturalWidth,
                    height: img.naturalHeight
                };
            });
        ''')

        # Find the largest image
        largest_image = None
        largest_size = 0

        for img in images:
            width = img['width']
            height = img['height']
            size = width * height

            if size > largest_size:
                largest_size = size
                largest_image = img['src']

        if largest_image:
            # Handle relative URLs
            if largest_image.startswith('//'):
                largest_image = 'http:' + largest_image
            elif largest_image.startswith('/'):
                largest_image = url + largest_image

            try:
            #   Step 5: Download the image to get its actual size
                img_response = requests.get(largest_image)
                img_data = Image.open(BytesIO(img_response.content))
                img_data.show()
                return img_data

            except Exception as e:
                print(f"Failed to process image {largest_image}: {e}")
                return None
    finally:
        driver.quit()