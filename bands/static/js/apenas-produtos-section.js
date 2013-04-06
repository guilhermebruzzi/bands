function mainApenasProdutosSection(){
    var produtosSection = document.querySelector('#produtos-section');
    if(produtosSection){
        var sectionContainer = document.querySelector('.container');
        var header = document.querySelector('.container>header');
        var footer = document.querySelector('.container>footer');
        sectionContainer.removeChild(header);
        sectionContainer.removeChild(footer);

        var produtosSection = document.querySelector('#produtos-section');
        var areaBanda = document.querySelector('#area-banda');
        produtosSection.removeChild(areaBanda);

        var areaProdutos = document.querySelector('#area-produtos');
        var tituloProdutos = document.querySelector('#titulo-produtos');
        areaProdutos.removeChild(tituloProdutos);

        var nomeBanda = document.querySelector('#nome-banda-produtos');
        nomeBanda.innerHTML += " - Produtos";
        if(produtosSection.classList.contains("produtos-section-dark")){
            areaProdutos.removeChild(nomeBanda);
            document.body.classList.add("produtos-section-dark");
        }
    }
}

mainApenasProdutosSection();
