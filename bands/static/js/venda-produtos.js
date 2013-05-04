var formPagSeguro = document.querySelector('form[target="pagseguro"]');
formPagSeguroHTML = ''
var frete_total = 10.0;

function isCd(descricao){
    return (descricao.indexOf("cd") !== -1);
}

function isCamisaNaoLosBife(descricao){
    return (descricao.toLowerCase().indexOf("camisa") !== -1 && descricao.toLowerCase().indexOf("los bife") === -1);
}

function getValorProdutoInput(input){
    var infoProdutoFilhos = input.parentNode.parentNode.parentNode.childNodes;
    var preco = "2000";
    for(var index = 0; index < infoProdutoFilhos.length; index++){
        var info = infoProdutoFilhos[index];
        if(info.classList && info.classList.contains("valor-produto")){
            preco = info.innerHTML;
            preco = preco.replace("R$ ", "");
            preco = preco.replace(",", "");
        }
    }
    return preco;
}

function getValorProduto(descricao){
    var valor = "2000";
    if(isCd(descricao)){
        valor = "1500";
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
        'valor': getValorProdutoInput(input),
        'quantidade': quantidade
    }
}

function addItemId(itemId, descricao, valor, quantidade){
    var inputHtmls = ['<input type="hidden" value="' + itemId + '" name="item_id_' + itemId + '">', '<input type="hidden" value="' + descricao + '" name="item_descr_' + itemId + '">', '<input type="hidden" value="' + quantidade + '" name="item_quant_' + itemId + '">', '<input type="hidden" value="' + valor + '" name="item_valor_' + itemId + '">'];
    for(var inputHtmlIndex in inputHtmls){
        var inputHtml = inputHtmls[inputHtmlIndex];
        formPagSeguroHTML += " " + inputHtml + " ";
    }
}

function comprarPagSeguro(evt){
    var selects = $('select.quantidade', $(this).parent().parent());
    var inputs = $('input.quantidade-cada-camisa', $(this).parent().parent());
    var datas = [];

    selects.each(function(index, select){
        datas.push(getProdutoDataSelect(select));
    });

    inputs.each(function(index, input){
        var camisa_data = getProdutoDataInputs(input);
        datas.push(camisa_data);
    });

    var emailCobranca = $('input[name="email_cobranca"]').val();
    formPagSeguroHTML = '<input type="hidden" value="' + emailCobranca + '" name="email_cobranca"> <input type="hidden" value="BRL" name="moeda"> <input type="hidden" value="CP" name="tipo">';

    var validou = false;
    var labelProdutos = "";
    var itemId = 1;
    var mensagemCamisa = null;
    var quantidadePrimeiroItem = 0;

    for(var dataIndex = 0; dataIndex < datas.length; dataIndex++){
        var data = datas[dataIndex];
        validou = validou || (data.quantidade > 0)
        if(data.quantidade > 0){
            if(isCd(data.descricao)){
                addItemId(itemId, data.descricao, data.valor, data.quantidade);
                if(itemId == 1){
                    quantidadePrimeiroItem = data.quantidade;
                }
                itemId++;
            }
            else{
                mensagemCamisa = "Por enquanto não temos mais camisas em estoque, curta a página facebook.com/bandsbr ou faça login aqui no site e lhe avisaremos quando poderão comprar.";
            }
            labelProdutos += data.quantidade + " " + data.descricao + " ";
        }
    }

    if(typeof _gaq != "undefined"){
        _gaq.push(['_trackEvent', 'Produtos', "Bandas em " + window.location.href, labelProdutos]);
    }


    var frete_por_item = frete_total / ((quantidadePrimeiroItem == 0) ? 1.0 : quantidadePrimeiroItem);
    formPagSeguroHTML += '<input type="hidden" name="item_frete_1" value="' + frete_por_item.toFixed(2) + '">';
    formPagSeguroHTML += '<input type="image" alt="Pague com PagSeguro - é rápido, grátis e seguro!" name="submit" src="/static/img/pagseguro.png">';

    $(this).html(formPagSeguroHTML);

    if(!validou){
        alert("Por favor, selecione 1 ou mais produtos para comprar");
        evt.preventDefault();
    }
    else{
        if(mensagemCamisa){
            alert(mensagemCamisa);
        }
        if(itemId == 1){ // Nenhum cd
            evt.preventDefault();
        }
    }
    return validou;
}

function mainVendaProdutos(){
    $(document).on('submit', 'form[target="pagseguro"]', comprarPagSeguro);
}

if(formPagSeguro){
    mainVendaProdutos();
}
