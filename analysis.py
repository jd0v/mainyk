import selenium
import selenium.common
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threading
import re
import json
import urllib.parse
import time
import copy
import os


class Analysis:

    def __init__(self, container):
        self.container = container
        self.log = self.container.log
        self.helper = self.container.helper
        self.json = self.container.json
        self.data = self.json.read_json_file()

    def to_lowercase(self, data):
        for item in data:
            for key in item:
                item[key] = item[key].lower()
        return data

    def no_lithuanian(self, data):
        for item in data:
            for key in item:
                item[key] = item[key].replace("ą", "a").replace("č", "c").replace("ę", "e").replace("ė", "e")\
                    .replace("į", "i").replace("š", "s").replace("ų", "u").replace("ū", "u").replace("ž", "z")
        return data

    def filter(self, data, key, val, compare, partial_value=False):
        # compare = [eq, neq, g, l]
        new_data = []
        for item in data:
            if compare == 'neq':
                if partial_value:
                    if val not in item[key]:
                        new_data.append(item)
                else:
                    if item[key] != val:
                        new_data.append(item)
            elif compare == 'eq':
                if partial_value:
                    if val in item[key]:
                        new_data.append(item)
                else:
                    if item[key] == val:
                        new_data.append(item)
            elif compare == 'g':
                if float(item[key]) > val:
                    new_data.append(item)
            elif compare == 'l':
                if float(item[key]) < val:
                    new_data.append(item)
            else:
                print("Wrong 'compare' value.")

        print(f"Total {len(new_data)} items left")
        return new_data

    def sort(self, data, by, min=None, max=None):
        if by == "kaina":
            new_data = sorted(data, key=lambda item: float(item["kaina"]))

        else:
            print("Wrong 'by'.")
            return None
        return new_data

    def print_data(self, data, key=None):
        no = 1
        for item in data:
            if key is None:
                print(no, item)
            else:
                print(no, item["url"])
                print(item[key])
            no += 1

    def find_each_other(self, data):
        data_pairs = []
        re_delimeters = r" ;|\/"
        for offer in data:
            offer_check = re.split(re_delimeters, offer["pavadinimas"])
            for seek in data:
                seek_check = re.split(re_delimeters, seek["noreciau"])
                for element in offer_check:
                    if element in seek_check:
                        data_pairs.extend([offer, seek])
        return data_pairs

    def filter_by_categories(self, data, categories, siulo_iesko, compare="eq"):
        result = []
        for category in categories:
            for key in CATEGORIES[category]:
                if siulo_iesko == "siulo":
                    tmp = self.filter(data, "pavadinimas", key, compare, True)
                    tmp.extend(self.filter(data, "aprasymas", key, compare, True))
                elif siulo_iesko == "iesko":
                    tmp = self.filter(data, "noreciau", key, compare, True)
                else:
                    raise ValueError

                for item in tmp:
                    if item not in result:
                        result.append(item)
        return result

    def filter_all_categories(self, data, siulo_iesko):
        for category in CATEGORIES:
            data_filtered = self.filter_by_categories(data, [category], siulo_iesko)
            filename = f"{directory}/Mainyk_{siulo_iesko}_{category}_{len(data_filtered)}.json"
            anal.json.write_to_json_file(data_filtered, filename)

    def show_uncategorised(self, data, siulo_iesko):
        data_uncategorised = []
        for item in data:
            valid_item = True
            for category in CATEGORIES:
                for keyword in CATEGORIES[category]:
                    if siulo_iesko == "siulo":
                        if keyword in item["pavadinimas"] or keyword in item["aprasymas"]:
                            valid_item = False
                            break
                    elif siulo_iesko == "iesko":
                        if keyword in item["noreciau"]:
                            valid_item = False
                            break
                if not valid_item:
                    break
            if valid_item:
                data_uncategorised.append(item)

        filename = f"{directory}/Mainyk_{siulo_iesko}_uncategorised_{len(data_uncategorised)}.json"
        self.json.write_to_json_file(data_uncategorised, filename)
        return data_uncategorised


CATEGORIES = {
    "adapteris": ["adapter"],
    "atmintukas": ["flash", "usb raktas", "usb laikmen", "flesiuk"],
    "ausines": ["ausines", "ausinuk"],
    "compaktai": ["cd", "dvd"],
    "cpu": ["proc", "cpu", "intel"],
    "dovana": ["dovan", "atiduo"],
    "floppy": ["floppy", "flopik", "disket"],
    "gpu": ["gpu", "vaizdo plok", "radeon", "geforce", "geforse", "nvidia"],
    "hdd": ["hdd", "hardas"],
    "kamera": ["web", "kamera", "cam"],
    "koloneles": ["kolon"],
    "kompiuteris": ["komp", "laptop", "loptop", "asus", "pavilion", "dell", "acer"],
    "konsole": ["xbox", "playstation", "ps2", "ps3", "nintend"],
    "klaviatura": ["klaviatur", "keyboard"],
    "laidai": ["laida", "kabel"],
    "marsrutizatorius": ["marsrutizator", "switch", "router", "rauter"],
    "modemas": ["modem"],
    "pakrovejas": ["pakrovejas", "maitblokis", "maitinim"],
    "pele": ["pele", "pelyte"],
    "plansete": ["planset", "ipad", "tab"],
    "ram": ["ram", "atmint", "ddr"],
    "skaneris": ["skener", "skaner"],
    "skaiciuotuvas": ["skaiciuotuv", "kalkuliator", "calculator"],
    "spausdintuvas": ["spausdintuv", "spauzdintuv", "printer", "spauszin"],
    "ssd": ["sdd"],
    "telefonas": ["telefon", "mobil", "nokia"],
    "vairas": ["vairas", "pedalai"],
    "vaizduoklis": ["vaizd", "monitori", "monik"],
}


if __name__ == "__main__":
    import container

    directory = "refactored"

    if not os.path.exists(directory):
        os.makedirs(directory)

    anal = Analysis(container.Container(json_filename="Mainyk_daiktai.json"))

    t0 = time.clock()
    refactored_data = anal.data
    refactored_data = anal.to_lowercase(refactored_data)
    refactored_data = anal.no_lithuanian(refactored_data)
    # print(time.clock() - t0)

    # anal.json.write_to_json_file(anal.find_each_other(refactored_data), "Mainyk_daiktai_pairs.json")
    # print(time.clock()-t0)
    # refactored_data = anal.sort(refactored_data, "kaina")
    # vilnius_data = anal.filter(refactored_data, "miestas", "vilnius", "eq")
    # refactored_data = anal.filter(refactored_data, "kaina", 2, 'g')
    # refactored_data = anal.filter(refactored_data, "kaina", 1000, 'l')
    # refactored_data = anal.filter(refactored_data, "noreciau", "usb", 'eq', True)
    # for key in ["siulyk", "bet ka", "bet ko", "siulom"]:
    #     refactored_data = anal.filter(refactored_data, "noreciau", key, 'neq', True)
    # refactored_data = anal.filter(refactored_data, "noreciau", "", 'neq')
    # refactored_data = anal.filter(refactored_data, "noreciau", "kolon", 'eq', True)
    # anal.print_data(refactored_data, "noreciau")
    # print(len(refactored_data))
    # refactored_data = anal.filter_by_categories(vilnius_data, ["compaktai"], False)
    # print(len(refactored_data))

    anal.filter_all_categories(refactored_data, "siulo")
    anal.filter_all_categories(refactored_data, "iesko")
    # anal.json.write_to_json_file(refactored_data, "Mainyk_daiktai_refactored.json")
    data_uncategorised = anal.show_uncategorised(refactored_data, "siulo")
    data_uncategorised = anal.show_uncategorised(refactored_data, "iesko")
