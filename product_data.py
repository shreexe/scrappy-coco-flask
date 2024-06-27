
import json
import re

from bs4 import BeautifulSoup
import requests
import constants

from product_image_data import download_images, save_images
from utils import check_dimensions_regex, get_model_id, process_dimensions, remove_whitespaces, sanitize_price, standardize_dimensions


def get_data_from_desc(desc_soup, search_str, array=None, showLabel=False):
    try:
        desc_div = desc_soup(text=re.compile(search_str, re.IGNORECASE))

        data = ""
        for elt in desc_div:
            elt_text = remove_whitespaces(str(elt))
            if array and elt_text in array:
                parent = remove_whitespaces(elt.parent.text)
                if array and parent in array:
                    grandparent = remove_whitespaces(elt.parent.parent.text)
                    if array and grandparent in array:
                        data += remove_whitespaces(
                            elt.parent.parent.parent.text) + " "
                    else:
                        data += grandparent + " "
                else:
                    data += parent + " "
            else:
                data += elt_text + " "

        if not showLabel:
            for d in array:
                data = data.replace(d, " ")
        # print(search_str, data)

    except:
        data = None

    return data


def format_product_data(model_id, sku, description, name, mrp, dimensions, link, colors, category, sub_category, material, shipping, attribute, images, var_image, discounted_price, short_description, dimension_data, std_dimensions):
    return {
        "Model ID": model_id,
        "NAS Address": None,
        "Brand": constants.brandName,
        "SKU": sku,
        "Description": description,
        "Name": name,
        "Price": mrp,
        "Dimensions": dimensions,
        "Weblink": link,
        "Web_Colour": colors,
        "Web_Category": category,
        "Web_Sub_Category": sub_category,
        "Web_Material": material,
        "Shipping": shipping,
        "Variants": attribute,
        "Images": images,
        "Variant Image": var_image,
        "Discounted Price": discounted_price,
        "Short Description": short_description,
        "Dimension Data": dimension_data,
        "Standardized Dimensions": std_dimensions
    }

def get_sku(soup):
    try:
        sku_array = ["Sku: ", "Sku:", "Sku", "SKU:"]
        sku = soup.find(
            "span", {"class": "sku"})
        if sku:
            sku = sku.text
        else:
            desc_soup = soup.find("div", {"id": constants.descTabId})
            sku = get_data_from_desc(desc_soup, "sku", sku_array)
    except:
        sku = None

    return remove_whitespaces(sku)


def get_name(soup):
    try:
        name = soup.find("h1", {"class": "product_title"}).text
    except:
        name = None

    return name


def get_category(soup):
    try:
        category = soup.find(
            constants.breadcrumbsElt, {"class": constants.breadcrumbsClass}).find_all('a')
        category = category[constants.categoryIndex].text
    except:
        category = None

    return category


def get_sub_category(soup):
    try:
        sub_category = soup.find(
            "span", {"class": "posted_in"}).text
        sub_category = sub_category.replace("Category: ", "")
        sub_category = sub_category.replace("Categories: ", "")
    except:
        sub_category = None

    return sub_category


def get_short_description(soup):
    try:
        short_description = soup.find(
            "div", {"class": "woocommerce-product-details__short-description"}).text
    except:
        short_description = None

    return remove_whitespaces(short_description)


def get_description(soup):
    try:
        description = soup.find(
            "div", {"id": "tab-description"}).text
        description = description
    except:
        description = None

    return remove_whitespaces(description)


def get_shipping(soup):
    try:
        shipping = soup.find(
            "ul", {"class": "mf-shipping-info"})
        if shipping:
            shipping = shipping.text
        else:
            shipping = soup.find(
                "div", {"id": constants.productShippingTabId}).text
    except:
        shipping = None

    return remove_whitespaces(shipping)


def get_data_from_addn_info(soup, search_str, show_label=True):
    try:
        rows = soup.find(
            "div", {"id": constants.addnInfoTabId}).find_all("tr")
        data = ""
        for row in rows:
            label = row.find(
                "th", {"class": "woocommerce-product-attributes-item__label"})
            if label:
                label = label.text
                if search_str in label:
                    value = row.find(
                        "td", {"class": "woocommerce-product-attributes-item__value"})
                    if value:
                        value = value.text
                        if show_label:
                            data += f"{label}: {value} "
                        else:
                            data += f"{value} "
                            data = data.replace(search_str, "")
                            data = data.replace(":", "")

    except:
        data = None

    return data
def get_data(soup, search_str, array=None, show_label=True, multi_search=False, tab_id=constants.descTabId):
    data = get_data_from_addn_info(soup, search_str, show_label)

    if not data:
        if multi_search:
            search_str = multi_search
        desc_soup = soup.find("div", {"id": tab_id})
        data = get_data_from_desc(desc_soup, search_str, array)
        if not data:
            short_desc_soup = soup.find(
                "div", {"class": "woocommerce-product-details__short-description"})
            data = get_data_from_desc(short_desc_soup, search_str, array)

    return remove_whitespaces(data)


def get_dimensions(soup):
    search_str = "Dimension"
    dimension_array = [
        "Product Dimensions: ", "Product Dimensions:", "Product Dimension:", "Product Dimension", "Dimensions:", "Dimension:", "Dimension: ", "Dimension:", "Dimensions: ", "Dimensions:", "Dimensions(CMS)", "Dimensions", "Dimension", "DIMENSIONS-", "DIMENSIONS: ", "DIMENSIONS:"]

    multi_search = "Dimension|Length|Depth|Height|Width|Size"

    return get_data(soup, search_str, dimension_array, multi_search=multi_search, tab_id=constants.dimensionTabId)


def get_material(soup):
    search_str = "Material"
    material_array = ["Material Content: ", "Material Content:", "Primary Material: ", "Primary Material:", "Primary Material", "Secondary Material:",
                      "Secondary Material", "Material : ",  "Material :", "Material: ",  "Material:", "Material", "MATERIAL: ", "MATERIAL:", "MATERIAL", "CONSTRUCTION-"]

    multi_search = "Material|Construction"
    material = (get_data(soup, search_str, material_array,
                multi_search=multi_search, show_label=False))
    print(material)
    return material


def get_colors(soup):
    search_str = "Color"

    return get_data(soup, search_str, None, False)


def get_attribute_colors(soup, key):
    select = soup.find("select", {"data-attribute_name": key})
    attr_colors = key + ": "
    for option in select.find_all('option'):
        if option['value'] != "":
            attr_colors += option.text + ", "

    return attr_colors


def get_price(soup):
    try:
        price = soup.find(
            "p", {"class": "price"})
        ins_price = price.find('ins')
        if ins_price:
            discounted_price = ins_price.text
        del_price = price.find('del')
        if del_price:
            mrp = del_price.text
        if not ins_price and not del_price:
            mrp = price.text
            discounted_price = None
    except:
        mrp = None
        discounted_price = None

    return sanitize_price(mrp), sanitize_price(discounted_price)


def get_product_data(baseURL, link):
    data = requests.get(link, headers=constants.headers).text
    soup = BeautifulSoup(data, "html.parser")

    # Get product data
    sku = get_sku(soup)

    name = get_name(soup)

    category = get_category(soup)

    sub_category = get_sub_category(soup)

    short_description = get_short_description(soup)

    description = get_description(soup)

    shipping = get_shipping(soup)

    dimension_data = get_dimensions(soup)
    processed_dim = process_dimensions(dimension_data)
    dimension_matches = check_dimensions_regex(processed_dim)

    if len(dimension_matches) > 0:
        std_dimensions = standardize_dimensions(dimension_matches)
        # check if LxBxH has been extracted
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

    material = get_material(soup)

    colors = get_colors(soup)

    variationsForm = soup.find(
        "form", {"class": "variations_form"})

    productData = []
    if variationsForm:
        variations_data = variationsForm.get("data-product_variations")
        if variations_data:
            var_json = json.loads(variations_data)
            if var_json:
                for i, variant in enumerate(var_json):
                    sku = variant["sku"] if variant["sku"] else sku
                    discounted_price = variant["display_price"]
                    mrp = variant["display_regular_price"]

                    # Get all attributes
                    attribute = ""
                    try:
                        attributes = variant["attributes"]
                        for key in attributes:
                            attribute += attributes[key] + " "
                            if "color" in key:
                                if not colors:
                                    colors = ""
                                colors += get_attribute_colors(soup, key)
                        # print(colors)
                    except:
                        attributes = ""
                        attribute = i + 1

                    attr = remove_whitespaces(str(attribute))

                    # Generate model id with link sku and attr data
                    model_id = get_model_id(
                        link + sku + attr, constants.brandCode)

                    # Save images
                    images = save_images(soup, model_id)
                    # images = get_image_links(soup)

                    try:
                        var_image = variant["image"]["src"]
                        download_images(model_id, [var_image])
                    except:
                        var_image = None

                    if var_image:
                        images.append(var_image)

                    if not attr == "":
                        var_name = name + " - " + attr
                    else:
                        var_name = name

                    print(var_name, sku, attribute, attributes)

                    variantData = format_product_data(model_id, sku, description, var_name, mrp, dimensions, link, colors,      category, sub_category,
                                                      material, shipping, attributes, images, var_image, discounted_price, short_description, dimension_data, std_dimensions)

                    productData.append(variantData)

        else:
            model_id = get_model_id(
                link + sku, constants.brandCode)

            # Save images
            images = save_images(soup, model_id)
            # images = get_image_links(soup)

            mrp, discounted_price = get_price(soup)

            attributes = ""
            json_script = soup.find(
                "script", {"class": "yoast-schema-graph--footer"})
            if json_script:
                json_string = json_script.string
                if json_string:
                    try:
                        var_json = json.loads(json_string)
                        attributes = var_json["@graph"][0]["offers"][0]["offers"]
                        # print(attributes)
                    except:
                        attributes = "Has variants"

            variantData = format_product_data(model_id, sku, description, name, mrp, dimensions, link, colors,      category, sub_category,
                                              material, shipping, attributes, images, None, discounted_price, short_description, dimension_data, std_dimensions)

            productData.append(variantData)

    else:
        # Generate model id
        model_id = get_model_id(link, constants.brandCode)

        # Save images
        images = save_images(soup, model_id)
        # images = get_image_links(soup)

        mrp, discounted_price = get_price(soup)

        single_prod_data = format_product_data(model_id, sku, description, name, mrp, dimensions, link, colors, category,
                                               sub_category, material, shipping, None, images, None, discounted_price, short_description, dimension_data, std_dimensions)

        productData.append(single_prod_data)

    return productData
