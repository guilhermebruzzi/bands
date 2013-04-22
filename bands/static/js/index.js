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
    var user_id = document.querySelector('#current_user_id').innerHTML;
    var params = 'tipo=' + encodeURIComponent(tipo) + '&user_id=' + encodeURIComponent(user_id);
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

function makeRequestBandHome(bandName) {
    if(typeof(_gaq) != "undefined"){
        _gaq.push(['_trackEvent', 'Band', 'Procurar Banda na Home', 'Banda: ' + bandName]);
    }
    if(erroProcurarBandas.classList.contains("visivel")){
        erroProcurarBandas.classList.remove("visivel");
        erroProcurarBandas.classList.add("invisivel");
    }
    erroProcurarBandas.innerHTML = 'Não encontramos nenhuma banda chamada: ' + bandName + '. Verifique se digitou o nome corretamente.';
    makeRequestServer("GET", "/search_band/" + bandName, adicionarBandaProcurada);
}

var procurarBandasText = document.querySelector('#opcoes-procurar-bandas-text');
var procurarBandasButton = document.querySelector('#opcoes-procurar-bandas-button');

function opcaoNewsletter(){
    var option = (this.innerHTML == "Sim") ? "sim" : "nao";
    var tipo = "Shows";

    makeRequestNewsletter(option, tipo);
    this.parentNode.parentNode.parentNode.style.display = "none";
}

function adicionarBandaProcurada(){
    if (httpRequest.readyState === 4) {
        if (httpRequest.status === 200) {
            var htmlBanda = httpRequest.responseText;
            var minhasBandasLista = document.querySelector('#minhas-bandas-lista');
            if(htmlBanda){
                minhasBandasLista.innerHTML = htmlBanda + minhasBandasLista.innerHTML;
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

function procurarBandaHome(){
    var bandName = procurarBandasText.value;
    procurarBandasText.value = "";
    makeRequestBandHome(bandName);
}

function enterPressedProcuraBanda(e) {
    if (e.keyCode == 13) {
        setTimeout(procurarShowDaBanda, 50);
    }
}

function enterPressedProcuraBandaHome(e) {
    if (e.keyCode == 13) {
        setTimeout(procurarBandaHome, 50);
    }
}

function gmailBtnClicked(){
    if(typeof _gaq != "undefined"){
        _gaq.push(['_trackEvent', 'Login', 'Login Botao Gmail', 'Login Gmail area minhas bandas pela index page']);
    }
    alert("Por enquanto não temos login pelo gmail, o login deve ser feito pelo facebook.\n" +
    "O Bands não postará nada em seu facebook e o login é bem rápido de ser feito.\n" +
    "No botão opine na parte direita você pode discutir sobre esse sistema de login.");
}

function bandsBtnClicked(){
    if(typeof _gaq != "undefined"){
        _gaq.push(['_trackEvent', 'Login', 'Login Botao Bands', 'Criar conta bands pela home']);
    }
    alert("Por enquanto não temos a opção de uma conta própria do Bands, sendo assim o login deve ser feito pelo facebook.\n" +
    "O Bands não postará nada em seu facebook e o login é bem rápido de ser feito.\n" +
    "No botão opine na parte direita você pode discutir sobre esse sistema de login.");
}

function historyTimelineBtnClicked(){
    alert("Por enquanto não temos a opção de história em formato de timeline.\n" +
    "Caso queira saber quando teremos essa opção faça login na parte superior do site.\n" +
    "No botão opine na parte direita você pode discutir sobre essa e outras opções que gostaria que tivessemos.");
}

function infoBandaGeneroClicked(){
    var bandaNome = $(this).parent().parent().find(".info-banda-nome").text();
    var genero = $(this).text();

    if(typeof _gaq != "undefined"){
        _gaq.push(['_trackEvent', 'Band', 'Gênero em timeline no modal de história', 'Banda: ' + bandaNome + ' Genero: ' + genero]);
    }
}

function main_index(){
    var answers = document.querySelectorAll(".answer-principal");
    for(var i = 0; i < answers.length; i++){
        var answer = answers[i];
        answer.addEventListener("click", opcaoNewsletter, false);
    }

    if(procurarBandasText){
        procurarBandasText.addEventListener("keypress", enterPressedProcuraBandaHome, false);
        procurarBandasButton.addEventListener("click", procurarBandaHome, false);
    }

    var gmailBtn = document.querySelector('#gmail-btn');
    if(gmailBtn){
        $(gmailBtn).click(gmailBtnClicked);
    }

    var bandsBtn = document.querySelector('#conta-bands-btn');
    if(bandsBtn){
        $(bandsBtn).click(bandsBtnClicked);
    }

    $('.modal').hide();

    $('#minhas-bandas-lista').on("click", ".favoritar", function(){
        var bandaNome = $(this).parent().parent().find(".info-banda-nome").text();

        if(typeof _gaq != "undefined"){
            _gaq.push(['_trackEvent', 'Band', 'Favoritar em uma pesquisa de banda', 'Banda: ' + bandaNome]);
        }

        $(this).toggleClass("favoritou");
    });

    $('#minhas-bandas-lista').on("change", ".nota", function(){
        var bandaNome = $(this).parent().parent().find(".info-banda-nome").text();
        var nota = $(this).val();

        if(typeof _gaq != "undefined"){
            _gaq.push(['_trackEvent', 'Band', 'Nota em uma pesquisa de banda', 'Banda: ' + bandaNome + ' Nota: ' + nota]);
        }
    });

    $('#minhas-bandas').on('click', ".close-banda", function(){
        $(this).parent().remove();
    });

    $('#minhas-bandas').on('click', ".favoritar", function(evt){
        evt.preventDefault();
        return false;
    });

    $('#minhas-bandas').on('click', ".ver-em-formato-timeline", historyTimelineBtnClicked);

    $('#minhas-bandas').on('click', ".info-banda-genero", infoBandaGeneroClicked);

    $(".enviar-pergunta").click(function(){
        var email = $(this).parent().parent().find(".email-pergunta").val();
        var texto = $(this).parent().parent().find(".texto-pergunta").val();
        var slug = $(this).parent().parent().find(".slug-pergunta").val();

        $.ajax({
            type: "POST",
            url: "/band-question/",
            data: { email: email, question: texto, band_slug: slug }
        }).done(function(msg) {
            alert(msg);
        });
    });
}

main_index();
