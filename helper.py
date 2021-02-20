from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class Helper:
    def __init__(self, container):
        self.container = container
        self.log = self.container.log

    def fuse(self, element="content", by="id"):
        if by == "id":
            WebDriverWait(self.container.driver, 10).until(expected_conditions.presence_of_element_located((By.ID, element)))
        elif by == "class":
            WebDriverWait(self.container.driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, element)))
        else:
            raise ValueError("Wrong 'by' type.")
