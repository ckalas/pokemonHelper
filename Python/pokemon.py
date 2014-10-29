from bs4 import BeautifulSoup
from clint.textui import colored
from operator import itemgetter
import sys, os, pokeData

""" Writes all the data to text files for other processing
	@params: 
		void
	@return
		void
"""
def writeData(pokes, items, abilities,typeData):
	with open('pokedex.txt', 'w+') as f:
		for p,t in pokes.items():
			f.write('{0}:{1}\n'.format(p,t))
	with open('items.txt', 'w+') as f:
		for p,t in items.items():
			f.write('{0}:{1}\n'.format(p,t[1]))
	with open('abilities.txt', 'w+') as f:
		for p,t in abilities.items():
			f.write('{0}:{1}\n'.format(p,t))
	with open('typeData.txt', 'w+') as f:
		typeStr = ''
		for p,t in typeData.items():
			f.write('{0}:{1}\n'.format(p,typeStr))


""" Load and parse the abilities into a dictionary 
	@params: 
		void
	@return
		dictionary of strings containing items
"""
def loadAbilities():
	# Load the raw HTML from external file into bs4
	soup = BeautifulSoup(pokeData.data[3])
	state = 'name'
	data = {}
	# Search the html for tags with correct info
	for tag in soup.findAll('tr'):
		if tag.text:
			info = tag.text.split('\n')
			data[info[1]] = info[3]
	return data

""" Load and parse the items into a dictionary 
	@params: 
		void
	@return
		dictionary of strings containing items
"""
def loadItems():
	# Load the raw HTML from external file into bs4
	soup = BeautifulSoup(pokeData.data[2])
	state = 'name'
	data = {}
	for tag in soup.findAll('tr'):
		if tag.text:
			info = tag.text.split('\n')
			data[info[3]] = (info[5], info[6])
	return data
		
""" Load and parse the pokedex into a dictionary 
	@params: 
		void
	@return
		dictionary of strings represting pokemon types
"""
def loadPokemon():
	# Load the raw HTML from external file into bs4
	soup = BeautifulSoup(pokeData.data[1])
	data = {}
	# Search the html for tags with correct info	
	for tag in soup.findAll('a'):
		# the title attribute will contain the pokemon name
		title = tag.get('title')
		if(title):
			name = title.split()[-1]
		# the class attribute will contain the type
		info = tag.get('class')
		# if len == 1 then it doesn't contain name, skip
		if len(info) == 1:
			continue
		else:
			# some checking to make sure duplicate types aren't created ie Water/Water
			# if a mega evolution exists, that type data will be stored
			# workaround done in main
			try:
				addType = info[1].split('-')[-1].title()
				types = data[name].split('/')
				if not addType in types:
					data[name] += '/'+addType
			except KeyError:
				data[name] = addType

	return data

""" Load and parse the data into a dictionary 
	@params: 
		void
	@return
		dictionary of list of tuples {type:[(attack type, effective dmg)]}
"""
def loadTypes():
	# Load the raw HTML from external file into bs4
	soup = BeautifulSoup(pokeData.data[0])
	data = {}
	lastType = None	
	# Search the html for tags with correct info							
	for tag in soup.findAll('td'):
		line = tag.get('title')
		# If the tag has no title ignore as line == None
		if not line:
			continue
		dmg = int(tag.get('class')[1].split('-')[2])
		# Split (now) valid data
		info = line.split()
		# If its a new type create new list
		if lastType != info[2]:
			data[info[2]] = []

		# Add the data entry as a tuple to the list representing the key
		data[info[2]].append((info[0],dmg))
		lastType = info[2]
	return data

""" Changes some of the keys where names are lost in import
	@params: 
		pokemon - dictionary with pokemon {name: type}
	@return
		void
"""
def replaceNames(pokemon):
	pokemon["Mr Mime"] = pokemon["Mime"]
	pokemon.pop("Mime", None)
	pokemon["Mime Jr."] = pokemon["Jr."]
	pokemon.pop("Jr.", None)
	pokemon["Ho-Oh"] = pokemon["Ho-oh"]
	pokemon.pop("Ho-oh", None)
	pokemon["Farfetch'D"] = pokemon["Farfetch'd"]
	pokemon.pop("Farfetch'd", None)
	pokemon["Nidoran"] = pokemon["Nidoran♀"]
	pokemon.pop("Nidoran♀", None)
	pokemon.pop("Nidoran♂", None)


""" Print the attack information 
	@params: 
		attack - tuple containing attack type and damage effect
		prevDmg - integer representing the dmamage value of last attack
	@return
		void
"""
def printInfo(attack, prevDmg):
	if (attack[1] != prevDmg):
		dmg = attack[1]/100 if (attack[1] > 0 or attack[1] < 1.0) else int(attack[1]/100)
		print(colored.red('['+ str(dmg) + 'x]'))
	if attack[1] == 0:
		print(colored.blue(attack[0])) # no effect
	elif attack[1] == 25:
		print(colored.magenta(attack[0])) # not effective
	elif attack[1] == 50:
		print(colored.yellow(attack[0])) # not effective
	elif attack[1] == 100:
		print(colored.green(attack[0])) # normal effect
	elif attack[1] == 200:
		print(colored.cyan(attack[0])) # super
	else:
		print(colored.white(attack[0])) # super effective

""" 				Note on type extraction from pokedex:
	
	Because of the way the pokedex data is read, any alternate forms or mega
	evolutions will just stack types onto the standarm form. For example, Mewtwo's type
	would read Psychic/Fighting.

	To handle this, there are 3 cases to consider.

	1) Pokemon that are single type that gain another type when mega evolving
		- a list of these is defined in pokedex.singles
		- if the mega ! symbol is not present, these pokemon types are taken to be
		  the first type only
		- when mega ! symbol is present, take both types

	2) Pokemon that are dual type and the second type changes
		- in this case, the first type listed is the same, but the second changes
		  (it would read like this: Water/Flying/Dark)
		- there Water/Flying is the standard form, and Water/Dark is the evolution
		- when mega ! symbol is present, take the type[0] and type[2] index
		- when mega ! symbol is not present, take type[:-1]
	3) Pokemon that are dual type and drop a type when mega evolving
		- reverse of first case
		- defined as doubles in pokedex

	Some pokemon are listed and their type changes based on item - these few are too
	ambiguous and no attempt is made to return their type.

"""
def mainLoop():
	data = loadTypes()
	pokemon = loadPokemon()
	itemsList = loadItems()
	abilities = loadAbilities()
	# Fix up some names that are parsed incorrectly
	replaceNames(pokemon)
	# Clear the terminal display
	os.system('clear')
	# Main loop
	while(1):
		mode = input(colored.cyan('(w)')+'eakness || '+colored.yellow('(s)') + 'earch: ')
		if mode == 'q':
			os.system('clear')
			sys.exit(0)
		while(1):
			# Prompt
			if mode == 'w':
				prompt = 'Enter opponents type or name (name!=mega): '
			elif mode == 's':
				prompt = 'Enter pokemon, type, item or ability: '

			else:
				break
			search = input(prompt).title()
			if not search:
				continue
			# Captial Q becaues it gets capitalized
			if search == 'Q':
				os.system('clear')
				break

			# Lookup ability/items here
			if mode == 's':
				if search in itemsList.keys():
					itemInfo = itemsList[search]
					print(colored.green(search) + colored.magenta(" [" + itemInfo[0] + "]") + " : " + itemInfo[1].strip('n'))
					continue
				elif search in abilities.keys():
					ability = abilities[search]
					print(colored.green(search) + ": " + ability)
					continue

			# Search pokedex for type info
			
			# Some pokemon types depend on item and are too ambiguously listed
			if search in pokeData.cant:
				print("This pokemon is too ambiguous. Enter the type directly")
				continue
			# Hacky workaround for mega/altenrate forms
			# Gets the type information of the pokemon and searches that
			if search[-1] == '!':
				# case 3) of explanation above
				if search[:-1] in pokeData.doubles:
					search = pokemon[search[:-1]].split('/')[0]
				else:
					types = pokemon[search[:-1]].split('/')
					# case 2) of explanation above
					if(len(types) > 2):
						search = types[0] + '/' + types[2]
					# Dual type unchanged in evolution
					else:
						search = '/'.join(types)
			if search in pokemon:
				# case 1) of explanation above
				if search in pokeData.singles:
					search = pokemon[search]
					search = search.split('/')[0]
				else:
					search = pokemon[search]
					split = search.split('/')
					if len(split) > 2:
						search = '/'.join(split[:-1])

			# Verify the type term exists
			try:
				# Sort the attack list based on ('type', attack) attack int
				data[search] = sorted(data[search], key = itemgetter(1), reverse = True)
			except KeyError:
				print('No such key: ' + search)
				continue
			# Weakness mode
			if mode == 'w':
				# Print the type information
				os.system('clear')
				print('Type: ' + colored.red(search) +' is weak to:')
				for key, value in data.items():
					if key == search:
						prevDmg = -1
						for attack in value:
							printInfo(attack, prevDmg)
							prevDmg = attack[1]
						break
			# Lookup mode
			elif mode == 's':
				os.system('clear')
				count = 0
				print('Type: ' + search)
				for key, value in pokemon.items():
					if value == search:
						count += 1
						print(colored.green(key))
				# Check other combination ie T1/T2 == T2/T1		
				if not count:
					split = search.split('/')
					split.reverse()
					recombined = '/'.join(split)
					for key, value in pokemon.items():
						if value == recombined:
							count += 1
							print(colored.green(key))
				print('Total of ' + colored.cyan(str(count)) + " " + search +' type found.')

if __name__ == "__main__":
	try:
		mainLoop()
	except KeyboardInterrupt:
		sys.exit(0)









