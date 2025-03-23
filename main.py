'''
    Created by jrkinch
    Project for scrapping pokemon names.
    Data Source: "https://m.bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
    
'''
from pokemon_list import pokemon_list

    
if __name__ == "__main__":
    #init class.
    pl = pokemon_list.PokemonList()
    
    #checks for data file and gets latest data.
    pl.check_file_and_get_latest()