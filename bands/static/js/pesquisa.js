function showElementsOfAClass(className){
    var classElements = document.querySelectorAll('.' + className);
    for (var index = 0; index < classElements.length; index++){
        var element = classElements[index];
        element.classList.remove("hidden");
    }
}

function hideElementsOfAClass(className){
    var classElements = document.querySelectorAll('.' + className);
    for (var index = 0; index < classElements.length; index++){
        var element = classElements[index];
        element.classList.add("hidden");
    }
}

function toggleAllAnswers(classNameToShow){
    var classesNames = ['musico', 'fa'];

    for (var classNameIndex in classesNames){
        var className = classesNames[classNameIndex];

        if(className == classNameToShow){
            showElementsOfAClass(className);
        }
        else{
            hideElementsOfAClass(className);
        }
    }

}

function showElements(event){
    document.querySelector('#questions').classList.remove("hidden");
    var classNameToShow = this.dataset.classNameToShow;
    toggleAllAnswers(classNameToShow)
}

function main (){
    var answerMainNodes = document.querySelectorAll('input.answer_main');

    for (var answerIndex = 0; answerIndex < answerMainNodes.length; answerIndex++){
        var answerMainNode = answerMainNodes[answerIndex];

        answerMainNode.addEventListener('click', showElements, false);
    }
}

main();