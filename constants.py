headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

totalPages = 50

dimension_array = [
    "Product Dimensions: ", "Product Dimensions:", "Product Dimension:", "Product Dimension", "Dimensions:", "Dimension:", "Dimension: ", "Dimension:", "Dimensions: ", "Dimensions:", "Dimensions(CMS)", "Dimensions", "Dimension", "DIMENSIONS-", "DIMENSIONS: ", "DIMENSIONS:", "Measurement in cm", "Measurement in inch", "Size : ", "Size :", "Size: ", "Size:", "Size (Small) : ", "Size (Small) :", "Size (Large) : ", "Size (Large) :", "Size", "Measurements in cm", "Measurements in inch", "Dimensions(cm)", "Dimensions(in)", "Dimensions (cm):"]

material_array = ["Material Content: ", "Material Content:", "Primary Material: ", "Primary Material:", "Primary Material", "Secondary Material:", "Material | ",
                  "Secondary Material", "Material : ",  "Material :", "Material: ",  "Material:", "Material", "MATERIAL: ", "MATERIAL:", "MATERIAL", "CONSTRUCTION-"]



brandCode='DUPE'
brandName='Narah'
brandDataDir = f'data/{brandCode}/'
brandOutputDir = f'output/{brandCode}/'
productDataFile = f'{brandDataDir}PXM_{brandCode}_products.json'
outputFile = f'{brandOutputDir}PXM_{brandCode}_products.xlsx'
imagesFolder = f'{brandOutputDir}images/'
categoryLinksFolder = f'{brandDataDir}categories/'