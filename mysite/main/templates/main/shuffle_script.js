async function shuffleDivs() {
    // Wysyłanie asynchronicznego żądania AJAX do Django
    const response = await fetch('', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({}),
    });

    // Odczytanie odpowiedzi JSON
    const data = await response.json();
    console.log("Otrzymane dane:", data);

    // Zaktualizowanie divów z tasowanymi danymi
    const divs = document.querySelectorAll('.shuffle-div');
    data.shuffled_texts.forEach((text, index) => {
        divs[index].innerHTML = text;
    });

    // Tasowanie divów w miejscu
    const container = document.body;
    const divArray = Array.from(container.getElementsByClassName('shuffle-div'));

    for (let i = divArray.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        container.insertBefore(divArray[j], divArray[i]);
    }
}

// Funkcja do pobierania tokena CSRF z ciasteczka
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
