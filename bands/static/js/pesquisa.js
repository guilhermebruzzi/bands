var answer_main_nodes = document.getElementsByClassName('answer_main')

for (var answer_index = 0; answer_index < answer_main_nodes.length; answer_index++){

    var answer_main_node = answer_main_nodes[answer_index]

    answer_main_node.addEventListener('click', function(event) {
        document.getElementById('questions').classList.remove("hidden")
    }, false);

}
