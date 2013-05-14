var erroProcurarBandas = document.querySelector('#erro-procurar-bandas');
var procurarBandasText = document.querySelector('#opcoes-procurar-bandas-text');
var procurarBandasButton = document.querySelector('#opcoes-procurar-bandas-button');

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

function adicionarBandaProcurada(){
    if (httpRequest.readyState === 4) {
        if (httpRequest.status === 200) {
            var htmlNovaBanda = httpRequest.responseText;
            var novaBanda = $(htmlNovaBanda);
            var minhasBandasLista = $('#minhas-bandas-lista');
            if(htmlNovaBanda){
                minhasBandasLista.prepend(novaBanda);
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

function procurarBandaHome(){
    var bandName = procurarBandasText.value;
    procurarBandasText.value = "";
    makeRequestBandHome(bandName);
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
        _gaq.push(['_trackEvent', 'Band', 'Gênero em uma pesquisa de banda', 'Banda: ' + bandaNome + ' Genero: ' + genero]);
    }
}

function carregaTimeline(timelineId){ // Ex.: timelineId='the-beatles-timeline'
    createStoryJS({
        type:       'timeline',
        width:      '800',
        height:     '600',
        lang:       'pt-br',
        source:     '/band/' + timelineId + '.json',
        embed_id:   timelineId
    });
}

function carregaTimelines(){
    $(".band-timeline").each(function(){
        var timelineId = $(this).attr("id");
        carregaTimeline(timelineId);
    });
}

function toggleBand(){
    var bandParent = $(this).parent();
    var bandSlug = bandParent.attr('id');
    var areaBanda = bandParent.find('#area-banda');
    var infoBanda = bandParent.find('#info-banda');
    var photoIcon = bandParent.find('.photo-icon');
    var timelineBanda = bandParent.find('.timeline-banda');
    var label = bandParent.find('.label');

    if(areaBanda.hasClass('hidden')) {
        areaBanda.removeClass('hidden');
        infoBanda.removeClass('hidden');
        timelineBanda.removeClass('timeline-invisivel');
        photoIcon.css('visibility', 'hidden');
        label.addClass('hidden');

        if(typeof _gaq != "undefined"){
            _gaq.push(['_trackEvent', 'Band', 'Expandir', 'Banda: ' + bandSlug]);
        }
    }else {
        areaBanda.addClass('hidden');
        infoBanda.addClass('hidden');
        timelineBanda.addClass('timeline-invisivel');
        photoIcon.css('visibility', 'visible');
        label.removeClass('hidden');

        if(typeof _gaq != "undefined"){
            _gaq.push(['_trackEvent', 'Band', 'Retrair', 'Banda: ' + bandSlug]);
        }
    }
}

function main_index(){
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

    $(document).on('click', '.info-banda-header', toggleBand);

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
