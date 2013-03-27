function hideUserVoice(){
    var userVoice = document.querySelector('#uvTab');
    userVoice.style.display = "none";
}
function mainApenasProdutosSection(){
    var produtosSection = document.querySelector('#produtos-section');
    produtosSection.style.margin = "0 0";
    if(produtosSection){
        var sectionContainer = document.querySelector('.container');
        var header = document.querySelector('.container header');
        var footer = document.querySelector('.container footer');
        sectionContainer.removeChild(header);
        sectionContainer.removeChild(footer);

        window.setInterval(hideUserVoice, 500);
    }
}

mainApenasProdutosSection();
