<!DOCTYPE html>
<html>
    <head>
    	<meta charset="utf-8">
    	<meta http-equiv="X-UA-Compatible" content="IE=edge">
    	<title>Nový recept</title>

        % include('bootstrap.tpl') 
        % include('styleBody.tpl')

        <script type="text/javascript">
            $(document).on("submit", "#addIngredientForm", function(e) {
                    $.ajax({
                        type: 'POST',
                        url: '/addIngredientAJAX',
                        data: $(this).serialize(),
                        success: function(response) {
                            $('#selectedIngredients').append("<tr><td>" + response.id + "</td><td>" + response.name + "</td><td>" + response.sugar+ "</td><td>" + response.fat + "</td><td>" + response.protein + "</td></tr>");
                            // console.log($('#ingredientsArray').val());
                            var temp_array = $('#ingredientsArray').val();
                            if (temp_array.length === 0) {
                                $('#ingredientsArray').val(response.id);
                            } else {
                                $('#ingredientsArray').val(temp_array + ", " + response.id);
                            }

                            // remove option
                            $("#ingredientSelect option[value='"+response.id+"']").remove();

                        },
                        error: function(error) {
                            console.log(error);
                        }

                    });
                    e.preventDefault();
            });

            $(document).on("submit", "#calcRecipeForm", function(e) {
                    $.ajax({
                        type: 'POST',
                        url: '/calcRecipeAJAX',
                        data: $(this).serialize(),
                        success: function(response){
                            var ingredients = response.array;
                            // ingredients to table
                            for (i = 0; i<response.array.length; i++ ){
                                $('#selectedIngredientsAdd').append("<tr><td>" + ingredients[i].id + "</td><td>" + ingredients[i].name + "</td><td>" + ingredients[i].sugar+ "</td><td>" + ingredients[i].fat + "</td><td>" + ingredients[i].protein + "</td><td>" + ingredients[i].amount + "</td></tr>");
                            }

                            $('#ingredientsArray').val("");

                            // ingredient IDs
                            
                            for (i = 0; i<ingredients.length; i++ ){
                                var temp_array = $('#ingredientsArray2').val();
                                if (temp_array.length === 0) {
                                    $('#ingredientsArray2').val(ingredients[i].id);
                                } else {
                                    $('#ingredientsArray2').val(temp_array + ", " + ingredients[i].id);
                                }
                            }

                            // ingredient amounts
                            
                            for (i = 0; i<ingredients.length; i++ ){
                                var temp_array2 = $('#ingredientsAmount2').val();
                                if (temp_array2.length === 0) {
                                    $('#ingredientsAmount2').val(ingredients[i].amount);
                                } else {
                                    $('#ingredientsAmount2').val(temp_array2 + ", " + ingredients[i].amount);
                                }
                            }

                            // diet ID
                            $('#selectedDietID').val(response.dietID);

                            // change visibility
                            $("#addRecipe").css('visibility', 'visible');

                        },
                        error: function(error) {
                            console.log(error);
                        }
                    });
                    e.preventDefault();
                });

        </script>
        <style type="text/css" media="screen">

            #addRecipe{
                visibility: hidden;
            }
        </style>
    </head>
    <body>
        % include('navbar.tpl')
        <div class="container row">
            <div class="col">

                <div class="form-group col-sm-12">
                    <form id="addIngredientForm" method="POST" action="/addIngredientAJAX">
                        <select id="ingredientSelect" name="ingredient" class="form-control">
                        %for ingredient in ingredients:
                            <option name={{ingredient.name}} value="{{ingredient.id}}">{{ingredient.name}}</option>
                        %end
                        </select>
                        <input id="ajaxButton" type="submit" class="btn btn-primary" value="Přidat surovinu" />
                    </form>
                </div>
                

                <div id="selectedIngredientsDiv" class="col-sm-12">
                    <table id="selectedIngredients" class="table">
                        <tr>
                            <th>ID</th>
                            <th>Název</th>
                            <th>Cukr</th>
                            <th>Tuk</th>
                            <th>Bílkovina</th>
                        </tr>
                    </table>
                </div>

                <div class="col-sm-12">
                    <form id="calcRecipeForm" method="POST" class="form-group" action="/calcRecipeAJAX">
                        <label for="recipeDiet">Název diety</label>
                        <select name="recipeDiet" class="form-control">
                        %for diet in diets:
                            <option value="{{diet.id}}">{{diet.name}}</option>
                        %end
                        </select>
                        <input id="calcRecipe" type="submit" class="btn btn-primary" value="Spočítat množství!" />
                        <input type="hidden" id="ingredientsArray" name="ingredientsArray" value="" />
                    </form>
                </div>

            </div>


            <div class="col-md-4" id=addRecipe>
                <form id="addRecipeForm" method="POST" action="/saveRecipeAJAX" class="form-group">
                    <label for="recipeName">Název receptu</label>
                    <input type="text" name="recipeName" required class="form-control"/>
                    
                    <table id="selectedIngredientsAdd" class="table">
                        <tr>
                            <th>ID</th>
                            <th>Název</th>
                            <th>Cukr</th>
                            <th>Tuk</th>
                            <th>Bílkovina</th>
                            <th>Množství</th>
                        </tr>
                    </table>

                    <input id="addRecipeButton" type="submit" class="btn btn-primary" value="Uložit mezi recepty" />
                    
                    <input type="hidden" id="ingredientsArray2" name="ingredientsArray2" value="" />
                    <input type="hidden" id="selectedDietID" name="selectedDietID" value="" />
                    <input type="hidden" id="ingredientsAmount2" name="ingredientsAmount2" value="" />

                </form>
            </div>
        </div>

    </body>
</html>

        