<script src="https://unpkg.com/stimulus/dist/stimulus.umd.js"></script>
<script type="text/javascript">
    const application = Stimulus.Application.start()

    application.register("new-recipe", class extends Stimulus.Controller {
      static get targets() {
        return [
          "name", "select", "baseSelect",
          "ingredientTable",
          "recipeName", "recipeSize", "recipeDiet"
          ]
      }

      connect() {
        $(".recipe__right").hide();
        $(".recipe__wrong").hide();
        $(".recipe__loader").hide();
      }

      refresh_select(){
          this.selectTarget.innerHTML = this.baseSelectTarget.innerHTML;

          var selected_ingredients = this.get_currently_selected();

          for (let i = 0, ingredient; ingredient = this.get_currently_selected()[i]; i++) {
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
            this.refresh_select();
            
            this.recipe__hideAll();

          });
        }
        e.preventDefault();
      }

      _check_if_first_ingredient(){
        if (this.get_currently_selected().length == 1){
          this.set_main_ingredient(this.get_currently_selected()[0].id)
        }
      }

      remove_ingredient(event){
        var id = event.target.parentNode.dataset.id
        for (let i = 0, row; row = this.ingredientTableTarget.rows[i]; i++) {
            if (row.dataset.id == id){
                row.remove()
            }
        }
        this.refresh_select();

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

      set_fixed_ingredient(event){
        var id = event.target.parentNode.dataset.id
        for (let i = 0, row; row = this.ingredientTableTarget.rows[i]; i++) {
            if (row.dataset.id == id){
                row.dataset.fixed = "true";
                row.removeAttribute("data-main");
            }
        }
      }

      calculate_recipe(){}


      get_currently_selected(){
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
                    console.log(error);
                }
        });
        e.preventDefault();
      }

      recipe__loader__show(){
        $(".recipe__loader").show();
        $(".recipe__right").hide();
        $(".recipe__wrong").hide();
      }

      recipe__wrong__show(){
        $(".recipe__loader").hide();
        $(".recipe__wrong").show();
        $(".recipe__right").hide();
      }

      recipe__right__show(){
        $(".recipe__loader").hide();
        $(".recipe__wrong").hide();
        $(".recipe__right").show();
      }

      recipe__hideAll(){
        $(".recipe__loader").hide();
        $(".recipe__wrong").hide();
        $(".recipe__right").hide();
      }
    });
    </script>

  <script type="text/javascript">
            var prerecipe__ingredient_array = [];
            var recipe__ingredient_array = [];
            var recipe__ingredient_dietID = "";

            Array.prototype.empty = function(){
                this.length = 0
            }

            $(document).ready(function() {
              $('#prerecipe__add-ingredient__form__select').select2();
            });

            // visibility
            function recipe__loader__show(){
                $(".recipe__loader").show();
                $(".recipe__right").hide();
                $(".recipe__wrong").hide();
            }

            function recipe__wrong__show(){
                $(".recipe__loader").hide();
                $(".recipe__wrong").show();
                $(".recipe__right").hide();
            }

            function recipe__right__show(){
                $(".recipe__loader").hide();
                $(".recipe__wrong").hide();
                $(".recipe__right").show();
            }


            $(document).on("submit", ".prerecipe__calc__form", function(e) {

                    // check conditions - ingredients types count
                    main_count = 0;
                    fixed_count = 0;
                    variable_count = 0;
                    for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                        if (prerecipe__ingredient_array[i].fixed == true){
                            fixed_count++;
                        } else if (prerecipe__ingredient_array[i].main == true){
                            main_count++;
                        } else {
                            variable_count++;
                        }
                    }
                    // main to variable if necessary
                    if (variable_count == 2 && main_count == 1){
                        for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                            if (prerecipe__ingredient_array[i].main == true){
                                prerecipe__ingredient_array[i].main = false;
                                main_count--;
                                variable_count++;
                        }
                      }
                    }

                    //nefixních (počítaná + hlavní) > 4
                    if (variable_count + main_count > 4){
                        bootbox.alert("Příliš mnoho počítaných surovin - počítané suroviny musí být právě 3");
                        $(".recipe__loader").hide();

                        return false;
                    }
                    //počítaná > 3
                    if (variable_count > 3){
                        bootbox.alert("Příliš mnoho počítaných surovin - počítané suroviny musí být právě 3");
                        $(".recipe__loader").hide();
                        return false;
                    }
                    //málo počítaných surovin
                    if (variable_count + main_count < 3){
                        bootbox.alert("Příliš málo počítaných surovin - počítané suroviny musí být právě 3");
                        $(".recipe__loader").hide();
                        return false;
                    }

                    // values for fixed
                    for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                        if (prerecipe__ingredient_array[i].fixed) {
                            prerecipe__ingredient_array[i].amount = parseFloat(prompt("Množství suroviny " + prerecipe__ingredient_array[i].name + " v gramech :","").replace(",","."));
                        }
                    }

                    $.ajax({
                        type: 'POST',
                        url: "{{ url_for('RecipesView:calcRecipeAJAX') }}",
                        data: JSON.stringify({
                            'ingredients' : prerecipe__ingredient_array,
                            'dietID' : $('.select-diet').val(),
                            'trial' : '{{ is_trialrecipe|safe }}'
                        }),
                        contentType: 'application/json;charset=UTF-8',
                        success: function(response){
                            var ingredients = response.ingredients;
                            var template_data = response.template_data;
                            var diet = response.diet

                            if (response == "False"){
                                recipe__wrong__show();
                                return;
                            }
                            
                            // // empty recipe all
                            recipe__ingredient_array.empty();

                            // fill with html
                            $('#recipe__right').html(template_data);

                            var mySlider = $("#slider").slider();

                            // ingredients to inputs
                            for (let i = 0; i < ingredients.length; i++ ){
                                recipe__right__form__addIngredient(ingredients[i]);
                            }

                            // diet ID
                            recipe__ingredient_dietID = diet.id

                            // change visibility
                            recipe__right__show();

                        },
                        error: function(error) {
                            // console.log(error);
                        }
                    });
                    e.preventDefault();
                });


            /// Running loader animation
            $(document).on("click", ".prerecipe__calc__form__submit", function() {
                recipe__loader__show();
            });


            /// Recalculating amounts
            $(document).on("slideStop", "#slider", function(e) {
                recipe__loader__show();

                for (let i = 0; i < recipe__ingredient_array.length; i++) {
                    if (recipe__ingredient_array[i].main === true){
                        recipe__ingredient_array[i].amount = $('#slider').val();
                        recipe__ingredient_array[i].fixed = true;
                        recipe__ingredient_array[i].min = $('#slider')[0].dataset.sliderMin;
                        recipe__ingredient_array[i].max = $('#slider')[0].dataset.sliderMax;
                        break;
                    }
                }

                $.ajax({
                        type: 'POST',
                        url: "{{ url_for('RecipesView:calcRecipeAJAX') }}",
                        data: JSON.stringify({
                            'dietID'       : recipe__ingredient_dietID,
                            'ingredients'  : recipe__ingredient_array},
                            null, '\t'), // WIP not sure why
                        contentType: 'application/json;charset=UTF-8',

                        success: function(response) {
                            var ingredients = response.ingredients;
                            var template_data = response.template_data;

                            if (response == "False"){
                                recipe__wrong__show();
                                return;
                            }
                            
                            // // empty recipe all
                            recipe__ingredient_array.empty();

                            // fill with html
                            $('#recipe__right').html(template_data);

                            var mySlider = $("#slider").slider();

                            // ingredients to inputs
                            for (let i = 0; i < ingredients.length; i++ ){
                                recipe__right__form__addIngredient(ingredients[i]);
                            }

                            // diet ID
                            recipe__ingredient_dietID = response.diet.id

                            // change visibility
                            recipe__right__show();

                        },
                        error: function(error) {
                            console.log(error);
                        }

                    });
                    e.preventDefault();
            });

            function toggleFixedIngredient(id){
                for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                    if (prerecipe__ingredient_array[i].id == id) {
                        if (prerecipe__ingredient_array[i].fixed){
                            prerecipe__ingredient_array[i].fixed = false;
                            $('.prerecipe__selected-ingredients__table').find('tr[id_value = "' + id +'"] ').removeClass('tr-fixedIngredient');
                        } else {
                            prerecipe__ingredient_array[i].fixed = true;
                            prerecipe__ingredient_array[i].main = false;
                            $('.prerecipe__selected-ingredients__table').find('tr[id_value = "' + id +'"] ').addClass('tr-fixedIngredient');
                            $('.prerecipe__selected-ingredients__table').find('tr[id_value = "' + id +'"] ').removeClass('tr-mainIngredient');

                        }
                    }
                }
            }

            function trialSaveConfirm(){
                r = confirm("Pokud si chcete recept uložit, musíte se zaregistrovat")
                if (r == true){
                    var win = window.open('{{ url_for("RegisterView:show") }}');
                }
                return true;
            }
        </script>