<script src="https://unpkg.com/stimulus/dist/stimulus.umd.js"></script>
<script type="text/javascript">
    const application = Stimulus.Application.start()

    application.register("new-recipe", class extends Stimulus.Controller {
      static get targets() {
        return [
          "baseSelect",
          "select", "ingredientTable", "selectDiet",

          "loader", "wrongRecipe",

          "recipeName", "recipeSize", "recipeDiet",
          "recipe", "recipeIngredientTable"
          ]
      }

      connect() {
        this.recipe__hideAll()
      }

      _refresh_select(){
        this.selectTarget.innerHTML = this.baseSelectTarget.innerHTML;

        for (let i = 0, ingredient; ingredient = this._get_currently_selected()[i]; i++) {
          let option = this.selectTarget.querySelector("option[value='" + ingredient.id + "']");
          option.remove();
        }
      }

      add_ingredient(e){
        e.preventDefault();

        if (this.selectTarget.value == false){return false;}
        else{
          fetch("{{ url_for('RecipesView:addIngredientAJAX') }}",{
            method: 'POST',
            body: JSON.stringify({'ingredient_id' : this.selectTarget.value}),
            headers: {'Content-Type': 'application/json,charset=UTF-8'}}
          ).then((response) => { return response.json(); }
          ).then((response) => {
            $(this.ingredientTableTarget).append(response['template_data']);
            this._check_if_first_ingredient();
            this._refresh_select();
            
            this.recipe__hideAll();
          });
        }
      }

      _check_if_first_ingredient(){
        if (this._get_currently_selected().length == 1){
          this._set_main_ingredient(this._get_currently_selected()[0].id)
        }
      }

      set_main_ingredient(event){
        var id = event.target.parentNode.dataset.id
        this._set_main_ingredient(id)
      }
      
      _set_main_ingredient(id){
        for (let i = 0, row; row = this.ingredientTableTarget.rows[i]; i++) {
            row.removeAttribute("data-main");

            if (row.dataset.id == id){
                row.dataset.main = "true";
                row.removeAttribute("data-fixed");
            }
        }
      }

      remove_ingredient(event){
        var id = event.target.parentNode.dataset.id

        for (let i = 0, row; row = this.ingredientTableTarget.rows[i]; i++) {
            if (row.dataset.id == id){
                row.remove()
            }
        }
        this._refresh_select();
        $(".recipe__right").hide();
      }

      toggle_fixed_ingredient(event){
        var id = event.target.parentNode.dataset.id
        for (let i = 0, row; row = this.ingredientTableTarget.rows[i]; i++) {
            if (row.dataset.id == id){
                if (row.dataset.fixed != "true"){
                    row.dataset.fixed = "true";
                    row.removeAttribute("data-main");
                } else {
                    row.removeAttribute("data-fixed");
                }
            }
        }
      }

      _row_to_ingredient(row){
        var ingredient = {}
        ingredient['id'] = row.dataset.id
        ingredient['name'] = row.dataset.name

        // optional
        ingredient['main'] = row.dataset.main
        ingredient['fixed'] = row.dataset.fixed
        ingredient['amount'] = row.dataset.amount

        return ingredient
      }

      _get_currently_selected(){
        return this._get_ingredients_from_table(this.ingredientTableTarget)
      }

      _get_currently_calculated(){
        return this._get_ingredients_from_table(this.recipeIngredientTableTarget)
      }

      _get_ingredients_from_table(table){
        var ingredients = [];

        for (let i = 1, row; row = table.rows[i]; i++) {
          if ("id" in row.dataset){
            let ingredient = this._row_to_ingredient(row)
            ingredients.push(ingredient);
          }

        }
        return ingredients;
      }

      _get_main_ingredient(ingredients){
        for (let i = 0, ingredient; ingredient = ingredients[i]; i++) {
          if (ingredient.main){
            return ingredient;
          }
        }
        return null;  
      }

      calculate_recipe(e){
        e.preventDefault();

        this.recipe__loader__show()

        var selected_ingredients = this._get_currently_selected()

        var main_count = selected_ingredients.filter((x) => x.main).length
        var fixed_count = selected_ingredients.filter((x) => x.fixed).length
        var variable_count = selected_ingredients.length - (main_count + fixed_count)

        // main to variable if necessary
        if (variable_count == 2 && main_count == 1){
          var main_ingredient = this._get_main_ingredient(selected_ingredients)
          if (! main_ingredient === null ){
              main_ingredient.removeAttribute("data-main");
              main_count--;
              variable_count++;
          }
        }

        //nefixních (počítaná + hlavní) > 4
        if (variable_count + main_count > 4){
            bootbox.alert("Příliš mnoho počítaných surovin - počítané suroviny musí být právě 3");
            this._hide_loader();
            return false;
        }
        //málo počítaných surovin
        if (variable_count + main_count < 3){
            bootbox.alert("Příliš málo počítaných surovin - počítané suroviny musí být právě 3");
            this._hide_loader();
            return false;
        }

        // values for fixed
        selected_ingredients.forEach(function(ingredient, i){
          if (ingredient.fixed){
            ingredient.amount = parseFloat(prompt("Množství suroviny " + ingredient.name + " v gramech :","").replace(",","."));
          }
        })

        var dietID = this.selectDietTarget.value

        this._calculate_core(selected_ingredients, dietID)
      }

      recalculate_recipe(e){
        e.preventDefault();
        this.recipe__loader__show()

        var calculated_ingredients = this._get_currently_calculated()
        var main_ingredient = this._get_main_ingredient(calculated_ingredients)

        main_ingredient.amount = $("#slider").val();
        main_ingredient.fixed = true
        main_ingredient.min = $('#slider')[0].dataset.sliderMin;
        main_ingredient.max = $('#slider')[0].dataset.sliderMax;

        var dietID = this.recipeDietTarget.dataset.newRecipeDietId

        this._calculate_core(calculated_ingredients, dietID)
      }

      _calculate_core(ingredients, dietID){
        fetch("{{ url_for('RecipesView:calcRecipeAJAX') }}", {
          method: 'POST',
          body: JSON.stringify({
              'ingredients' : ingredients,
              'dietID' : dietID,
              'trial' : '{{ is_trialrecipe|safe }}'
          }),
          headers: {'Content-Type': 'application/json,charset=UTF-8'},
        })
        .then((response) => {
          if (!response.ok){
            this.recipe__wrong__show();
            throw new Error(response);
          }
          return response.json();
        })
        .then((response) => {
          var template_data = response.template_data;

          if (response == "False"){
              this.recipe__wrong__show();
              return;
          }

          this.recipeTarget.innerHTML = template_data
          var mySlider = $("#slider").slider();

          this.recipe__right__show();

        })
      }

      save_recipe(e){
        e.preventDefault();

        fetch("{{ url_for('RecipesView:saveRecipeAJAX') }}", {
          method: 'POST',
          body: JSON.stringify({
            'ingredients' : this._get_currently_calculated(),
            'dietID' : this.recipeDietTarget.dataset.newRecipeDietId,
            'name' : this.recipeNameTarget.value,
            'size' : this.recipeSizeTarget.value
          }),
          headers: {'Content-Type': 'application/json,charset=UTF-8'},
        })
        .then((response) => {
          return response.text(); })
        .then((response) => {
          var pathname = window.location.pathname.split("/")[0];
          window.location.replace(pathname + response);
        })
      }

      _hide_loader(){
        $(this.loaderTarget).hide();
      }

      recipe__loader__show(){
        $(this.loaderTarget).show();
        $(this.recipeTarget).hide();
        $(this.wrongRecipeTarget).hide();
      }

      recipe__wrong__show(){
        $(this.recipeTarget).hide();
        $(this.wrongRecipeTarget).show();
        $(this.loaderTarget).hide();
      }

      recipe__right__show(){
        $(this.recipeTarget).show();
        $(this.wrongRecipeTarget).hide();
        $(this.loaderTarget).hide();
      }

      recipe__hideAll(){
        $(this.recipeTarget).hide();
        $(this.wrongRecipeTarget).hide();
        $(this.loaderTarget).hide();
      }
    });
    </script>

<script type="text/javascript">
  Array.prototype.empty = function(){
      this.length = 0
  }

  $(document).ready(function() {
    $('#ingredient_select').select2();
  });

  function trialSaveConfirm(){
      r = confirm("Pokud si chcete recept uložit, musíte se zaregistrovat")
      if (r == true){
          var win = window.open('{{ url_for("RegisterView:show") }}');
      }
      return true;
  }
</script>