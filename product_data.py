
import re
import constants

from utils import remove_whitespaces


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