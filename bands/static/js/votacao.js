var httpRequest;

function makeRequestAddBand(url, band, facebook_id) {
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
    httpRequest.onreadystatechange = showNewBand;
    httpRequest.open('POST', url);
    httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    httpRequest.send('band=' + encodeURIComponent(band) + '&user_facebook_id=' + facebook_id);
}

var votacaoInput = document.querySelector('#adicionar-item-votacao-text');
var facebookIdInput = document.querySelector('#user_facebook_id');

function showNewBand() {
    if (httpRequest.readyState === 4) {
        if (httpRequest.status === 200) {
            var response = httpRequest.responseText.split("\n");
            var band_name = response[0]
            var band_slug = response[1]
            var bands_list = document.querySelector('.list_bands_user_likes');
            bands_list.innerHTML += '<li><input type="checkbox" checked="checked" value="' + band_slug + '" /> ' + band_name + '</li>';
            votacaoInput.value = "";
        } else {
            console.log('There was a problem with the request.');
        }
    }
}

function adicionarItem() {
    var url_create_band = "/add_band/";
    var band = votacaoInput.value;
    var facebook_id = facebookIdInput.value;
    makeRequestAddBand(url_create_band, band, facebook_id)
}

function enterPressed(e) {
    if (e.keyCode == 13) {
        adicionarItem();
    }
}

function votacao(){
    var votacaoButton = document.querySelector('#adicionar-item-votacao-button');
    votacaoButton.addEventListener("click", adicionarItem, false);
    votacaoInput.addEventListener("keypress", enterPressed, false);
}

votacao();