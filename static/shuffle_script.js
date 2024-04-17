function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
 function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        }

async function minuspoint(){
    var score = document.getElementById('score');
    var currentNumber = parseInt(score.innerText);
    var newNumber = currentNumber - 1;

       // Ustaw nową wartość liczby wewnątrz diva




    score.innerText = newNumber;
    var clickedElement = event.target;
    // Dodaj cień do elementu, który został kliknięty
    clickedElement.style.boxShadow = '1px 1px 27px 23px rgba(223, 27, 27, 1)';


    // Odczekaj 2 sekundy przed usunięciem cienia
    await sleep(1500);

    // Usuń cień po odczekaniu
    clickedElement.style.boxShadow = '';

}
async function pluspoint(){

     var clickedElement = event.target;
    // Dodaj cień do elementu, który został kliknięty
    clickedElement.style.boxShadow = '1px 1px 27px 23px rgba(68, 223, 27, 1)';


    // Odczekaj 2 sekundy przed usunięciem cienia
    await sleep(1000);

    // Usuń cień po odczekaniu
    clickedElement.style.boxShadow = '';
    shuffleDivs();
}



async function shuffleDivs() {



    const div1 = document.getElementById('div1');
    const div2 = document.getElementById('div2');
    const div3 = document.getElementById('div3');
    const div1style= window.getComputedStyle(div1);
    if (div1style.display === 'none') {
        div1.style.display = 'none';
        div3.style.display = 'block';
    }
    const container = document.body;

    const scoreDiv2 = document.getElementById('score');

    const score = scoreDiv2.textContent || scoreDiv2.innerText;
    console.log(score);
    console.log('adad');
    const requestData = {
        'scoreText': score,
    };
    console.log(requestData);




    const response = await fetch('/shuffle_divs/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(requestData),
    });


    const data = await response.json();
    console.log("Otrzymane dane:", data);
    const index=data.right;
    const movieData=data.shuffled_texts;
    const textToScore=data.score;

    for (let i = 1; i < 6; i++) {
        if(i===parseInt(index)){
            console.log(document.getElementById(`movie-${i}`))
            document.getElementById(`movie-${i}`).onclick = (event) => pluspoint(event);
        } else{
            console.log('zle:')
            console.log(document.getElementById(`movie-${i}`))
           document.getElementById(`movie-${i}`).onclick = (event) => minuspoint(event);
        }

    }











    console.log(textToScore)
    const scoreDiv=document.getElementById('score');
    scoreDiv.innerText=textToScore;
    for (let i = 1; i < movieData.length+1; i++) {
        const imgId = `movie-${i}`;
        console.log(`ID obrazu dla ${imgId}`);
        document.getElementById(imgId).src = movieData[i-1][1];
    }

    const divs = document.querySelectorAll('.overlay-text');
    divs.forEach((div, index) => {
        div.innerHTML = movieData[index][0];
    });

    const text=document.querySelectorAll('.main-text');
    text.forEach((txxt, index) => {
        txxt.innerHTML = data.text;
    });


    // Tasowanie divów w miejscu








    // Funkcja do pobierania tokena CSRF z ciasteczka

    if (div1style.display === 'none') {
        div3.style.display = 'none';
        div1.style.display = 'block';
        await sleep(10);

    }
}

async function toggleDivs() {
    const div1 = document.getElementById('div1');
    const div2 = document.getElementById('div2');
    const div3 = document.getElementById('div3');
    var score = document.getElementById('score');
    var score2 = document.getElementById('score2');
    const div1style= window.getComputedStyle(div1);

    console.log('dziala');
    console.log(div1style.display);
    if (div1style.display === 'none') {

        div1.style.display = 'block';
        div2.style.display = 'none';

        shuffleDivs();
        score2.style.display = 'block';
        score.style.display = 'block';

        console.log('odpala sie');

    }


}

