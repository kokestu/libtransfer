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
ids = [img.get("id").split("_")[-1] for img in imgs]  # gets the image urls

#######################
# Download the images #
#######################
import requests

id_to_file_path = {}
for i, url in enumerate(urls, start=1):
    # Download the image
    response = requests.get(url)
    image_data = response.content

    # Save the image to a file
    file_name = f"{i}.{url.split('.')[-1]}"
    id_to_file_path[ids[i-1]] = f"/MyLibrary/Images/Books/{file_name}"
    with open(f"data/imgs/{file_name}", 'wb') as f:
        f.write(image_data)


############################
# Build the new Excel file #
############################
import pandas as pd

# Read the spreadsheet into a dataframe
input_df = pd.read_excel('data/librarything_kokestu.xlsx').fillna('')
output_df = pd.read_excel('data/MyLibrary.xls')

## TODO: DO SOME STUFF
for index, old_row in input_df.iterrows():
    # Create a new dataframe with a single row
    new_row = pd.DataFrame({
        "Title": [old_row["Title"]],
        "Authors": [' '.join(old_row["Primary Author"].split(', ')[::-1]) or "None"],
        "Series": [None],
        "Categories": [', '.join(filter(None, [
            old_row["Tags"].title(),
            old_row["Languages"],
            "Jana's" if "Jana's" in old_row["Collections"] else "Mine"
        ]))],
        "Published date": [old_row["Date"]],
        "Publisher": [old_row["Publication"].split(' (')[0]],
        "Pages": [old_row["Page Count"]],
        "ISBN": [old_row["ISBN"][1:-1]],
        "Read": ["Yes" if "Read" in old_row["Collections"] else "No"],
        "Reading periods": [None],
        "Comments": ["unfixed"],
        "Summary": [None],
        "Cover path": [id_to_file_path.get(str(old_row["Book ID"]), None)],
    })

    # Append the new row to the original dataframe
    output_df = pd.concat([output_df, new_row], ignore_index=True)

# Write the final one to a file
output_df.to_excel('out/MyLibrary.xlsx', sheet_name='Books', index=False)

###############
# Examine SQL #
###############
import sqlite3

# Open a connection to the database file
conn = sqlite3.connect('data/mylibrary2.db')

# Create a cursor
cursor = conn.cursor()

df = pd.read_excel('out/MyLibrary.xlsx').fillna('')

for index, row in df.iterrows():
    ## UPDATE DB
    # Define the update query
    query = f"UPDATE BOOK SET COVER_PATH='{row['Cover path']}' WHERE ISBN='{row['ISBN']}'"
    # Execute the update query
    cursor.execute(query)

# Commit the changes
conn.commit()

# Close the connection
conn.close()