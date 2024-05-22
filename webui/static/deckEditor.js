function addSubdeck(prefix, defaultName = "Default Subdeck Name", defaultCsv = "path/to/default.csv", defaultHeaders = "Deutsch,Romaji,Hiragana,Katakana", index = null) {
    const subdeckCountElement = document.getElementById(`${prefix}_subdeck_count`);
    if (!subdeckCountElement) {
        console.error(`Element with ID ${prefix}_subdeck_count not found`);
        return;
    }
    const count = index !== null ? index : parseInt(subdeckCountElement.value);
    const newCount = index !== null ? count : count + 1;
    subdeckCountElement.value = newCount;

    const subdeckSection = document.getElementById(`${prefix}_subdeck_section`);
    if (!subdeckSection) {
        console.error(`Element with ID ${prefix}_subdeck_section not found`);
        return;
    }
    const newSubdeck = document.createElement('div');
    newSubdeck.id = `${prefix}_subdeck_${count}`;
    newSubdeck.innerHTML = `
        <h3>${prefix === 'main' ? 'Subdeck' : 'Nested Subdeck'} ${newCount}</h3>
        <label for="${prefix}_subdeck_name_${count}">Name:</label>
        <input type="text" id="${prefix}_subdeck_name_${count}" name="${prefix}_subdeck_name_${count}" value="${defaultName}" required><br>
        <label for="${prefix}_subdeck_csv_${count}">CSV File Path:</label>
        <input type="text" id="${prefix}_subdeck_csv_${count}" name="${prefix}_subdeck_csv_${count}" value="${defaultCsv}" required><br>
        <label for="${prefix}_csv_headers_${count}">CSV Headers (comma separated):</label>
        <input type="text" id="${prefix}_csv_headers_${count}" name="${prefix}_csv_headers_${count}" value="${defaultHeaders}" required><br>
        <input type="hidden" id="${prefix}_card_count_${count}" name="${prefix}_card_count_${count}" value="0">
        <button type="button" onclick="removeSubdeck('${prefix}_subdeck_${count}', '${prefix}_subdeck_count')">Remove Subdeck</button>
        <br><br>
        <input type="hidden" id="${prefix}_subdeck_${count}_subdeck_count" name="${prefix}_subdeck_${count}_subdeck_count" value="0">
        <div id="${prefix}_subdeck_${count}_subdeck_section"></div>
        <button type="button" onclick="addSubdeck('${prefix}_subdeck_${count}')">Add Nested Subdeck</button>
        <br><br>
    `;
    subdeckSection.appendChild(newSubdeck);
}

function removeSubdeck(subdeckId, countId) {
    const subdeckElement = document.getElementById(subdeckId);
    if (subdeckElement) {
        subdeckElement.parentNode.removeChild(subdeckElement);
        const countElement = document.getElementById(countId);
        const count = parseInt(countElement.value);
        countElement.value = count - 1;
    } else {
        console.error(`Element with ID ${subdeckId} not found`);
    }
}
