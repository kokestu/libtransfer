#################
# Read the HTML #
#################
from bs4 import BeautifulSoup

with open('data/book-covers.htm', 'r') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Find img elements -- these are ordered by ISBN
imgs = soup.find_all('img')
urls = [img.get("src") for img in imgs]  # gets the image urls

#######################
# Download the images #
#######################
import requests

for url in urls:
    # Download the image
    response = requests.get(url)
    image_data = response.content

    # Save the image to a file
    file_name = url.split('/')[-1]   # TODO: name the images appropriately
    with open(f"data/imgs/{file_name}", 'wb') as f:
        f.write(image_data)

############################
# Build the new Excel file #
############################
import pandas as pd

# Read the spreadsheet into a dataframe
df = pd.read_excel('data/librarything_kokestu.xlsx')

# Print the first few rows of the dataframe
print(df.head())

## TODO: DO SOME STUFF
final_df = df

final_df.to_excel('out/MyLibrary.xlsx', sheet_name='Books', index=False)