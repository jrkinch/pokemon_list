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
            This grabs the table with all of the pokemon text info but 'src' image data is not included in cell row.
        '''
        self.pokemon_list = []
        self.image_list = []
        tables = self.driver.find_elements(by=By.CLASS_NAME, value="roundy")
        for table in tables:
            rows  = table.find_elements(by=By.XPATH, value='.//tr')
            links = table.find_elements(by=By.TAG_NAME, value="img")
            for r in rows:
                cells = r.find_elements(by=By.XPATH, value='.//td')
                pokemon_row = []
                for cell in cells:
                    pokemon_row.append(cell.text)
                try:
                    if '#' in pokemon_row[0]:
                        self.pokemon_list.append(pokemon_row)
                except Exception as e:
                    print("Error: ", e)
        
            #Gets the image data for the pokemon list table data to merge later.
            variates = ['Alola', 'Galar', 'Hisui', 'Paldea']
            for l in links:
                if not any(variate in l.get_attribute("src") for variate in variates):
                    self.image_list.append(l.get_attribute("src"))

    def set_image_list_to_pokemon_data(self):
        '''
            Put images in image_list in pokemon_list data table.
        '''
        for image in self.image_list:
            for index, pokemon in enumerate(self.pokemon_list): 
                if pokemon[0][1:] in image: #uses the pokedex number excluding the '#' char.
                    pokemon[1] = image
                    
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
        
        #Put images in image_list in pokemon data table.
        self.set_image_list_to_pokemon_data()
        
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
                print("Data is up to date.")
            else:
                #get info again
                print("Data is different, need to update...")
                self.get_and_set_data()
        else:
            self.get_and_set_data()
        
        #close the webdriver.
        self.cleanup()
        
            
if __name__ == "__main__":
    #init class.
    pl = PokemonList()
    
    #checks for data file and gets latest data.
    pl.check_file_and_get_latest()
    