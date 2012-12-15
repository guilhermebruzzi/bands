function adicionarItem() {
    var votacaoText = document.querySelector('#adicionar-item-votacao-text');
    alert(votacaoText.value);
}

function votacao(){
    var votacaoButton = document.querySelector('#adicionar-item-votacao-button');

    votacaoButton.addEventListener("click", adicionarItem, false);
}

votacao();