import json
from bs4 import BeautifulSoup
import requests
from product_data import format_product_data, get_data_from_desc
from utils import check_dimensions_regex, get_model_id, process_dimensions, remove_whitespaces, sanitize_price, standardize_dimensions
from product_image_data import download_images, download_shopify_images
import constants



def get_dimensions(soup):
    search_str = "Dimension"
    dimension_array = constants.dimension_array
    multi_search = "Dimension|Length|Depth|Height|Width|Size|Measurement"

    dimension_data = get_data_from_desc(soup, multi_search, dimension_array, showLabel=True)
    processed_dim = process_dimensions(dimension_data)
    dimension_matches = check_dimensions_regex(processed_dim)

    if len(dimension_matches) > 0:
        std_dimensions = standardize_dimensions(dimension_matches)
        if len(std_dimensions) == 1 and len(std_dimensions[0]) == 3:
            dimensions = std_dimensions[0]
        else:
            std_dimensions = standardize_dimensions([processed_dim])
    else:
        std_dimensions = standardize_dimensions([processed_dim])

    if len(std_dimensions) == 1 and len(std_dimensions[0]) == 3:
        dimensions = std_dimensions[0]
    else:
        dimensions = dimension_data

    return dimension_data, std_dimensions, dimensions


def process_products(baseurl):
    print("inside process")
    products = get_products(baseurl)

    productList = []
    for i, product in enumerate(products, start=1):
        productData = parse_product_data(product, baseurl)
        print(f'Processing {i} product {productData[0]["Name"]}...')
        productList += productData

    return productList

def get_products(baseURL):
    print("inside get_products")
    url = baseURL + 'products.json?limit=250&page={}'
    products = []
    for pageNo in range(1, constants.totalPages):
        productsURL = url.format(pageNo)
        print(productsURL)
        req = requests.get(productsURL, headers=constants.headers)
        productsJSON = req.json()
        if len(productsJSON['products']) > 0:
            products += productsJSON['products']
        else:
            break

    with open(constants.productDataFile, 'w') as file:
        json.dump(products, file)

    print(len(products))

    return products


def parse_product_data(product, baseURL):
    print("inside parse")
    name = product['title']
    link = baseURL + '/products/' + product['handle']
    category = product['product_type']
    sub_category = product['tags']
    short_description = None
    body_html = product['body_html']
    body_soup = BeautifulSoup(body_html, "html.parser")
    description = remove_whitespaces(body_soup.text)
    shipping = get_data_from_desc(body_soup, "Shipping")
    dimension_data, std_dimensions, dimensions = get_dimensions(body_soup)
    material = get_material(body_soup)
    colors = get_data_from_desc(body_html, "Color")
    images = [image["src"] for image in product['images']]
    

    productData = []
    for variant in product['variants']:
        attribute = variant['title']
        if attribute == "Default Title":
            var_name = name
        else:
            var_name = name + " - " + attribute
        sku = variant['sku'] if variant['sku'] else ""
        model_id = get_model_id(link + sku + attribute, constants.brandCode)
        # download_shopify_images(model_id, images)

        # try:
        #     var_image = variant['featured_image']['src'] if variant.get('featured_image') else None
        #     if var_image:
        #         # download_images(model_id, [var_image])
        # except:
        #     var_image = None

        mrp = sanitize_price(variant["compare_at_price"])
        discounted_price = sanitize_price(variant["price"])
        if not mrp:
            mrp = discounted_price

        variantData = format_product_data(model_id, sku, description, var_name, mrp, dimensions, link, colors, category, sub_category,
                                          material, shipping, attribute, images, var_image, discounted_price, short_description, dimension_data, std_dimensions)

        productData.append(variantData)

    return productData



def get_material(soup):
    search_str = "Material"
    material_array = constants.material_array
    multi_search = "Material|Construction"
    material = get_data_from_desc(soup, multi_search, material_array)
    print(material)
    return material