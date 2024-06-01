import os
import shutil
import string
import constants
import requests
import random

def save_images(soup, model_id):
    imageLinks = get_image_links(soup)
    result = download_images(model_id, imageLinks)

    return result
def get_image_links(soup):
    imageLinks = []
    try:
        figures = soup.find(
            constants.productImgElt, {"class": constants.productImgClass}).find_all("img")

        for figure in figures:
            image = figure.get("data-original")
            if not image:
                image = figure.get("src").replace("-100x100", "")
                image = image.replace("-600x600", "")
                image = image.replace("-150x150", "")

            if image not in imageLinks:
                imageLinks.append(image)
    except:
        pass

    return imageLinks

def create_images_dir(model_id):
    images_dir = constants.imagesFolder + model_id
    
    if not os.path.exists(images_dir):
        os.mkdir(images_dir)
        
    return images_dir


def download_images(model_id, image_links):
    images_dir = create_images_dir(model_id)
    count = 0
    for i, image_link in enumerate(image_links):
        r = requests.get(image_link, headers=constants.headers).content
        try:
            # possibility of decode
            r = str(r, 'utf-8')
        except UnicodeDecodeError:
            # After checking above condition, Image Download start
            image_name = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=4))
            print(image_name)
            image_dir_path = f"{images_dir}/{image_name}"
            if not os.path.isfile(image_dir_path):
                with open(image_dir_path, "wb+") as f:
                    f.write(r)

                # counting number of image downloaded
                count += 1

    return image_links

def download_shopify_images(model_id, image_links):
    print(image_links)
    images_dir = create_images_dir(model_id)
    for i, image_link in enumerate(image_links):
        image_name = os.path.basename(image_link).split("?")[0] 
        image_dir_path = f"{images_dir}/{image_name}"

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(image_link, stream=True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            if not os.path.isfile(image_dir_path):
                with open(image_dir_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

                # print('Image successfully Downloaded: ', image_dir_path)
        else:
            print('Image Couldn\'t be retrieved')