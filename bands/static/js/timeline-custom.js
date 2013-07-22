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
        var label = 'Banda: ' + timelineId + ' Texto: ' + $(elm).text();
        if(typeof _gaq != "undefined"){
            _gaq.push(['_trackEvent', 'Band Timeline', 'Navegacao Musica', label]);
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

    $(document).on("click", ".navegacao-musica", function(){
        var index = 1;
        var classList = $(this).attr('class').split(/\s+/);
        for(var classIndex in classList){
            var classItem = classList[classIndex];
            if(classItem != "navegacao-musica" && classItem.indexOf("navegacao-musica-") !== -1){
                index = parseInt(classItem.replace("navegacao-musica-", ""));
                break;
            }
        }

        $('.flag-content')[index].click();

        gaNavegacaoMusica(this);
    });

    $(".nav-next").find(".date").each(function(){
        var currentDateWithoutYear = $(this).text().substring(0, -5).trim();
        var currentYear = $(this).text().replace(currentDateWithoutYear, "").trim();
        $(this).html("<span class='date-without-year'>" + currentDateWithoutYear + "</span><span class='date-year'>" + currentYear + "</span>");
    });

});
