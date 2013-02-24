var erroProcurarBandas = document.querySelector('#erro-procurar-bandas');

function makeRequestServer(method, url, callback, params){
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

    httpRequest.open(method, url);

    if(method == 'POST') {
        httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        httpRequest.send(params);
    } else {
        httpRequest.send(params);
    }
}
function makeRequestNewsletter(option, tipo, callback) {
    var params = 'tipo=' + encodeURIComponent(tipo);
    makeRequestServer("POST", "/newsletter/" + option, callback, params);
}
function makeRequestShowFromBand(bandName) {
    if(typeof(_gaq) != "undefined"){
        _gaq.push(['_trackEvent', 'Show', 'Busca Show', 'Procurar Show na Home: ' + bandName]);
    }
    if(erroProcurarBandas.classList.contains("visivel")){
        erroProcurarBandas.classList.remove("visivel");
        erroProcurarBandas.classList.add("invisivel");
    }
    erroProcurarBandas.innerHTML = 'Não encontramos nenhum show de ' + bandName + ' num futuro próximo';
    makeRequestServer("GET", "/show_from_band/" + bandName, adicionarShowDaBanda);
}

var procurarBandasText = document.querySelector('#opcoes-procurar-bandas-text');
var procurarBandasButton = document.querySelector('#opcoes-procurar-bandas-button');

function opcaoNewsletter(){
    var option = (this.innerHTML == "Sim") ? "sim" : "nao";
    var tipo = "Shows";

    makeRequestNewsletter(option, tipo);
    this.parentNode.parentNode.parentNode.style.display = "none";
}

function adicionarShowDaBanda(){
    if (httpRequest.readyState === 4) {
        if (httpRequest.status === 200) {
            var htmlShow = httpRequest.responseText;
            var minhasBandasShows = document.querySelector('#minhas-bandas-shows-lista');
            if(htmlShow){
                minhasBandasShows.innerHTML = htmlShow + minhasBandasShows.innerHTML;
            }
            else{
                if(erroProcurarBandas.classList.contains("invisivel")){
                    erroProcurarBandas.classList.remove("invisivel");
                    erroProcurarBandas.classList.add("visivel");
                }
            }

        } else {
            console.log('There was a problem with the request.');
        }
    }
}

function procurarShowDaBanda(){
    var bandName = procurarBandasText.value;
    procurarBandasText.value = "";
    makeRequestShowFromBand(bandName);
}

function enterPressedProcuraBanda(e) {
    if (e.keyCode == 13) {
        setTimeout(procurarShowDaBanda, 50);
    }
}

function main_index(){
    var answers = document.querySelectorAll(".answer-principal");
    for(var i = 0; i < answers.length; i++){
        var answer = answers[i];
        answer.addEventListener("click", opcaoNewsletter, false);
    }

    if(procurarBandasText){
        procurarBandasText.addEventListener("keypress", enterPressedProcuraBanda, false);
        procurarBandasButton.addEventListener("click", procurarShowDaBanda, false);
    }
}

main_index();