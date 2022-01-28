import datetime
from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
import os
import time
import shutil

dirpath = f'{os.getcwd()}/output'
if os.path.exists(dirpath):
    shutil.rmtree(dirpath)


class Robot:
    def __init__(self):
        self.browser = Selenium()
        self.http = HTTP()
        self.tables = Tables()
        self.pdf = PDF()
        self.table_list = []
        self.lib = Archive()

    def login(self):
        self.browser.open_available_browser("https://robotsparebinindustries.com/", maximized=True)
        self.browser.input_text('//input[@id="username"]', 'maria')
        self.browser.input_text('//input[@id="password"]', 'thoushallnotpass')
        self.browser.wait_and_click_button('//button[@type="submit"]')
        self.browser.wait_until_page_contains_element('//input[@id="firstname"]')
        self.browser.click_element_if_visible('//a[@class ="nav-link"]')
        time.sleep(3)

    def order_robot(self):
        table_data = self.tables.read_table_from_csv('orders.csv', columns=["Order number", "Head", "Body", "Legs", "Address"])
        for data in table_data:
            self.table_list.append(data)
        for row in self.table_list:
            try:
                while True:
                    try:
                        self.browser.click_button('OK')
                        break
                    except:
                        self.browser.wait_and_click_button('//button[@id="order-another"]')
                self.browser.select_from_list_by_value('head', f'{row["Head"]}')
                self.browser.select_radio_button('body', f'{row["Body"]}')
                self.browser.input_text('//input[@placeholder="Enter the part number for the legs"]', f'{row["Legs"]}')
                self.browser.input_text('//input[@id="address"]', f'{row["Address"]}')
                self.browser.wait_and_click_button('//button[@id="preview"]')
                self.browser.click_button('//button[@id="order"]')
                self.browser.wait_until_page_contains_element('//div[@id="robot-preview-image"]', timeout=datetime.timedelta(seconds=10))
                time.sleep(3)
                self.browser.screenshot('robot-preview-image', f'output/robot_{row["Order number"]}.png')
                receipt = self.browser.get_element_attribute('//div[@id="receipt"]', 'outerHTML')
                self.pdf.html_to_pdf(receipt, f'receipt_{row["Order number"]}.pdf')
                # self.browser.screenshot('//div[@id="receipt"]', f'output/receipt_{row["Order number"]}.png')
                # self.browser.screenshot('//div[@id="receipt"]', f'output/receipt_{row["Order number"]}.png')

                while True:
                    try:
                        self.browser.wait_and_click_button('//button[@id="order-another"]')
                        break
                    except:
                        self.browser.click_button('order')

            except:
                self.browser.click_button('order')

    def zip_file(self):
        self.lib.archive_folder_with_zip('./output', 'output.zip', recursive=True)


if __name__ == "__main__":
    obj = Robot()
    obj.login()
    obj.order_robot()
    obj.zip_file()
