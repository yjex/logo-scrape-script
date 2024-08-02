from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import env
import gspread
import pandas as pd

gc = gspread.service_account(env.filename)

shopsheet = gc.open(env.mainwb)

shoplinksheet = shopsheet.worksheet(env.link_mastersheet)

# creating dictionary of shop_ids, links
shoplink_df = pd.DataFrame(shoplinksheet.get_all_values())

id_linkdict = dict(zip(shoplink_df[0][1:], shoplink_df[1][1:]))

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-webgl")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(10)

exception_list = []

# loops through each shop_id, opens the link to the shop and gets the logo link attribute
for id in id_linkdict:
    cell = shoplinksheet.find(id)
    driver.get(id_linkdict[id])
    is_empty = shoplinksheet.cell(cell.row, 3)
    try:
        # updates sheet with logo url if logo link attribute is present 
        img_element = driver.find_element(By.CLASS_NAME, env.class_name)
        img_link = img_element.get_attribute("src")
        shoplinksheet.update_cell(cell.row, 3, img_link)
    except NoSuchElementException:
        # creates list of shop_ids where logo link attribute cannot be found
        exception_list.append(id)
        pass

# creates message telling user which shop_id's logo links cannot be found
final_message = env.final_msg
for exception in exception_list:
    final_message += exception+" "

shoplinksheet.update_cell(2, 4, final_message)

driver.quit()