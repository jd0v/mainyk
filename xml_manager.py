from xml.etree import ElementTree


class XMLManager:

    def __init__(self, filepath):
        try:
            self.tree = ElementTree.parse(filepath)
        except FileNotFoundError:
            tmp = ElementTree.Element("root")
            tmp_tree = ElementTree.ElementTree(tmp)
            tmp_tree.write(filepath)
            # with open(filepath, 'w') as f:
            #     f.write(ElementTree.tostring(tmp_tree))
            self.tree = ElementTree.parse(filepath)
        self.root = self.tree.getroot()

    def get_element_value(self, tag):
        element = self.root.find(tag)
        return element.text

    def set_element_value(self, tag, value):
        element = self.root.find(tag).text = value


if __name__ == "__main__":
    xml = XMLManager("config.xml")
    a = xml.get_element_value("NeighbourOasesAlreadyScannedRadius")
    pass
