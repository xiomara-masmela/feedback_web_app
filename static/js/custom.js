//change color hero


function changeHeroBg(){
    const red = Math.floor(Math.random() * 255);
    const green = Math.floor(Math.random() * 255);
    const blue = Math.floor(Math.random() * 255);

    const randomRGBA = 'rgba(' + red + ',' + green + ', ' + blue + ',0.2)';
    const hero = document.querySelector('.hero');
    hero.style.backgroundColor = randomRGBA;
    console.log(randomRGBA)
}
const intervalBgColor = setInterval(changeHeroBg, 2000);

window.addEventListener('load', changeHeroBg);
