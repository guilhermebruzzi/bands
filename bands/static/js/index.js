function main_index(){
    var viewportHeight = document.body.clientHeight;

    var descricao = document.querySelector('#descricao');
    var descricaoHeight = descricao.offsetHeight;

    var descricaoMarginBottom = 10; // Mudar, se no CSS mudou

    var header = document.querySelector('.container > header');
    var headerHeight = header.offsetHeight;
    var footer = document.querySelector('.container > footer');
    var footerHeight = footer.offsetHeight;


    var informacoesExistentes = document.querySelector('#informacoes-existentes');

    if(descricao && informacoesExistentes){ // Iguala as alturas (levando em conta a margem) se conseguiu pegá-los
        var newHeight = viewportHeight - headerHeight - footerHeight;
        if(viewportHeight > 830){
            informacoesExistentes.style.height = newHeight + "px"
            descricao.style.height = newHeight + "px";
            descricao.style.marginBottom = "0px";
        }
        else{
            informacoesExistentes.style.height = newHeight + descricaoMarginBottom + "px";
            descricao.style.height = newHeight + "px";
        }
    }
}

main_index();