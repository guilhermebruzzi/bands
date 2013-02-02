function mostrarOcultarMenu() {
    var menuLista = document.querySelector('#user-menu');

    if(menuLista.classList.contains("invisivel")){
        menuLista.classList.remove("invisivel");
        menuLista.classList.add("visivel");
    }else{
        menuLista.classList.remove("visivel");
        menuLista.classList.add("invisivel");
    }
}

function dropDownMenu() {
    var menuButton = document.querySelector('#user-box-options');

    if(menuButton){
        menuButton.addEventListener("click", mostrarOcultarMenu, false);
    }
}

dropDownMenu();