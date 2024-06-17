
import json
import os
import random
import string
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, send_file, render_template_string
import pandas as pd
import requests

import constants

from get_shopify_data import process_products


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
invalid_url_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invalid URL</title>
</head>
<body>
    <script>
        alert("Invalid Shopify link. Please provide a valid link.");
        window.location.href = "/";
    </script>
</body>
</html>
"""
# def generate_name():
#    return ''.join(random.choices(string.ascii_uppercase +
#                              string.digits, k=4))

# def update_constants(brand_code,brand_name):
#      with open('constants.py', 'w') as f:
#         f.write(f"brandCode='{brand_code}'\n")
#         f.write(f"brandName='{brand_name}'\n")
#         f.write(f"brandDataDir=f'data/{{brandCode}}/'\n")
#         f.write(f"brandOutputDir=f'output/{{brandCode}}/'\n")
#         f.write(f"productDataFile=f'{{brandDataDir}}PXM_{{brandCode}}_products.json'\n")
#         f.write(f"outputFile=f'{{brandOutputDir}}PXM_{{brandCode}}_products.xlsx'\n")
#         f.write(f"imagesFolder=f'{{brandOutputDir}}images/'\n")
#         f.write(f"categoryLinksFolder=f'{{brandDataDir}}categories/'\n")


def get_categories(link, categoryLinkElt, categoryLinkClass):
    print("inside get category", link)

    categoryLinks = []
    response = requests.get(link, headers=constants.headers).text
    soup = BeautifulSoup(response, 'html.parser')
    categories = soup.find_all(categoryLinkElt, {
                               "class": categoryLinkClass})

    for i, category in enumerate(categories):
        categoryLink = category.find("a").get("href")
        if categoryLink not in categoryLinks:

            categoryLinks.append(categoryLink)

    with open(constants.categoryLinksFile, 'w') as file:
        json.dump(categoryLinks, file)
    print(categoryLinks)

    return categoryLinks


def get_category_links(getCategoriesURL, categoryLinkElt, categoryLinkClass):
    print("inside get category links")
    # if os.path.isfile(constants.categoryLinksFile):
    #     with open(constants.categoryLinksFile, 'r') as j:
    #         categoryLinks = json.load(j)
    # else:

    categoryLinks = get_categories(
        getCategoriesURL, categoryLinkElt, categoryLinkClass)

    return categoryLinks


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/main', methods=['POST'])
def main():
    baseurl = request.form.get('url')
    print("got url", baseurl)

    getCategoriesURL = request.form.get('shopurl')
    print(getCategoriesURL, "shopurl")

    categoryLinkElt = request.form.get('catlinkelt')
    print(categoryLinkElt,"element")

    categoryLinkClass = request.form.get('catlinkclass')
    print(categoryLinkClass, "class")

    # json_url = f"{baseurl}/products.json?limit=250&page=1"
    # response = requests.get(json_url)

    # if response.status_code == 200:

    #     products = process_products(baseurl)

    # else:
    print("inside else")
    productLinks = get_category_links(
        getCategoriesURL, categoryLinkElt, categoryLinkClass)
    print(productLinks)

    return render_template('categories.html', productLinks=productLinks)

    # df = pd.DataFrame(products)
    # df = df.sort_values(by=['Name'])
    # df.to_excel(constants.outputFile, index=False)
    # table_html = df.head(10).to_html(classes='data', header="true")
    # return render_template('result.html', tables=[table_html])


@app.route('/download')
def download_file():
    output_path = constants.outputFile
    return send_file(output_path, as_attachment=True, download_name='products.xlsx')


if __name__ == '__main__':
    app.run(debug=True)
