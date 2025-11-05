const title = document.getElementById('inputTitle')
const mainTitle = document.getElementById('mainTitle')

const handlerInputOnChange = function(e) {
    mainTitle.innerText = !title.value ? "Meu Novo evento" : e.target.value;
}

title.addEventListener('input', handlerInputOnChange);
title.addEventListener('change', handlerInputOnChange);