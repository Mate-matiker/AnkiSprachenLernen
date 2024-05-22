function selectDeck(deckName) {
    // Fetch and display deck data for editing
    fetch(`/decks/${deckName}`)
        .then(response => response.json())
        .then(data => {
            displayDeckEditor(data);
        })
        .catch(error => console.error('Error fetching deck data:', error));
}

function displayDeckEditor(data) {
    const editor = document.getElementById('deck_editor');
    editor.innerHTML = `
        <h2>Edit Deck: ${data.decks[0].name}</h2>
        <form action="/generate_config" method="post">
            <label for="main_deck_name">Main Deck Name:</label>
            <input type="text" id="main_deck_name" name="main_deck_name" value="${data.decks[0].name}" required><br>

            <label for="audio_path">Audio Path:</label>
            <input type="text" id="audio_path" name="audio_path" value="${data.audio_path}" required><br>

            <label for="audio_extension">Audio Extension:</label>
            <input type="text" id="audio_extension" name="audio_extension" value="${data.audio_extension}" required><br>

            <label for="image_path">Image Path:</label>
            <input type="text" id="image_path" name="image_path" value="${data.image_path}" required><br>

            <label for="image_extension">Image Extension:</label>
            <input type="text" id="image_extension" name="image_extension" value="${data.image_extension}" required><br>

            <input type="hidden" id="main_subdeck_count" name="subdeck_count" value="${data.decks[0].subdecks.length}">
            <div id="main_subdeck_section"></div>
            <button type="button" onclick="addSubdeck('main')">Add Subdeck</button>

            <br><br>
            <button type="submit">Save Deck</button>
        </form>
    `;
    // Populate subdecks
    data.decks[0].subdecks.forEach((subdeck, index) => {
        addSubdeck('main', subdeck.name, subdeck.csv_file, subdeck.csv_headers.join(','), index);
    });
}
