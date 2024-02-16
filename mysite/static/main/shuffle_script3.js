async function shuffleDivs() {
    // Wysyłanie asynchronicznego żądania AJAX do Django
    const response = await fetch('/shuffle_divs/', {
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
    const movieData=data.shuffled_texts


        // Pętla for do iteracji przez tytuły i ustawiania plakatów
    for (let i = 1; i < movieTitles.length+1; i++) {
        const imgId = `movie-${i}`;
        console.log(`ID obrazu dla ${imgId}`);
        document.getElementById(imgId).src = movieData[i-1][0];
    }

    // Zaktualizowanie divów z tasowanymi danymi
    const divs = document.querySelectorAll('.shuffle-div');
    divs.forEach((div, index) => {
        div.innerHTML = movieData[index][0];
    });



    // Tasowanie divów w miejscu
    const index=data.right;
    const container = document.body;
    const divArray = Array.from(container.getElementsByClassName('shuffle-div'));
    const divToUpdate = container.querySelector(`#shuffle-div-${index}`);
    document.getElementById('shuffle-div-1').onclick = null;
    document.getElementById('shuffle-div-2').onclick = null;
    document.getElementById('shuffle-div-3').onclick = null;
    document.getElementById('shuffle-div-4').onclick = null;
    document.getElementById('shuffle-div-5').onclick = null;
    document.getElementById(`shuffle-div-${index}`).onclick = () => shuffleDivs(index);







    // Funkcja do pobierania tokena CSRF z ciasteczka
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        }
}


