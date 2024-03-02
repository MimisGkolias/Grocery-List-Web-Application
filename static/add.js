document.addEventListener('DOMContentLoaded', function(){

    const container = document.querySelector(".container");
    // container.classList.add('container');
    var first_button = document.getElementById('add-button');
    var first_input = document.getElementById('item0');
    document.querySelector('#new_list').addEventListener("keypress", function(event){
        if (event.key === 'Enter'){
            console.log(event.key);
            event.preventDefault();
        }
    });
    first_button.associatedInput = first_input;

    var buttons = new Map();
    // buttons.set(first_button, first_input);

    function addInput(event){
        event.preventDefault();
        // let inputs = document.querySelectorAll('#new_list input');
        // inputs.forEach(input => {
        //     input.addEventListener('keydown', function(event){
        //         if (event.key === 'Enter')
        //         {
        //             event.preventDefault();
        //         }
        //     });
        // });

        console.log("addInput function called");


        var button = event.target;
        var input = button.associatedInput;
        button.associatedInput = input;

        if (input.value !== '')
        {
            button.textContent = '-';
            button.id = 'remove-button';

            buttons.set(button, input);

            let new_div = document.createElement('div');
            new_div.classList.add('pair');


            let new_input = document.createElement('input');
            new_input.placeholder = 'Item';
            new_input.setAttribute('autocomplete', 'off');
            new_input.setAttribute('type', 'text');
            new_input.classList.add('form-control', 'input-width');
            new_input.name = "item" + document.getElementsByTagName("input").length;

            let new_button = document.createElement('button');
            new_button.innerHTML = "+";
            new_button.classList.add('btn', 'btn-primary', 'add-button');
            new_button.id = 'add-button';
            // new_button.onclick = addInput;

            new_button.associatedInput = new_input;

            new_div.appendChild(new_input);
            new_div.appendChild(new_button);

            container.appendChild(new_div);


        }

        else {
            alert("Please enter an item");
        }
        // alert(buttons);

    }

    function remove(event)
    {
        event.preventDefault();

        let button = event.target;
        let input = buttons.get(button);

        button.parentNode.removeChild(button);
        input.parentNode.removeChild(input);

        buttons.delete(button);

        for (let i=0; i<document.getElementsByTagName("input").length; i++)
        {
            document.getElementsByTagName("input")[i].name = "item" + i;
        }

    }

    document.addEventListener('click', function(event){
        if (event.target.id === 'add-button')
        {
            addInput(event);
        }
        else if (event.target.id === 'remove-button')
        {
            remove(event);
        }
    });


    let submitButton = document.getElementById("submit-button");
    submitButton.addEventListener('click', function(event){

        let inputs = document.getElementsByTagName("input");
        let lastInputValue = inputs[inputs.length - 1].value;
        if (lastInputValue !== '')
        {
            let targetInputElement = inputs[inputs.length - 1];
            targetInputElement.value = lastInputValue;
        }
        else if (lastInputValue === '')
        {
            alert("Please enter an item");
            event.preventDefault();
        }

    });

});
