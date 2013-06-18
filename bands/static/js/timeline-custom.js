$(document).ready(function(){
    carregaTimelines();

    function findParentTimelineId(elm){
        var elm = $(elm);
        while(!elm.hasClass("storyjs-embed")){
            elm = elm.parent();
        }
        return elm.attr("id");
    }

    function gaNavegacaoMusica(elm){
        var timelineId = findParentTimelineId(elm);
        if(typeof _gaq != "undefined"){
            _gaq.push(['_trackEvent', 'Band Timeline', 'Navegacao Musica', 'Banda: ' + timelineId + ' Texto: ' + $(elm).text()]);
        }
    }

    $(document).on("click", ".nav-container", function(){
        var timelineId = findParentTimelineId(this);
        if(typeof _gaq != "undefined"){
            _gaq.push(['_trackEvent', 'Band Timeline', 'Navegacao pelas setas laterais', 'Banda: ' + timelineId]);
        }
    });

    $(document).on("click", ".flag", function(){
        var timelineId = findParentTimelineId(this);
        if(typeof _gaq != "undefined"){
            _gaq.push(['_trackEvent', 'Band Timeline', 'Navegacao pelos paineis na barra de rolagem embaixo', 'Banda: ' + timelineId + ' Texto: ' + $(this).text()]);
        }
    });

    $(document).on("click", ".media", function(){
        var timelineId = findParentTimelineId(this);
        if(typeof _gaq != "undefined"){
            _gaq.push(['_trackEvent', 'Band Timeline', 'Clicou em video ou texto da wikipedia', 'Banda: ' + timelineId]);
        }
    });

    $(document).on("click", ".navegacao-musica-2", function(){
        $('.flag-content')[2].click();
        gaNavegacaoMusica(this);
    });

    $(document).on("click", ".navegacao-musica-3", function(){
        $('.flag-content')[3].click();
        gaNavegacaoMusica(this);
    });

    $(".nav-next").find(".date").each(function(){
        var currentDateWithoutYear = $(this).text().substring(0, -5).trim();
        var currentYear = $(this).text().replace(currentDateWithoutYear, "").trim();
        $(this).html("<span class='date-without-year'>" + currentDateWithoutYear + "</span><span class='date-year'>" + currentYear + "</span>");
    });

});
