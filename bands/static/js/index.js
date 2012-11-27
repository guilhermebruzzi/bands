function main_index(){
    var descricao = document.querySelector('#descricao');
    var informacoesExistentes = document.querySelector('#informacoes-existentes');

    if(descricao && informacoesExistentes){
        informacoesExistentes.style.height = descricao.offsetHeight + "px";
    }
}

main_index();