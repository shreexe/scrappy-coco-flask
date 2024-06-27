import os
import requests
from bs4 import BeautifulSoup
from category_data import get_category_links
import constants
import json


def get_product_links(productGridClass,productGridElt,getCategoriesURL, categoryLinkElt, categoryLinkClass):
   
     print("inside get_product_links")
     print(getCategoriesURL,"----SHOP URL--------")
     categoryLinks = get_category_links(getCategoriesURL, categoryLinkElt, categoryLinkClass)

     productLinks = []
     for categoryLink in categoryLinks:
            productsInCategory = get_products_by_category(categoryLink,productGridClass,productGridElt)
            productLinks = list(set(productLinks + productsInCategory))

            with open(constants.productLinksFile, 'w') as file:
                json.dump(productLinks, file)

   
     return productLinks


def get_products_by_category(categoryLink,productGridClass,productGridElt):

    productsInCategory = []
    category = get_category_name(categoryLink)
    print(f'Retrieving {category} product links...')
    for pageNo in range(1, constants.totalPages):
        categoryLinkPage = get_category_link_page(categoryLink, pageNo)
        print(categoryLinkPage)
        req = requests.get(categoryLinkPage, headers=constants.headers)
        status = req.status_code
        if status == 404:
            break
        else:
            response = req.text
            soup = BeautifulSoup(response, "html.parser")
            products = soup.find_all(
                productGridElt, {"class": productGridClass})
            if not len(products) > 0:
                break
            for product in products:
                link = get_product_link(product)
                # print(link)
                if link not in productsInCategory:
                    productsInCategory.append(link)

    with open(f'{constants.categoryLinksFolder}PXM_{constants.brandCode}_{category}.json', 'w') as file:
        json.dump(productsInCategory, file)

    return productsInCategory


def get_category_name(categoryLink):
    
        return categoryLink.split('/')[-2]


def get_category_link_page(categoryLink, pageNo):
   
    return (f'{categoryLink}page/{pageNo}')


def get_product_link(product):
    
    return product.find("a").get("href")



