import cianparser
import shutil
import json


class Cparser:

    def __init__(self):
        self.additional = {
            'max_price': 45000,
            'metro': "Московский",
            "is_by_homeowner": True,
            "sort_by": "creation_data_from_newer_to_older"
        }
        self.data = []
        self.filename = 'dump.json'
        self.memoryfile= 'dumpold.json'


    def get_new_entries(self):
        with open(self.filename, "r") as fp:
            dump = json.load(fp)
            with open(self.memoryfile, "w") as memfile:
                json.dump(dump, memfile)
            diff = []
            lasturl = ''
            for flat in self.data:
                if flat in dump:
                    break
                diff.append(flat)
        return diff



    def save_json(self):
        with open(self.filename, "w") as fp:
            json.dump(self.data, fp)


    def parse(self):
        return cianparser.parse(
            deal_type="rent_long",
            accommodation_type="flat",
            location="Москва",
            rooms=(1, 2, 3),
            additional_settings=self.additional,
            start_page=1,
            end_page=1,
        )


    def update(self):
        self.data = self.parse()
        diff = self.get_new_entries()
        self.save_json()
        return diff
