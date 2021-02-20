import os
import time
import selenium
import selenium.common
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threading
import re
import json
import urllib.parse


class MainykThread(threading.Thread):

    def __init__(self, container):
        threading.Thread.__init__(self)
        self.container = container
        self.log = self.container.log
        self.helper = self.container.helper
        self.json = self.container.json
        # self.xml = self.container.xml
        # self.nickname = nickname
        # self.password = password
    #
    # def preferences_maker(self):
    #     fp = webdriver.ChromeOptions()
    #     fp.set_preference("browser.cache.memory.capacity", 4000)
    #     fp.set_preference("browser.sessionhistory.max_entries", 2)
    #     fp.set_preference("browser.sessionhistory.max_total_viewers", 0)
    #     return fp

    def logscreen(self):

        # go to the self.log in page
        while True:
            try:
                self.log.info("Connecting to " + self.container.website)
                # self.container.driver.get(self.website)
                self.container.driver.get(self.container.website)
                break
            except selenium.common.exceptions.WebDriverException as ex:
                if 'Reached error page' not in ex.__str__():
                    self.log.error('Unhandled exception')
                    self.log.exception(ex)
                    break
                self.log.warning("Cant access the website. Retrying...")

    def run(self):

        # self.container.driver = webdriver.Firefox()
        self.container.driver = webdriver.Chrome("/home/aidas/PycharmProjects/mainyk/chromedriver")

        self.cycle_through_to_final_page("http://www.mainyk.lt/daiktai/zaidimu-kompiuteriai")
        self.cycle_through_to_final_page("http://www.mainyk.lt/daiktai/kiti-irenginiai")

        self.container.driver.close()

    def cycle_through_to_final_page(self, start_url):
        start_page = start_url.split("/")
        try:
            page = int(start_page[-1])
        except:
            page = 1
            start_url += r"/1"
        url = start_url
        valid_page = self.read_all_items_on_page(url)
        while valid_page:
            page += 1
            print(f"Current page: {page}")
            url = urllib.parse.urljoin(url, str(page))
            valid_page = self.read_all_items_on_page(url)

    # def valid_page(self):
    #
    #     websites_objs = self.container.driver.find_elements_by_xpath(
    #         "//div[@class='list-items']/div[@class='list-grid-item']/a")
    #     if not websites_objs:
    #         return False
    #
    #     return True

    def read_all_items_on_page(self, url):

        self.container.driver.get(url)

        try:
            self.helper.fuse()
        except:
            return False

        urls = []
        websites_objs = self.container.driver.find_elements_by_xpath(
            "//div[@class='list-items']/div[@class='list-grid-item']/a")
        for obj in websites_objs:
            urls.append(obj.get_attribute("href"))

        if not urls:
            return False

        for idx, url in enumerate(urls, 1):
            print(f"{idx}/{len(urls)}")
            info = self.read_page(url)
            self.json.append_data_to_json_file(info)

        return True

    def read_page(self, url):
        self.container.driver.get(url)

        try:
            self.helper.fuse()
        except:
            # TODO patikrinti ar yra toks puslapis
            raise

        pavadinimas = self.container.driver.find_element_by_xpath("//div[@id='content']/h1").text

        miestas = ""
        domina = ""
        noreciau = ""
        kaina = ""
        tmp = self.container.driver.find_elements_by_xpath("//div[@class='item-view-right']")
        for item in tmp:
            if item.find_element_by_xpath("strong").text == "MIESTAS":
                splited_tmp = item.text.split(" ")
                if len(splited_tmp) > 1:
                    miestas = " ".join(splited_tmp[1:])
            elif item.find_element_by_xpath("strong").text == "DOMINA":
                splited_tmp = item.text.split(" ")
                if len(splited_tmp) > 1:
                    domina = " ".join(splited_tmp[1:])
            elif item.find_element_by_xpath("strong").text == "NORĖČIAU MAINAIS":
                noreciau, kaina = [element.text for element in item.find_elements_by_xpath("p")]
                if "EUR" in kaina:
                    kaina = kaina.split("EUR")[0].replace(" ", "")

        aprasymas = ""
        tmp = self.container.driver.find_elements_by_xpath("//div[@class='item-view-left']")
        for item in tmp:
            if item.find_element_by_xpath("strong").text == "APRAŠYMAS":
                splited_tmp = item.text.split(" ")
                if len(splited_tmp) > 1:
                    aprasymas = " ".join(splited_tmp[1:])

        info = {
            "url": url,
            "pavadinimas": pavadinimas,
            "miestas": miestas,
            "domina": domina,
            "noreciau": noreciau,
            "kaina": kaina,
            "aprasymas": aprasymas,
        }

        return info


if __name__ == "__main__":
    import container

    t = MainykThread(container.Container(json_filename="Mainyk_daiktai.json"))
    t.start()
