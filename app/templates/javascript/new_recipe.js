<script src="https://unpkg.com/stimulus/dist/stimulus.umd.js"></script>
<script type="text/javascript">
    const application = Stimulus.Application.start()

    application.register("new-recipe", class extends Stimulus.Controller {
      static get targets() {
        return [
          "name", "select", "baseSelect", "selectDiet",
          "ingredientTable",
          "recipeName", "recipeSize", "recipeDiet",
          "recipe", "recipeIngredientTable",
          "loader", "wrongRecipe"
          ]
      }

      connect() {
        this.recipe__hideAll()
      }

      _refresh_select(){
          this.selectTarget.innerHTML = this.baseSelectTarget.innerHTML;

          var selected_ingredients = this._get_currently_selected();

          for (let i = 0, ingredient; ingredient = this._get_currently_selected()[i]; i++) {
            let option = this.selectTarget.querySelector("option[value='" + ingredient.id + "']")
            option.remove();
          }
      }

      add_ingredient(e){
        if (this.selectTarget.value == false){return false;}
        else{
          fetch("{{ url_for('RecipesView:addIngredientAJAX') }}",{
                method: 'POST',
                body: JSON.stringify({'ingredient_id' : this.selectTarget.value}),
                headers: {'Content-Type': 'application/json,charset=UTF-8'},
          }
          ).then((response) => { return response.json(); }
          ).then((response) => {
            var template_data = response['template_data'];

            $(this.ingredientTableTarget).append(template_data);
            this._check_if_first_ingredient();
            this._refresh_select();
            
            this.recipe__hideAll();

          });
        }
        e.preventDefault();
      }

      _check_if_first_ingredient(){
        if (this._get_currently_selected().length == 1){
          this.set_main_ingredient(this._get_currently_selected()[0].id)
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

        //TODO: if deleted main ingredient, select new one
        //
        $(".recipe__right").hide();
      }
      
      set_main_ingredient(event){
        if (isNaN(arguments[0])) {
          var id = event.target.parentNode.dataset.id
        } else {
          var id = arguments[0]
        }
        for (let i = 0, row; row = this.ingredientTableTarget.rows[i]; i++) {
            row.removeAttribute("data-main");

            if (row.dataset.id == id){
                row.dataset.main = "true";
                row.removeAttribute("data-fixed");
            }
        }
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

      _get_currently_selected(){
        var selected_ingredients = [];

        for (let i = 1, row; row = this.ingredientTableTarget.rows[i]; i++) {

          var ingredient = {}
          ingredient['id'] = row.dataset.id

          // optional
          ingredient['main'] = row.dataset.main
          ingredient['fixed'] = row.dataset.fixed
          ingredient['amount'] = row.dataset.amount

          selected_ingredients.push(ingredient);
        }
        return selected_ingredients;
      }

      _get_currently_calculated(){
        var ingredients = [];

        for (let i = 1, row; row = this.recipeIngredientTableTarget.rows[i]; i++) {
          if ("id" in row.dataset){
            var ingredient = {}
            ingredient['id'] = row.dataset.id

            // optional
            ingredient['main'] = row.dataset.main
            ingredient['amount'] = row.dataset.amount

            ingredients.push(ingredient);
          }

        }
        return ingredients;

      }

      _get_main_ingredient(){
        for (let i = 0, ingredient; ingredient = this._get_currently_selected()[i]; i++) {
          if (ingredient.dataset.main){
            return ingredient;
          }
        }
        return null;  
      }

      calculate_recipe(e){
        e.preventDefault();
        this.recipe__loader__show()

        var main_count = 0;
        var fixed_count = 0;
        var variable_count = 0;

        var selected_ingredients = this._get_currently_selected()

        for (let i = 0, ingredient; ingredient = selected_ingredients[i]; i++) {
          if (ingredient.main){
            main_count++;
          } else if (ingredient.fixed){
            fixed_count++;
          } else {
            variable_count++;
          }
        }

        // main to variable if necessary
        if (variable_count == 2 && main_count == 1){
          var main_ingredient = this._get_main_ingredient()
          if (! main_ingredient === null ){
              ingredient.removeAttribute("data-main");
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
        for (let i = 0, ingredient; ingredient = this._get_currently_selected()[i]; i++) {
          if (ingredient.fixed){
            ingredient.amount = parseFloat(prompt("Množství suroviny " + ingredient.name + " v gramech :","").replace(",","."));
          }
        }

        var url = "{{ url_for('RecipesView:calcRecipeAJAX') }}"
        var dietID = this.selectDietTarget.value

        this._calculate_core(url, selected_ingredients, dietID)
      }

      recalculate_recipe(e){
        e.preventDefault();
        this.recipe__loader__show()

        var calculated_ingredients = this._get_currently_calculated()

        calculated_ingredients.forEach(function(ingredient, i){
          if (ingredient.main == "true"){
            ingredient.amount = $("#slider").val();
            ingredient.fixed = true
            ingredient.min = $('#slider')[0].dataset.sliderMin;
            ingredient.max = $('#slider')[0].dataset.sliderMax;
          }
        })

        var url = "{{ url_for('RecipesView:calcRecipeAJAX') }}"
        var dietID = this.recipeDietTarget.dataset.newRecipeDietId

        this._calculate_core(url, calculated_ingredients, dietID)
      }

      _calculate_core(url, ingredients, dietID){
        fetch(url,{
          method: 'POST',
          body: JSON.stringify({
              'ingredients' : ingredients,
              'dietID' : dietID,
              'trial' : '{{ is_trialrecipe|safe }}'
          }),
          headers: {'Content-Type': 'application/json,charset=UTF-8'},
        }
        ).then((response) => { return response.json(); }
        ).then((response) => {
        var ingredients = response.ingredients;
            var template_data = response.template_data;
            var diet = response.diet

            if (response == "False"){
                this.recipe__wrong__show();
                return;
            }

            // fill with html
            this.recipeTarget.innerHTML = template_data

            var mySlider = $("#slider").slider();

            // change visibility
            this.recipe__right__show();

        });

        
      }

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
                    var pathname = window.location.pathname.split("/")[0];
                    window.location.replace(pathname + response);
                },
                error: function(error) {
                    // console.log(error);
                }
        });
        e.preventDefault();
      }

        //       $(this.recipeTarget).hide();
        // $(this.wrongRecipeTarget).hide();
        // $(this.loaderTarget).hide();

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