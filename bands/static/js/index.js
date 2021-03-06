var erroProcurarBandas = document.querySelector('#erro-procurar-bandas');
var procurarBandasText = document.querySelector('#opcoes-procurar-bandas-text');

var disqus_shortname = 'bands';
var disqus_identifier; //unique identifier
var disqus_url; //post permalink
// var disqus_title; //post title

function loadDisqus(source, identifier, url) {

    if (window.DISQUS) {

        jQuery('#disqus_thread').insertAfter(source); //append the HTML after the link

        //if Disqus exists, call it's reset method with new parameters
        DISQUS.reset({
            reload: true,
            config: function () {
                this.page.identifier = identifier;
                this.page.url = url;
                // this.page.title = title
            }
        });

    } else {

        //insert a wrapper in HTML after the relevant "show comments" link
        jQuery('<div id="disqus_thread"></div>').insertAfter(source);
        disqus_identifier = identifier; //set the identifier argument
        disqus_url = url; //set the permalink argument
        // disqus_title = title;

        //append the Disqus embed script to HTML
        var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
        dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
        jQuery('head').append(dsq);

    }
};

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
            $("#banda-loading").addClass("hidden");
            minhasBandasLista.removeClass("padding-80");


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


function infoBandaGeneroClicked(){
    var bandaNome = $(this).parent().parent().find(".info-banda-nome").text();
    var genero = $(this).text();

    if(typeof _gaq != "undefined"){
        _gaq.push(['_trackEvent', 'Band', 'Gênero em uma pesquisa de banda', 'Banda: ' + bandaNome + ' Genero: ' + genero]);
    }
}

function contribuaTimelineClicked(){
    var bandaNome = $(this).parent().parent().parent().find(".info-banda-nome").text();

    if(typeof _gaq != "undefined"){
        _gaq.push(['_trackEvent', 'Band Timeline', 'Botao colabore', 'Banda: ' + bandaNome]);
    }
}

function enviarContribuicaoClicked(){
    var modal = $(this).parent().parent();
    var bandaSlug = modal.attr("id").replace("modal-contribuicao-", "");
    var data = modal.find(".data-acontecimento").val();
    var texto = modal.find(".texto-acontecimento").val();

    if(typeof _gaq != "undefined"){
        _gaq.push(['_trackEvent', 'Band Timeline', 'Enviar Contribuicao', 'Banda: ' + bandaSlug + ' Data:' + data + ' Texto: ' + texto]);
    }
    alert('Obrigado por contribuir, iremos avaliar a sua contribuicao e incluí-la em breve! :)');
}

function mostrarComentariosClicked(){
    var bandaNome = $(this).parent().parent().find(".info-banda-nome").text();

    if(typeof _gaq != "undefined"){
        _gaq.push(['_trackEvent', 'Band', 'Ver comentários em uma pesquisa de banda', 'Banda: ' + bandaNome]);
    }

    $(".mostrar-comentarios").removeClass("invisivel");
    $(this).addClass("invisivel");
}

function favoritarClicked(){
    var bandaNome = $(this).parent().parent().parent().find(".info-banda-nome").text();

    if(typeof _gaq != "undefined"){
        _gaq.push(['_trackEvent', 'Band', 'Favoritar em uma pesquisa de banda', 'Banda: ' + bandaNome]);
    }

    $(this).toggleClass("favoritou");
}

function carregaTimeline(timelineId){ // Ex.: timelineId='the-beatles-timeline'
    createStoryJS({
        type:       'timeline',
        width:      '90%',
        height:     '90%',
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
    var shareBanda = bandParent.find('.share');
    var comentariosBanda = bandParent.find('.comentarios');
    var mostrarComentarios = comentariosBanda.find('.mostrar-comentarios');
    var label = bandParent.find('.label');

    if(timelineBanda.hasClass('invisivel')) {
        areaBanda.removeClass('hidden');
        infoBanda.removeClass('hidden');
        timelineBanda.removeClass('invisivel');
        label.addClass('hidden');

        if(typeof _gaq != "undefined"){
            _gaq.push(['_trackEvent', 'Band', 'Expandir', 'Banda: ' + bandSlug]);
        }
    }else {
        areaBanda.addClass('hidden');
        infoBanda.addClass('hidden');
        timelineBanda.addClass('invisivel');
        label.removeClass('hidden');

        if(typeof _gaq != "undefined"){
            _gaq.push(['_trackEvent', 'Band', 'Retrair', 'Banda: ' + bandSlug]);
        }
    }
}

function main_index(){
    if(procurarBandasText){
        procurarBandasText.addEventListener("keypress", enterPressedProcuraBandaHome, false);
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

    $('#minhas-bandas-lista').on("click", ".favoritar", favoritarClicked);
    $('#minhas-bandas-lista').on("click", ".favoritar-texto", favoritarClicked);

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

    var bandasDatalist = $("#bandas");
    if(bandasDatalist.length > 0){
        bandasDatalist.load("/bandas-datalist/");
    }

    var minhasBandasListas = $("#minhas-bandas-lista");

    if(minhasBandasListas.length > 0 && $(".deslogado").length > 0){
        $.ajax({
            type: "GET",
            url: "/bandas-locais/"
        }).done(function(htmlBandasLocais) {
                minhasBandasListas.append(htmlBandasLocais);
        });
    }

    $('#minhas-bandas').on('click', ".mostrar-comentarios", mostrarComentariosClicked);

    $('#minhas-bandas').on('click', '.similar', function(){
        var bandaLoading = $('#banda-loading');
        if(bandaLoading.hasClass("hidden")){
            bandaLoading.removeClass("hidden");
        }
        $("#minhas-bandas-lista").addClass("padding-80");
        var bandName = $(this).text();
        makeRequestBandHome(bandName);
        window.location.href = window.location.href.replace(window.location.hash, "") + "#minhas-bandas"
    });

    $(document).on('click', ".contribua-timeline", contribuaTimelineClicked);
    $(document).on('click', ".enviar-contribuicao", enviarContribuicaoClicked);

}

main_index();
