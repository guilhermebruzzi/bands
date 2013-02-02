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

function opcaoNewsletter(){
    var option = (this.innerHTML == "Sim") ? "sim" : "nao";
    var cadastro = document.querySelector(".cadastro");
    if(cadastro){ // Se tiver o elemento para fazer cadastro, é porque a pessoa não está logada
        if(option == "sim"){
            var fazerLogin = confirm("Para receber shows, é necessário efetuar login, deseja entrar no site agora (com o facebook isso é feito em apenas 1 clique)?");
            if (fazerLogin)
            {
                window.location = "/login/";
                return;
            }
        }
        this.parentNode.style.display = "none";
    } else{
        var tipo = "Meus Shows";
        for(var i in this.parentNode.classList){
            var classe = this.parentNode.classList[i];
            if(classe == "newsletter-shows-locais"){
                tipo = "Shows Locais";
            }
        }
        makeRequestNewsletter(option, tipo);
        this.parentNode.style.display = "none";
    }
}

function main_index(){
    var answers = document.querySelectorAll(".answer-principal");
    for(var i = 0; i < answers.length; i++){
        var answer = answers[i];
        answer.addEventListener("click", opcaoNewsletter, false);
    }
}

main_index();