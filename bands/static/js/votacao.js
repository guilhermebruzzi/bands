var httpRequest;
var featureList;
var votacaoInputDefault = "Nome da nova banda";

function makeRequestBand(method, operation, band, callback) {
    if (window.XMLHttpRequest) { // Mozilla, Safari, ...
        httpRequest = new XMLHttpRequest();
    } else if (window.ActiveXObject) { // IE
        try {
            httpRequest = new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch (e) {
            try {
                httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
            }
            catch (e) {}
        }
    }
    if (!httpRequest) {
        return false;
    }

    if(callback) {
        httpRequest.onreadystatechange = callback;
    }

    httpRequest.open(method, "/band/" + operation);

    if(method == 'POST') {
        httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        httpRequest.send('band=' + encodeURIComponent(band));
    } else {
        httpRequest.send();
    }
}

var votacaoInput = document.querySelector('#adicionar-item-votacao-text');
var minhasBandasList = document.querySelector('#minhas-bandas-list');
var bandasSugeridasList = document.querySelector('#bandas-sugeridas-list');


function removeElement(node) {
    node.parentNode.removeChild(node);
}

function createLiItemVotacaoHTML(bandSlug, bandName, checked){
    var checkedAttribute = checked ? 'checked="checked"' : '';
    return '<li><input type="checkbox" ' + checkedAttribute + ' class="item-votacao" value="' + bandSlug + '" /> <span class="sort-search minhas-bandas-name">' + bandName + '</span></li>';
}

function mudaNumeroMinhasBandas(diff){
    var numeroMinhasBandas = document.querySelector('#numero-minhas-bandas');
    var novoNumeroMinhasBandas = parseInt(numeroMinhasBandas.innerHTML, 10) + diff;
    numeroMinhasBandas.innerHTML = novoNumeroMinhasBandas.toString();
}

function decrementaNumeroMinhasBandas(){
    mudaNumeroMinhasBandas(-1);
}

function incrementaNumeroMinhasBandas(){
    mudaNumeroMinhasBandas(1);
}

function adicionaEmMinhasBandas(bandSlug, bandName){
    minhaBanda = minhasBandasList.querySelector("li input.item-votacao[value=" + bandSlug + "]");

    if(minhaBanda == null) {
        minhasBandasList.innerHTML += createLiItemVotacaoHTML(bandSlug, bandName, true);
        var itemCheckBoxes = document.querySelectorAll('.item-votacao');
        addListenerMarcacao(itemCheckBoxes);
        incrementaNumeroMinhasBandas();
        featureList = new List('minhas-bandas-itens', { valueNames: ['sort-search'] });
        featureList.sort("sort-search", {"asc": true});
    }
}

function showNewBand() {
    if (httpRequest.readyState === 4) {
        if (httpRequest.status === 200) {
            var response = httpRequest.responseText.split("\n");
            var bandName = response[0]
            var bandSlug = response[1]
            adicionaEmMinhasBandas(bandSlug, bandName);
            votacaoInput.value = "";
        } else {
            console.log('There was a problem with the request.');
        }
    }
}

function adicionarItem() {
    if(votacaoInput.value.trim() != "" && votacaoInput.value.trim() != votacaoInputDefault) {
        makeRequestBand('POST', "add/", votacaoInput.value, showNewBand);
    }
}

function enterPressed(e) {
    if (e.keyCode == 13) {
        setTimeout(adicionarItem, 50);
    }
}

function adicionaEmSugestaoDeBandas(bandSlug, bandName){
    var sugestao = document.querySelector("ul.list_bands_user_likes div#bandas-sugeridas li input.item-votacao[value=" + bandSlug + "]");
    if(!sugestao) {
        bandasSugeridasList.innerHTML += createLiItemVotacaoHTML(bandSlug, bandName, false);
        var itemCheckBoxes = document.querySelectorAll('.item-votacao');
        addListenerMarcacao(itemCheckBoxes);
        return true;
    }
    return false;
}

function bandasRelacionadas() {
    if (httpRequest.readyState === 4) {
        if (httpRequest.status === 200) {
            var response = httpRequest.responseText.split("\n");
            var counter = 0;
            for (var i = 0; i < response.length - 1 && counter < 3; i += 2) {
                var bandSlug = response[i];
                var bandName = response[i + 1];
                if(adicionaEmSugestaoDeBandas(bandSlug, bandName)) {
                    counter++;
                }
            }
            votacaoInput.value = "";
        } else {
            console.log('There was a problem with the request.');
        }
    }
}

function marcacaoItem() {
    if (this.checked) {
        this.setAttribute("checked", "checked");
        makeRequestBand('POST', "like/", this.value);
        makeRequestBand('GET', "related_bands/" + this.value + "/", this.value, bandasRelacionadas);
        if(bandasSugeridasList && this.parentNode.parentNode.id == bandasSugeridasList.id) {
            var bandSlug = this.value;
            var bandName = this.parentNode.textContent.trim();
            removeElement(this.parentNode);
            adicionaEmMinhasBandas(bandSlug, bandName);
        } else { // Remarquei uma banda que estava em minhas bandas
            incrementaNumeroMinhasBandas();
        }
    } else {
        this.removeAttribute("checked");
        makeRequestBand('POST', "unlike/", this.value);
        if(this.parentNode.parentNode.id == minhasBandasList.id){
            decrementaNumeroMinhasBandas();
        }
    }
}

function addListenerMarcacao(components) {
    for (var i = 0; i < components.length; ++i) {
        components[i].addEventListener("click", marcacaoItem, false);
    }
}

function colocaFraseDefault(){
    if(votacaoInput.value.trim() == ""){
        votacaoInput.value = votacaoInputDefault;
    }
}

function retiraFraseDefault(){
    if(votacaoInput.value == votacaoInputDefault){
        votacaoInput.value = "";
    }
}

function votacao() {
    var votacaoButton = document.querySelector('#adicionar-item-votacao-button');
    var itemCheckBoxes = document.querySelectorAll('.item-votacao');

    if(votacaoButton){
        colocaFraseDefault();
        votacaoButton.addEventListener("click", adicionarItem, false);
        votacaoInput.addEventListener("keypress", enterPressed, false);
        votacaoInput.addEventListener("focus", retiraFraseDefault, false);
        votacaoInput.addEventListener("blur", colocaFraseDefault, false);
        addListenerMarcacao(itemCheckBoxes);

        /* Plugin de procurar e ordenar */
        featureList = new List('minhas-bandas-itens', { valueNames: ['sort-search'] });
        featureList.sort("sort-search", {"asc": true});
    }
}

votacao();