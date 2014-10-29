package ck.pokemon.model;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

// TODO: edit text file to make all type data good

public class PokemonData {
	
	private Map<String,String> pokedex;
	private Map<String, String[]> typeData;
	private Map<String,String> itemsAndAbilities;

	
	/** Constructor that reads data from files and stores it 
	 * @throws IOException */
	
	public PokemonData() throws IOException {
		// Instantiate fields 
		pokedex = new HashMap<String,String>();
		itemsAndAbilities = new HashMap<String,String>();
		typeData = new HashMap<String,String[]>();
		// Load data
		this.readPokedex();
		this.readItemsAndAbilities();
		this.readTypeData();

	}
	
	/** Reads the pokedex data from text file */
	private void readPokedex() throws IOException {
		
        BufferedReader in = new BufferedReader(new FileReader("/Applications/Pokemon.app/Contents/Java/resources/data/pokedex.txt"));
        String str;

        while((str = in.readLine()) != null){
        	if ( str.contains(":") ) {
        		pokedex.put(str.split(":")[0], str.split(":")[1]);
        	}
        }
        
        in.close();
	}
	
	/** Reads the items and abilities from text file */
	private void readItemsAndAbilities() throws IOException {
        BufferedReader in = new BufferedReader(new FileReader("/Applications/Pokemon.app/Contents/Java/resources/data/items.txt"));
        BufferedReader in2 = new BufferedReader(new FileReader("/Applications/Pokemon.app/Contents/Java/resources/data/abilities.txt"));
        String str;

        while((str = in.readLine()) != null){
            itemsAndAbilities.put(str.split(":")[0], str.split(":")[1]);
        }
        
        in.close();
        
        while((str = in2.readLine()) != null){
            itemsAndAbilities.put(str.split(":")[0], str.split(":")[1]);
        }
        
        in2.close();
	}
	
	/* Reads the type data from text file */
	private void readTypeData() throws IOException {
		
        BufferedReader in = new BufferedReader(new FileReader("/Applications/Pokemon.app/Contents/Java/resources/data/typeData.txt"));
        String str;
        
        while((str = in.readLine()) != null){
        	String temp = str.split(":")[1].replace("[", "").replace("]","").replace("'", "").replace("(", "").replace(")","");
        	String[] temp2 = temp.split(",");
        	
        	typeData.put(str.split(":")[0], temp2);
        	
        }
        
        in.close();
	}
	
	/** Gets the entry for a given item or ability */
	public String getItemsAndAbilities(String key) {
		String output = "";
		if ((output = this.itemsAndAbilities.get(key)) != null) {
			return output;
		}
		return "Not found";
	}
	
	/** Gets the entry for a given item or ability */
	public String getPokemon(String key, boolean mode) {
		String output = "";
		if ((output = pokedex.get(key)) != null) {
			return mode ? this.getTypeData(output) : output;
		}
		return "Not found";
	}
	
	public boolean isPokemon(String key) { 
		return this.pokedex.containsKey(key);
	}
	
	public boolean isItemOrAbility(String key) {
		return this.itemsAndAbilities.containsKey(key);
	}
	
	public boolean isType(String key) {
		return this.typeData.containsKey(key);
	}
	
	/** Gets the data for aiven type */
	public String getTypeData(String type) {
		String[] temp = this.typeData.get(type);
		String output = "";
		for(int i = 0; i<temp.length; i++) {
			if(i%2==0) {
				output += temp[i] + ",";
			}
			else {
				output += temp[i] + ":";
			}
			
		}
		return output;
	}
	
	/** Gets the types associated with a given damage in a list of type data */
	public static Map<String,String> getAttack(String data) {
		Map<String, String> attackDict = new HashMap<String, String>();
		String four = "";
		String two = "";
		String one = "";
		String half = "";
		String quarter = "";
		String none = "";
		String[] split = data.split(":");
		
		
		for (int i = 0; i < split.length; i++) {
			String[] temp = split[i].split(",");
			if (temp[1].trim().equals("400")) {
				four += temp[0].trim() + "\n";
			}
			if (temp[1].trim().equals("200")) {
				two += temp[0].trim() + "\n";
			}
			if (temp[1].trim().equals("100")) {
				one += temp[0].trim() + "\n";
			}
			if (temp[1].trim().equals("50")) {
				half += temp[0].trim() + "\n";
			}
			if (temp[1].trim().equals("25")) {
				quarter += temp[0].trim() + "\n";
			}
			if (temp[1].trim().equals("0")) {
				none += temp[0].trim() + "\n";
			}
		}
		if (four.length() > 0) {
			attackDict.put("400", four.substring(0, four.length()-1));
		}
		if (two.length() > 0) {
			attackDict.put("200", two.substring(0, two.length()-1));
		}
		if (one.length() > 0) {
			attackDict.put("100", one.substring(0, one.length()-1));
		}
		if (half.length() > 0) {
			attackDict.put("50", half.substring(0, half.length()-1));
		}
		if (quarter.length() > 0) {
			attackDict.put("25", quarter.substring(0, quarter.length()-1));
		}
		if (none.length() > 0) {
			attackDict.put("0", none.substring(0, none.length()-1));
		}
		return attackDict;
		
	}
		
}
