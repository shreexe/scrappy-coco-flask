from flask import Flask, render_template, request
import pandas as pd
import requests
import constants

from get_shopify_data import process_products


app= Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/main',methods=['POST'])
def main():
    baseurl = request.form.get('url')    
    print("got url",baseurl)
    json_url=f"{baseurl}/products.json?limit=250&page=1"
    # print(json_url)
    # response=requests.get(json_url)
    # print(response.json())
    # if response.status_code==404:
    #     productLinks = get_product_links()
    #     products = []
  
    #     for i, productLink in enumerate(productLinks, start=1):
    #         productData = get_product_data(productLink)
    #         if len(productData) > 0:
    #             print(f'Processing {i} product {productData[0]["Name"]}...')
    #         products += productData
    # else:
    products=process_products(baseurl)
    print( products,"products")
    
    df = pd.DataFrame(products)
    df = df.sort_values(by=['Name'])
    df.to_excel(constants.outputFile, index=False)
    table_html = df.head(10).to_html(classes='data', header="true")
    return render_template('result.html', tables=[table_html])
    





    
    
