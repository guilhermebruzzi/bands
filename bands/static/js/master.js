function mostrarOcultarMenu() {
    var menuLista = document.querySelector('#user-menu');
    var menuSeta = document.querySelector('#user-box-seta');

    if(menuLista.classList.contains("invisivel")){
        menuLista.classList.remove("invisivel");
        menuLista.classList.add("visivel");

        menuSeta.classList.add("user-box-seta-ao-contrario");

    }else{
        menuLista.classList.remove("visivel");
        menuLista.classList.add("invisivel");

        menuSeta.classList.remove("user-box-seta-ao-contrario");
    }
}

function dropDownMenu() {
    var menuButton = document.querySelector('#user-box-options');

    if(menuButton){
        menuButton.addEventListener("click", mostrarOcultarMenu, false);
    }
}

dropDownMenu();