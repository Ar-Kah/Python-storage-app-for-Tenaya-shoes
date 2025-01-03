# Python storage app for Tenaya Finland #

## This project was made for my familys company to manage our shoe storage. It handles comming and leaving shipments. ##

The project was made to help with storage management for bigger and bigger quantitys. I plan to update this project every time using it we find a bug or think that furteher functionality is needed. Right now the app can stores the shoes in a json file and displays it in a pandastable.

### Before running ###

If you try to run the code you must add an _asiakas.json_ (asiakas = customer in finnish) file to the _json_ folder this is to protect our customers details.
___You sould use this format to add customer details___

code()
  "Varuste.net":
  {
    "Toinen nimi":"Aalto Group Oy",
    "Laskutustiedot":
    [
      "17022863",
      "PL 100",
      "80020 Kollector Scan"
    ],
    "Sposti": "17022863@scan.netvisor.fi"
  }

#### Adding window ####

In the adding window the application handles comming shipments by scanning the barcode of the shoebox. Before adding the shoes to the storage you can easily check how many shoes of each model and size have been added and the check if it maches with the shipping documents. After saving the shoes they are added to the main storage and written to the storage.json file.

### sending window ###
