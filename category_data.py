import requests
from bs4 import BeautifulSoup
import json
import constants
import os.path


def get_categories(link, categoryLinkElt, categoryLinkClass):
    print()
    categoryLinks = []
    response = requests.get(link, headers=constants.headers).text
    soup = BeautifulSoup(response, 'html.parser')
    categories = soup.find_all(categoryLinkElt, {
                               "class": categoryLinkClass})
    print(categories,"cate")

    for i, category in enumerate(categories):
        categoryLink = category.find("a").get("href")
        if categoryLink not in categoryLinks:

            categoryLinks.append(categoryLink)

    with open(constants.categoryLinksFile, 'w') as file:
        json.dump(categoryLinks, file)

    return categoryLinks





def get_category_links(getCategoriesURL, categoryLinkElt, categoryLinkClass):
    print("SHOP URL FROM GET_CATEGORY ELEMENTS--------",getCategoriesURL)
    if os.path.isfile(constants.categoryLinksFile):
        with open(constants.categoryLinksFile, 'r') as j:
            categoryLinks = json.load(j)
    else:

        categoryLinks = get_categories(
            getCategoriesURL, categoryLinkElt, categoryLinkClass)

    return categoryLinks



