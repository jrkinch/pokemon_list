<h1>pokemon_list</h1>
Project for scrapping Pokémon names.<br>
Data Source: "https://m.bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"<br><br>

Project to extract pokemon list from website to an excel document.<br>
Wanted to do a webscrapping project using Selenium.<br>
&emsp;- Takes data from website and puts info into excel spreadsheet.<br>
&emsp;&emsp;- 'pokemon_output.xlsx' located in the 'pokemon_list/data' folder.<br>
&emsp;&emsp;- Has five columns; 'Pokedex', 'Image', 'Name', 'Type1', 'Type2':<br>
&emsp;&emsp;&emsp;- 'Pokedex', Pokemon's number in the Pokedex.<br>
&emsp;&emsp;&emsp;- 'Image', URL location of PNG on web.<br>
&emsp;&emsp;&emsp;- 'Name', Pokemon's Name.<br>
&emsp;&emsp;&emsp;- 'Type1', Element type of Pokemon.<br>
&emsp;&emsp;&emsp;- 'Type2', Second element type of Pokemon, blank if None.<br><br>

	
<h2>Installation:</h2>
1) Run <code>pip install -r requirements.txt</code> in the project folder or 'run_requirements.bat' from the 'scripts' folder.<br>
2) Install the webdrivers for OS at "https://www.selenium.dev/downloads/".<br>
&emsp;- Project has setup for Chrome and Firefox webdrivers but other could be added.<br><br>


<h2>Getting Started:</h2>
Steps:<br>
1) Put the 'pokemon_list' folder in any project.<br>
2) Use <code>from pokemon_list import pokemon_list</code> in project.<br>
3) Init the class then use the 'check_file_and_get_latest' function from module.<br>
- Example:<br>
<code>pl = pokemon_list.PokemonList()
pl.check_file_and_get_latest()
</code>

