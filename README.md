# libtransfer

Okay, so this is hell code.

Here is what you need to do, brave Padawan.

1. Download the HTML from the LibraryThing catalog (https://www.librarything.com/catalog). Probably you need to examine the HTML to find the node that contains all the images and copy it directly, since the Javascript changes this dynamically. This gets us the URLs for downloading the images we want.
2. Download the LibraryThing data in Excel format. Also download an Excel backup of the MyLibrary data, we can use this as a template.
3. Run the code to fetch all the images. Zip these up to manually move them to the phone.
4. Run the code to generate the Excel spreadsheet. This must be opened and re-saved in .xls format afterwards, because the app doesn't like the newer format.
5. Copy the images to /MyLibrary/Covers/Books/... and unzip. Copy the XLS file to /Documents/... and import it in the app. At this point the app will be like "where are the covers? you haven't backed them up, you fool!", but we know that the covers are there.
6. Make a new .db backup from the app, and bring this back to the laptop. Run the code on this new file to add the filepaths for the covers.
7. Transfer back to the /Documents/... on the phone, and import from the .db file this time. Ta-da!