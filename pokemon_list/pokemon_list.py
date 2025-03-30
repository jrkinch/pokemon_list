'''
    Created by jrkinch
    Project for scrapping pokemon names.
    Data Source: "https://m.bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
    
'''
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
import re
import pandas as pd
import os
from datetime import date


class PokemonList():
    def __init__(self):
        self.listURL = "https://m.bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
        if __name__ == "__main__":
            self.fileName = ".//data//pokemon_output.xlsx"
        else:
            self.fileName = ".//pokemon_list//data//pokemon_output.xlsx"
            
    def setup(self, driver="chrome"):
        if driver == "chrome":
            self.driver = webdriver.Chrome()
        elif driver == "firefox":
            self.driver = webdriver.Firefox()
    
    def cleanup(self):
        self.driver.close()
            
    def check_pokemon_data_file(self):
        '''
            Checks to see if the file exists and how many rows it has.
        '''
        if os.path.exists(self.fileName):
            df = pd.read_excel(self.fileName)
            return True, len(df)
        else:
            return False, 0
      
    def get_site_list_amount(self): 
        '''
            Find and return the pokemon amount data from the website.
        '''
        pattern = r"^\d+$"
        textList = self.driver.find_elements(by=By.TAG_NAME, value="p")   
        for t in textList:
            if "Pokémon in total." in t.text:
                match = re.search(r'\d+', t.text)
                if match:
                    found = match.group(0)
                    return int(found)
        
    def get_site_pokemon_list_data(self):
        '''
            This grabs the table with all of the pokemon text info but 'src' image data is not included in cell row. Getting src image text through 'link' variable and attaching to the blank cell because it is the only cell the cell.text returns blank.
        '''
        self.pokemon_list = []
        self.image_list = []
        tables = self.driver.find_elements(by=By.CLASS_NAME, value="roundy")
        for table in tables:
            rows  = table.find_elements(by=By.XPATH, value='.//tr')        
            for index, r in enumerate(rows):
                cells = r.find_elements(by=By.XPATH, value='.//td')   
                pokemon_row = []
                for cell in cells:
                    link = r.find_element(by=By.TAG_NAME, value="img")
                    if cell.text == "": #cell.text doesn't get img src so this attachs src image text to only cell that doesn't have text
                        pokemon_row.append(link.get_attribute("src")) 
                    else:
                        pokemon_row.append(cell.text)
                try:
                    if '#' in pokemon_row[0]:
                        self.pokemon_list.append(pokemon_row)
                except Exception as e:
                    print("Error: ", e)

                    
    def save_to_file(self):
        '''
            Put data to file.
        '''
        df = pd.DataFrame(self.pokemon_list, columns=['Pokedex', 'Image', 'Name', 'Type1', 'Type2'])
        df.to_excel(self.fileName, index=False)
        
    def get_and_set_data(self): 
        '''
            Functions to call when needing a new/updated pokemon list.
        '''
        #Grab Pokemon info.
        self.get_site_pokemon_list_data()
        
        #Put data to file.
        self.save_to_file()
        
    def check_file_and_get_latest(self):
        '''
            This check if file exists, is up to date or gets data.
        '''
        #setup the webdriver.
        self.setup()
        
        #Open the pokemon website.
        self.driver.get(self.listURL)
        
        #Checks to see if data file exists and either updates or confirms data is up to date.
        fileExists, fileAmount = self.check_pokemon_data_file()
        if fileExists:
            #Checking data file and site for same amount number.
            siteAmount = self.get_site_list_amount()
            if fileAmount == siteAmount:
                print("Pokémon list data is up to date.")
            else:
                #get info again
                print("Pokémon list data is different, needs to update...")
                print("Updating Pokémon list data...")
                self.get_and_set_data()
                print("Pokémon list data completed.")
        else:
            print("Retrieving Pokémon list data...")
            self.get_and_set_data()
            print("Pokémon list data completed.")
        
        #close the webdriver.
        self.cleanup()
        
            
if __name__ == "__main__":
    #init class.
    pl = PokemonList()
    
    #checks for data file and gets latest data.
    pl.check_file_and_get_latest()
    