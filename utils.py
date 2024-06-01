from hashlib import sha1
import pathlib
import constants
import re
from quantulum3 import parser


def remove_whitespaces(string):
    if string:
        string = string.strip().replace("\n", " ")
        string = " ".join(string.split())
        return string

    return string


def sanitize_price(value):
    if value:
        value = value.replace("₹", "")
        value = value.replace(",", "")
        value = value.replace("Rs.", "")
        value = value.replace("Price:", "")
        value = value.replace("Offer:", "")
        value = remove_whitespaces(value)
        try:
            value = float(value)
            return int(value)  
        except:
            return value

    return value


def check_dimensions_regex(value):
    try:
        unit_regex = r"*(?:(?:in(?:ch)(?:es)?|\"|″|”|cm |cms|cm|CM)"
        by_regex = r"?(?:x|by|\*|X|)"

        # len_regex = r"(?:L|\(L\)| L|W|\(W\)| H|H)"
        # breadth_regex = r"(?: H|\(H\)|W|\(W\)| W)"
        # height_regex = r"(?: D|\(D\)|H|\(H\)| D)"
        # regex = f"(?<!\S)(\d+(?:.\d+)?) {unit_regex}{addn_regex}?)? {by_regex} ?(\d+(?:.\d+)?)(?: {by_regex} ?\d+(?:.\d+)?)* {unit_regex}{addn_regex}?)?(?: {by_regex} ?(\d+(?:.\d+)?))* {unit_regex}{addn_regex}?)?"

        addn_regex = r"(?:L| L|\(L\)| \(L\)|D| D|\(D\)| \(D\)|H| H|\(H\)| \(H\)|W| W|\(W\)| \(W\))"
        regex = f"(?<!\S)(\d+(?:.\d+)?) {unit_regex}{addn_regex}?)?(?: {by_regex} ?(\d+(?:.\d+)?))* {unit_regex}{addn_regex}?)?(?: {by_regex} ?(\d+(?:.\d+)?))* {unit_regex}{addn_regex}?)?"

        matches = re.finditer(regex, value)

        dimensions = []
        for matchNum, match in enumerate(matches, start=1):
            # print("Match {matchNum} was found at {start}-{end}: {match}".format(
            #     matchNum=matchNum, start=match.start(), end=match.end(), match=match.group()))
            dimension = match.group().replace('”', '"')
            if not dimension.isdigit():
                dimension = process_dimensions(dimension)
                dimensions.append(dimension)
    except:
        dimensions = []

    return dimensions


def process_dimensions(dim):
    try:
        dimension = dim.replace("x", " x ")
        dimension = dimension.replace("X", " x ")
        dimension = dimension.replace("*", " x ")
        dimension = dimension.replace("-", " ")
        dimension = dimension.replace("Inches", "Inches ")
        # dimension = dimension.replace("W", "")
        # dimension = dimension.replace("D", "")
        # dimension = dimension.replace("H", "")

        dimension = " ".join(dimension.split())
    except:
        dimension = dim

    return dimension


def standardize_dimensions(dimensions):
    converted = []
    try:
        for dim in dimensions:
            parsed = parser.parse(dim)
            unit = ""

            if "cm" in dim or "CM" in dim or "cms" in dim or "centimetres" in dim or "Cm" in dim:
                unit = "centimetre"
            else:
                if "feet" in dim or "Feet" in dim or "ft" in dim:
                    unit = "foot"
                else:
                    if "inch" in dim or "inches" in dim or "in" in dim or "Inches" in dim or "INCHES" in dim:
                        unit = "inch"

            size = []
            for p in parsed:
                p_unit = p.unit.name
                # print(p_unit)
                if p_unit in ["dimensionless"]:
                    p_unit = unit
                val = None
                if (p_unit in ["second of arc"] or p_unit in ["inch"]) and p.value:
                    val = p.value * 25.4
                if p_unit in ["centimetre"] and p.value:
                    val = p.value * 10
                if p_unit in ["foot"] and p.value:
                    val = p.value * 304.8
                if val:
                    val = round(val)
                    size.append(val)

            if len(size) > 0:
                converted.append(size)
    except:
        pass

    return converted


def get_model_id(string, brand_code):
    hashed = sha1(string.encode('utf-8')).hexdigest()
    pxm_id = f"CC_{brand_code}_{hashed[:8]}"

    return pxm_id


def get_category_links_file(brandCode):
    categoryLinksFile = f'data/PXM_{brandCode}_category_links.json'
    return categoryLinksFile


def get_product_links_file(brandCode):
    productLinksFile = f'data/PXM_{brandCode}_product_links.json'
    return productLinksFile


def get_products_output_file(brandCode):
    outputFile = f'output/{brandCode}/PXM_{brandCode}_products.xlsx'
    return outputFile


def get_images_folder(brandCode):
    imagesFolder = f'output/{brandCode}/images/'
    return imagesFolder


def create_dirs():
    pathlib.Path(constants.brandDataDir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(constants.categoryLinksFolder).mkdir(
        parents=True, exist_ok=True)
    pathlib.Path(constants.imagesFolder).mkdir(parents=True, exist_ok=True)

    return True


create_dirs()
# print(parser.parse("65 * 57.5 * 84.5 * 45 CM"))
