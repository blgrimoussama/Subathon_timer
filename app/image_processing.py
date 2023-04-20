from PIL import Image, ImageDraw, ImageOps
from io import BytesIO
import numpy as np
import requests

def round_image(url):
    # Load the image from the URL
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert('RGB')

    # Create a mask with rounded corners
    height,width = img.size
    lum_img = Image.new('L', [height,width] , 0)

    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(0,0), (height,width)], 0, 360,
        fill = 255)
    img_arr = np.array(img)
    lum_img_arr =np.array(lum_img)

    final_img_arr = np.dstack((img_arr,lum_img_arr))
    final_img = Image.fromarray(final_img_arr)

    return final_img

def byte_streamer(img):
    byte_stream = BytesIO()
    img.save(byte_stream, format='PNG')
    byte_stream.seek(0)
    
    return byte_stream

