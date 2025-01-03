# Python storage app for Tenaya Finland #

## This project was made for my familys company to manage our shoe storage. It handles comming and leaving shipments. ##

The project was made to help with storage management for bigger and bigger quantitys. I plan to update this project every time using it we find a bug or think that furteher functionality is needed. Right now the app can stores the shoes in a json file and displays it in a pandastable.

## Main window ##

the program generates a pandastable from the json file called storage.json and displays this information.

## Adding window ##

In the adding window the application handles comming shipments by scanning the barcode of the shoebox. You can test the program by taking the barecodes from the ___barcodes json file___. Before adding the shoes to the storage you can easily check how many shoes of each model and size have been added and the check if it maches with the shipping documents. After saving the shoes they are added to the main storage and written to the storage.json file.

## sending window ##

in this window you can also scan barcodes to an entry and the program will tell you how many of each kind you have scanned. By adding the ___asiakas.json___ file to the json file you can generate an invoice and select where the program will save your generated PDF invoice.

#### Before running ####

If you try to run the code you must add an _asiakas.json_ (asiakas = customer in finnish) file to the _json_ folder this is to protect our customers details.
___You sould use this format to add customer details___

```json
{
  "Kiipelykeskus 1":
  {
    "Toinen nimi":"KiKe",
    "Laskutustiedot":
    [
      "2319432",
      "PL 100",
      "80020 Kollector Scan"
    ],
    "Sposti": "932132@email.com"
  },
  "Kiipeilyvisio Oy":
  {
    "Tarkennus":
    [
      "Name1",
      "Name2",
      "Name3"
    ],
    "Laskutustiedot":
     [
       "Ostolaskut 32143G",
       "PL 50",
       "43218 EXAMLE SCAN"
     ],
     "Sposti": "179354L@scan.joujou.fi"
  },
  "Some name":
  {
    "Osoitetiedot":
    [
      "Peräkatu 72",
      "90213 Kuusamo",
      "info@somename.com",
      "0403213432"
    ],
    "Laskutustiedot":
    [
      "Ostolaskut 10663C",
      "PL 20",
      "53421 VISMA SCAN",
      "113213D@scan.scanscan.fi"
    ]
  }
}
```
You sould notice that for example elements named ___Tarkennus___ (adjustments) and ___Osoitetiedot___ are optional and are not mandatory so that the program runs.

