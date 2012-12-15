function main_index(){
    var viewportHeight = document.body.clientHeight;

    var descricao = document.querySelector('#descricao');
    var informacoesExistentes = document.querySelector('#informacoes-existentes');

    if(descricao && informacoesExistentes){ // Iguala as alturas (levando em conta a margem) se conseguiu pegá-los (página principal)

        var header = document.querySelector('.container > header');
        var headerHeight = header.offsetHeight;
        var footer = document.querySelector('.container > footer');
        var footerHeight = footer.offsetHeight;

        var margin = 10; // Dou um espaço pro footer

        var newHeight = viewportHeight - headerHeight - footerHeight;

        informacoesExistentes.style.height = newHeight + margin + "px";
        descricao.style.height = newHeight + margin + "px";
    }
}

main_index();