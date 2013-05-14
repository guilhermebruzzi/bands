$(document).ready(function(){
    carregaTimelines();

    function findParentTimelineId(elm){
        var elm = $(elm);
        while(!elm.hasClass("storyjs-embed")){
            elm = elm.parent();
        }
        return elm.attr("id");
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

});
