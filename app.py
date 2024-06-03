
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


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/main', methods=['POST'])
def main():
    baseurl = request.form.get('url')
    print("got url", baseurl)
    json_url = f"{baseurl}/products.json?limit=250&page=1"
    response = requests.get(json_url)

    if response.status_code == 200:

        products = process_products(baseurl)

    else:

        return render_template_string(invalid_url_template)

    df = pd.DataFrame(products)
    df = df.sort_values(by=['Name'])
    df.head(5).to_excel(constants.outputFile, index=False)
    table_html = df.head(5).to_html(classes='data', header="true")
    return render_template('result.html', tables=[table_html])


@app.route('/download')
def download_file():
    output_path = constants.outputFile
    return send_file(output_path, as_attachment=True, download_name='products.xlsx')


if __name__ == '__main__':
    app.run(debug=True)
