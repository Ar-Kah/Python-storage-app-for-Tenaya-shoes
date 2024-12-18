import json

def read_barcode_from_json(barcode):
    try:
        with open('Jsonfiles/barcodes.json', 'r') as file:
            data = json.load(file)
            for shoe in data:
                for size in data[shoe]:
                    if data[shoe][size] == barcode:
                        return True, shoe, size
        return False, "", ""
    except FileNotFoundError:
        print("File not found")
    except json.JSONDecodeError:
        print("There was an error with the json syntax")
    return False, "", ""

