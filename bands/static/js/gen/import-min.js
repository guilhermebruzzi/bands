function main_index(){var f=document.body.clientHeight;var g=document.querySelector("#descricao");var j=g.offsetHeight;var b=10;var e=document.querySelector(".container > header");var c=e.offsetHeight;var i=document.querySelector(".container > footer");var h=i.offsetHeight;var d=document.querySelector("#informacoes-existentes");if(g&&d){var a=f-c-h;if(f>830){d.style.height=a+"px";g.style.height=a+"px";g.style.marginBottom="0px"}else{d.style.height=a+b+"px";g.style.height=a+"px"}}}main_index();function showElementsOfAClass(c){var d=document.querySelectorAll("."+c);for(var a=0;a<d.length;a++){var b=d[a];b.classList.remove("hidden")}}function hideElementsOfAClass(c){var d=document.querySelectorAll("."+c);for(var a=0;a<d.length;a++){var b=d[a];b.classList.add("hidden")}}function toggleAllAnswers(b){var d=["musico","fa"];for(var a in d){var c=d[a];if(c==b){showElementsOfAClass(c)}else{hideElementsOfAClass(c)}}}function showElements(b){document.querySelector("#questions").classList.remove("hidden");var a=this.value;toggleAllAnswers(a)}function main_pesquisa(){var a=document.querySelectorAll("input.answer_main");for(var c=0;c<a.length;c++){var b=a[c];b.addEventListener("click",showElements,false)}}main_pesquisa();var _gaq=_gaq||[];_gaq.push(["_setAccount","UA-36066139-1"]);_gaq.push(["_trackPageview"]);(function(){var b=document.createElement("script");b.type="text/javascript";b.async=true;b.src=("https:"==document.location.protocol?"https://ssl":"http://www")+".google-analytics.com/ga.js";var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(b,a)})();function adicionarItem(a){alert(a)}function votacao(){var a=document.querySelector("#adicionar-item-votacao-button");var b=document.querySelector("#adicionar-item-votacao-text");alert("teste");a.addEventListener("click",adicionarItem(b.value),false)}votacao();