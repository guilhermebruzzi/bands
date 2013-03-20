var formPagSeguro = document.querySelector('form[target="pagseguro"]');

function getProdutoData(select){
    var quantidade = select.value;
    var descricao = select.options[select.selectedIndex].text + " Los Bife";
    var itemId = 0;
    var produtoNodes = select.parentNode.childNodes;
    for(var nodeIndex in produtoNodes){
        var node = produtoNodes[nodeIndex];
        if(node.classList && node.classList.contains("item-id")){
            itemId = parseInt(node.innerHTML, 10);
        }
    }
    var valor = '2000';
    if(descricao.indexOf("cd") !== -1){
        valor = '1500';
    }
    return {
        'itemId': itemId,
        'descricao': descricao,
        'valor': valor,
        'quantidade': quantidade
    }
}

function addItemId(itemId, descricao, valor, quantidade){
    var inputHtmls = ['<input type="hidden" value="' + itemId + '" name="item_id_' + itemId + '">', '<input type="hidden" value="' + descricao + '" name="item_descr_' + itemId + '">', '<input type="hidden" value="' + quantidade + '" name="item_quant_' + itemId + '">', '<input type="hidden" value="' + valor + '" name="item_valor_' + itemId + '">'];
    for(var inputHtmlIndex in inputHtmls){
        var inputHtml = inputHtmls[inputHtmlIndex];
        formPagSeguro.innerHTML += " " + inputHtml + " ";
    }
}

function comprarPagSeguro(evt){
    var selects = document.querySelectorAll('.quantidade');
    var data1 = getProdutoData(selects[0]);
    var data2 = getProdutoData(selects[1]);
    formPagSeguro.innerHTML = '<input type="hidden" value="guibruzzi@gmail.com" name="email_cobranca"> <input type="hidden" value="BRL" name="moeda"> <input type="hidden" value="CP" name="tipo">';
    if(data1.quantidade == 0 && data2.quantidade == 0){
        alert("Por favor, selecione 1 ou mais produtos para comprar");
        evt.preventDefault();
        return false;
    }
    else if(data1.quantidade == 0){
        addItemId(1, data2.descricao, data2.valor, data2.quantidade);
    }
    else if(data2.quantidade == 0){
        addItemId(1, data1.descricao, data1.valor, data1.quantidade);
    }
    else{
        addItemId(1, data1.descricao, data1.valor, data1.quantidade);
        addItemId(2, data2.descricao, data2.valor, data2.quantidade);
    }
    formPagSeguro.innerHTML += '<input type="image" alt="Pague com PagSeguro - é rápido, grátis e seguro!" name="submit" src="/static/img/pagseguro.png">';
    return true;
}

function mainVendaProdutos(){
    formPagSeguro.addEventListener("submit", comprarPagSeguro, false);
}

if(formPagSeguro){
    mainVendaProdutos();
}
