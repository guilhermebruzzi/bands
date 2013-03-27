var formPagSeguro = document.querySelector('form[target="pagseguro"]');


function getValorProduto(descricao){
    var valor = '2000';
    if(descricao.indexOf("cd") !== -1){
        valor = '1500';
    }
    return valor;
}

function getProdutoDataSelect(select){
    var quantidade = select.value;
    var descricao = select.options[select.selectedIndex].text + " Los Bife";

    return {
        'descricao': descricao,
        'valor': getValorProduto(descricao),
        'quantidade': quantidade
    }
}

function getProdutoDataInputs(input){
    var descricao = "";
    var inputClassList = input.classList;
    for(var classIndex in inputClassList){
        var className = inputClassList[classIndex];
        if(className != "quantidade-cada-camisa"){
            descricao = capitaliseFirstLetter(className.split("-").join(" "));
            break;
        }
    }

    var quantidade = 0;
    if(input.value){
        quantidade = parseInt(input.value, 10);
    }

    return {
        'descricao': descricao,
        'valor': getValorProduto(descricao),
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
    var selects = document.querySelectorAll('select.quantidade');
    var inputs = document.querySelectorAll('input.quantidade-cada-camisa');
    var datas = []
    for(var selectIndex = 0; selectIndex < selects.length; selectIndex++){
        var select = selects[selectIndex];
        datas.push(getProdutoDataSelect(select));
    }
    for(var inputIndex = 0; inputIndex < inputs.length; inputIndex++){
        var input = inputs[inputIndex];
        datas.push(getProdutoDataInputs(input));
    }

    formPagSeguro.innerHTML = '<input type="hidden" value="guibruzzi@gmail.com" name="email_cobranca"> <input type="hidden" name="item_frete_1" value="1000"> <input type="hidden" value="BRL" name="moeda"> <input type="hidden" value="CP" name="tipo">';

    var validou = false;
    var labelProdutos = "";
    var itemId = 1;
    for(var dataIndex = 0; dataIndex < datas.length; dataIndex++){
        var data = datas[dataIndex];
        validou = validou || (data.quantidade > 0)
        if(data.quantidade > 0){
            addItemId(itemId, data.descricao, data.valor, data.quantidade);
            labelProdutos += data.quantidade + " " + data.descricao + " ";
            itemId++;
        }
    }

    if(typeof _gaq != "undefined"){
        _gaq.push(['_trackEvent', 'Produtos', 'Banda Los Bife', labelProdutos]);
    }

    formPagSeguro.innerHTML += '<input type="image" alt="Pague com PagSeguro - é rápido, grátis e seguro!" name="submit" src="/static/img/pagseguro.png">';

    if(!validou){
        alert("Por favor, selecione 1 ou mais produtos para comprar");
        evt.preventDefault();
    }
    return validou;
}

function mainVendaProdutos(){
    formPagSeguro.addEventListener("submit", comprarPagSeguro, false);
}

if(formPagSeguro){
    mainVendaProdutos();
}
