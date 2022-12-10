
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
import os
import base64
import urllib
import json

# Creating a webdriver instance
driver = webdriver.Chrome('./chromedriver.exe')

# Configs
query = ["dogs", "cat"] # Change me to the list you have.
no_of_images = 50 # Number of images you need to scrap from google images.

for query in query:

    # Open Google Images in the browser
    driver.get('https://images.google.com/')

    # Finding the search box
    box = driver.find_element(
        "xpath", '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')

    # Type the search query in the search box
    box.send_keys(query)

    # Pressing enter
    box.send_keys(Keys.ENTER)

    def scroll_to_bottom():

        last_height = driver.execute_script('\
        return document.body.scrollHeight')

        while True:
            driver.execute_script('\
            window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)

            new_height = driver.execute_script('\
            return document.body.scrollHeight')
            try:
                driver.find_element("css_selector", ".YstHxe input").click()
                time.sleep(2)

            except:
                pass

            # checking if we have reached the bottom of the page
            if new_height == last_height:
                break

            last_height = new_height

    # Calling the function
    scroll_to_bottom()

    # Loop to capture and save each image
    i = 1
    count = 1
    while True:
        if (count > no_of_images):
            print("Completed")
            break


        try:
            # XPath of each image
            img = driver.find_element("xpath",
                                      '//*[@id="islrg"]/div[1]/div[' + str(i) + ']/a[1]/div[1]/img').click()

            # Just to avoid unwanted errors
            time.sleep(1)
            i = i + 1
            tot = driver.find_element(
                "xpath", '//*[@id="Sva75c"]/div/div/div[2]/div[2]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a/img')
            src = tot.get_attribute('src')
            if src.startswith("https:"):
                urllib.request.urlretrieve( 
                    # save image
                    src, f'./assets/{query}{str(count)}.png')
                count = count + 1
                print(src)

                # Update meta
                # Open the JSON file
                with open("meta.json", "r") as file:
                    # Load the data from the file
                    data = json.load(file)

                # Append a new object to the data
                data.append({"alt": tot.get_attribute('alt'), "url": src, "filename": f'{query}{str(count - 1)}.png'})

                # Open the JSON file
                with open("meta.json", "w") as file:
                    # Write the updated data to the file
                    json.dump(data, file)

        except Exception as e:
            print(e)
            i = i + 1
            continue

# Driver closure.
driver.close()
