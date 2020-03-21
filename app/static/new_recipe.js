const application = Stimulus.Application.start()

application.register("new-recipe", class extends Stimulus.Controller {
  static get targets() {
    return [ "name", "select", "ingredientTable",


    "recipeName", "recipeSize", "recipeDiet"]
  }

  connect() {}

  reset_select(){}

  add_ingredient(e){
    // add new element (ajax)
    // WIP - teď takhle obcházím to, že v AJAXu je this něco jiného. Celkově bych měl celý ajax-stimulus přepsat jinak
    var ingredientTableTarget = this.ingredientTableTarget

    if (this.selectTarget.value == null){
        return false;
    }
    else{
        $.ajax({
            type: 'POST',
            url: {{ url_for('RecipesView:addIngredientAJAX') }},
            data: $(this).serialize(),
            data: JSON.stringify({
                'ingredient_id' : this.selectTarget.value},
                null, '\t'),
            contentType: 'application/json;charset=UTF-8',
            success: function(response) {
                var ingredient = response['ingredient'];
                var template_data = response['template_data'];

                prerecipe__calc__form__ingredients__add(ingredient);
                prerecipe__addIngredient__form__select__refresh();

                $(ingredientTableTarget).append(template_data);
                
                recipe__hideAll();

            },
            error: function(error) {
                console.log(error);
            }
        });
        e.preventDefault();
    }
  }

  remove_ingredient(){}
  
  set_main_ingredient(id){
    for (let i = 0, row; row = this.ingredientTableTarget.rows[i]; i++) {
        row.removeAttribute("data-main");

        if (row.dataset.id_value == id){
            row.dataset.main = "true";
            row.removeAttribute("data-fixed");
        }
    }
  }

  set_fixed_ingredient(){}

  calculate_recipe(){}


  get_currently_selected(){
    var selected_ingredients = [];
    for (let i = 0, row; row = this.ingredientTableTarget.rows[i]; i++) {
        ingredient = {}
        ingredient['id'] = row.getAttribute("id_value")

        // optional
        ingredient['amount'] = row.dataset.getAttribute("amount")
        ingredient['fixed'] = row.dataset.getAttribute("fixed")
        ingredient['main'] = row.dataset.getAttribute("main")

        selected_ingredients.push(ingredient);
    }
    return selected_ingredient_ids;
  }

  toggle_loader(){}
  show_loader(){}
  hide_loader(){}

  save_recipe(e){
    var recipeNameTarget = this.recipeNameTarget
    var recipeSizeTarget = this.recipeSizeTarget
    var recipeDietTarget = this.recipeDietTarget

    // Save recipe AJAX
    $.ajax({
            type: 'POST',
            url: "{{ url_for('RecipesView:saveRecipeAJAX') }}",
            data: JSON.stringify({
                'ingredients' : recipe__ingredient_array,
                'dietID' : recipeDietTarget.dataset.newRecipeDietId,
                'name' : recipeNameTarget.value,
                'size' : recipeSizeTarget.value
            }),
            contentType: 'application/json;charset=UTF-8',
            success: function(response){
                // var pathname = window.location.pathname.split("/")[0];
                // window.location.replace(pathname + response);
            },
            error: function(error) {
                console.log(error);
            }
    });
    e.preventDefault();
  }
});