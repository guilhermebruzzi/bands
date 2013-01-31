function makeRequestNewsletter(option, tipo, callback) {
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

    httpRequest.open("POST", "/newsletter/" + option);
    httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    httpRequest.send('tipo=' + encodeURIComponent(tipo));
}

function confirmaLogado(){
    var cadastro = document.querySelector(".cadastro");
    if(cadastro){ // Se tiver o elemento para fazer cadastro, é porque a pessoa não está logada
        alert('É necessário fazer login (observe botão no quadro da direita) para receber shows no email');
    }
    else{
        var tipo = "Meus Shows";
        for(var i in this.classList){
            var classe = this.classList[i];
            if(classe == "newsletter-shows-locais"){
                tipo = "Shows Locais";
            }
        }

        var option = (this.innerHTML == "Sim") ? "sim" : "nao";
        makeRequestNewsletter(option, tipo);
        this.parentNode.style.display = "none";
    }
}

function main_index(){
    var answers = document.querySelectorAll(".answer");
    for(var i in answers){
        var answer = answers[i];
        answer.addEventListener("click", confirmaLogado, false);
    }
}

main_index();