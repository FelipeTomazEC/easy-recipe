function createRecipeIngredient() {
    const availableIngredients = JSON.parse(document.getElementById('ingredient_list').textContent) ?? []

    // Create the fieldset
    const recipeIngredient = document.createElement('fieldset');
    recipeIngredient.className = 'recipe-ingredient';

    // Create the label for the ingredient select
    const ingredientLabel = document.createElement('label');
    ingredientLabel.setAttribute('for', 'ingredient');
    ingredientLabel.textContent = 'Ingredient';
    recipeIngredient.appendChild(ingredientLabel);

    // Create the select element for ingredients
    const ingredientSelect = document.createElement('select');
    ingredientSelect.name = `ingredients[${getIngredientsCount()}][ean]`;

    // Loop through the ingredientList and create option elements
    availableIngredients.filter(ingredient => !isIngredientAlreadyPresent(ingredient))
        .forEach(ingredient => {
            const option = document.createElement('option');
            option.value = ingredient.ean;
            option.textContent = `${ingredient.name} (${ingredient.standard_unit})`;
            ingredientSelect.appendChild(option);
        });

    recipeIngredient.appendChild(ingredientSelect);

    // Create the label for the amount input
    const amountLabel = document.createElement('label');
    amountLabel.setAttribute('for', 'amount');
    amountLabel.textContent = 'Amount';
    recipeIngredient.appendChild(amountLabel);

    // Create the number input for amount
    const amountInput = document.createElement('input');
    amountInput.type = 'number';
    amountInput.name = `ingredients[${getIngredientsCount()}][amount]`;
    amountInput.id = 'amount';
    amountInput.min = '0';
    amountInput.step = '0.1'
    amountInput.value = '1';
    recipeIngredient.appendChild(amountInput);

    // Create the remove button
    const removeButton = document.createElement('button');
    removeButton.classList.add('remove-ingredient-btn')
    removeButton.classList.add('cancel-button')
    removeButton.type = 'button';
    removeButton.textContent = 'Remove';
    removeButton.onclick = () => recipeIngredient.remove()

    recipeIngredient.appendChild(removeButton);

    // Append the fieldset to the ingredients container
    document.querySelector('.ingredients').appendChild(recipeIngredient);
}

function getIngredientsCount() {
    return document.querySelectorAll('.recipe-ingredient').length;
}

function isIngredientAlreadyPresent(ingredient) {
    return [...document.querySelectorAll('select').values()]
        .map(select => select.value)
        .some(selectedOption => selectedOption === ingredient.ean);
}

document.addEventListener('DOMContentLoaded', function () {
    const removeIngredientButtons = document.querySelectorAll('.remove-ingredient-btn');
    removeIngredientButtons.forEach(button => button.onclick = (e) => e.srcElement.parentElement.remove());
})
