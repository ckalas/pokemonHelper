package ck.pokemon.view;

import java.util.Map;

import org.apache.commons.lang3.text.WordUtils;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.text.Text;
import ck.pokemon.MainApp;
import ck.pokemon.model.PokemonData;


public class PokemonViewController {
    
	@FXML
    private TextField searchField;
    @FXML
    private Text fourHundredText;
    @FXML
    private Text twoHundredText;
    @FXML
    private Text oneHundredText;
    @FXML
    private Text fiftyText;
    @FXML
    private Text twentyFiveText;
    @FXML
    private Text zeroText;
    @FXML
    private Text infoText;
    @FXML
    private Text typeLabel;
    @FXML
    private Text infoLabel;
    @FXML
    private Text pokeType;

    // Reference to the main application.
    private MainApp mainApp;

    /**
     * The constructor.
     * The constructor is called before the initialize() method.
     */
    public PokemonViewController() {
    }

    /**
     * Initializes the controller class. This method is automatically called
     * after the fxml file has been loaded.
     */
    @FXML
    private void initialize() {
        // Clear pokemon details.
        showPokemonDetails(null);
        infoText.setText("");
        infoLabel.setText("");
        typeLabel.setText("");
        pokeType.setText("");


    }
    /**
     * Is called by the main application to give a reference back to itself.
     * 
     * @param mainApp
     */
    public void setMainApp(MainApp mainApp) {
        this.mainApp = mainApp;
    }
    
    /**
     * Fills all text fields to show details about the person.
     * If the specified person is null, all text fields are cleared.
     * 
     * @param person the person or null
     */
    private void showPokemonDetails(String type) {
        if (type != null) {
        	Map<String,String> data = PokemonData.getAttack(type);
            // Fill the labels with info from the person object.
            fourHundredText.setText((data.get("400") != null ? data.get("400"): ""));
            twoHundredText.setText((data.get("200") != null ? data.get("200"): ""));
            oneHundredText.setText((data.get("100") != null ? data.get("100"): ""));
            fiftyText.setText((data.get("50") != null ? data.get("50"): ""));
            twentyFiveText.setText((data.get("25") != null ? data.get("25"): ""));
            zeroText.setText((data.get("0") != null ? data.get("0"): ""));
        } 
        
        else {
        	fourHundredText.setText("");
            twoHundredText.setText("");
            oneHundredText.setText("");
            fiftyText.setText("");
            twentyFiveText.setText("");
            zeroText.setText("");
        }
    }

    /**
     * Called when the user clicks the edit button. Opens a dialog to edit
     * details for the selected person.
     */
    @FXML
    private void onEnter() {
    	PokemonData pokemonData = this.mainApp.getPokemonData();
    	String query = searchField.getText();
    	searchField.clear();
    	if (query != null) {
    		if (query.contains("/")) {
    			query = WordUtils.capitalize(query.split("/")[0]) + "/" + WordUtils.capitalize(query.split("/")[1]);
    		}
    		String cap = WordUtils.capitalize(query);
    		if (pokemonData.isPokemon(cap)) {
    			typeLabel.setText(cap);
    			pokeType.setText(pokemonData.getPokemon(cap,false));
    			showPokemonDetails(pokemonData.getPokemon(cap,true));
    		}
    		else if (pokemonData.isItemOrAbility(cap)) {
    			infoLabel.setText(cap);
    			infoText.setText(pokemonData.getItemsAndAbilities(cap));

    		}
    		else if (pokemonData.isType(cap)) {
    			typeLabel.setText(cap);
    			pokeType.setText("");
    			showPokemonDetails(pokemonData.getTypeData(cap));
    		}
    	}
    }
    
}