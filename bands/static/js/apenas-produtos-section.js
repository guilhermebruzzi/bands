function hideUserVoice(){
    var userVoice = document.querySelector('#uvTab');
    if (userVoice){
        userVoice.style.display = "none";
    }
}
function mainApenasProdutosSection(){
    var produtosSection = document.querySelector('#produtos-section');
    if(produtosSection){
        var sectionContainer = document.querySelector('.container');
        var header = document.querySelector('.container header');
        var footer = document.querySelector('.container footer');
        sectionContainer.removeChild(header);
        sectionContainer.removeChild(footer);

        var produtosSection = document.querySelector('.produtos-section');
        var areaBanda = document.querySelector('.area-banda');
        produtosSection.removeChild(areaBanda);
        produtosSection.style.width = '700px';
        produtosSection.style.margin = "0 0";
        produtosSection.innerHTML += '<footer style="width: 700px; margin: 50px 0 30px 0;">Quer saber de shows e produtos de outras bandas? Acesse o <a target="_blank" href="http://bands.com.br"><img src="http://bands.com.br/static/img/logoBands.jpg" style="width: 64px; height: 50px; position: relative; top: 10px;"></a></footer>';

        window.setInterval(hideUserVoice, 500);
    }
}

mainApenasProdutosSection();
