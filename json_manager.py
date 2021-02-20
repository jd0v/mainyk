import json


class JsonManager:

    def __init__(self, container, filename):
        self.container = container
        self.log = self.container.log
        self.filename = filename
        try:
            with open(self.filename, 'r') as f:
                pass
        except FileNotFoundError:
            self.log.info(f"{self.filename} not found. Creating it.")
            with open(self.filename, 'w') as f:
                f.write('[]')

    def append_data_to_json_file(self, new_data, filename=None):
        if filename is None:
            filename = self.filename
        data = self.read_json_file(filename)
        data.append(new_data)
        self.write_to_json_file(data, filename)

    def write_to_json_file(self, data, filename=None):
        if filename is None:
            filename = self.filename
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def read_json_file(self, filename=None):
        if filename is None:
            filename = self.filename
        with open(filename) as f:
            data = json.load(f)
        return data


if __name__ == "__main__":
    import container
    jsonman = JsonManager(container.Container(json_filename="Mainyk_daiktai.json"), "Mainyk_daiktai.json")
