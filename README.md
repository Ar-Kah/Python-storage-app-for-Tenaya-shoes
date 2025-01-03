# Python storage app for Tenaya Finland #

## This project was made for my familys company to manage our shoe storage. It handles comming and leaving shipments. ##

The project was made to help with storage management for bigger and bigger quantitys. I plan to update this project every time using it we find a bug or think that furteher functionality is needed. Right now the app can stores the shoes in a json file and displays it in a pandastable.

### Before running ###

If you try to run the code you must add an _asiakas.json_ (asiakas = customer in finnish) file to the _json_ folder this is to protect our customers details.
___You sould use this format to add customer details___

Markup :  `
{
  "Kiipelykeskus 1":            // the first element is the name of the cstomer
  {
    "Toinen nimi":"KiKe",      // this is an optional element in the json file but it indicates the second name of the company if it has one
    "Laskutustiedot":          // this is the billing information of the customer
    [
      "2319432",
      "PL 100",
      "80020 Kollector Scan"
    ],
    "Sposti": "932132@email.com"    // email
  },
  "Kiipeilyvisio Oy":
  {
    "Tarkennus":              // this is also a optional array element
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
    "Osoitetiedot":        // this is also an optional element in the json file
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
`
Markup : ```json
         ```

#### Adding window ####

In the adding window the application handles comming shipments by scanning the barcode of the shoebox. Before adding the shoes to the storage you can easily check how many shoes of each model and size have been added and the check if it maches with the shipping documents. After saving the shoes they are added to the main storage and written to the storage.json file.

### sending window ###
