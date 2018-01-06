<!DOCTYPE html>
<html>
    <head>
    	<meta charset="utf-8">
    	<meta http-equiv="X-UA-Compatible" content="IE=edge">
    	<title>Nový recept</title>

        % include('bootstrap.tpl') 
        % include('styleBody.tpl')

        <script type="text/javascript">

            // On ready - change visibility to default
            $(document).ready(function() {
                selectAllIngredients = String(document.getElementById("ingredientSelect").innerHTML);
                // $("#addRecipe").css('visibility', 'hidden');
                $("#right").css('visibility', 'hidden');
                $("#wrong").css('visibility', 'hidden');
                $(".loader").css('visibility', 'hidden');
            });

            $(function(){
                  $('#selectedIngredients').on('click','tr button.remove',function(e){
                     e.preventDefault();
                    $(this).parents('tr').remove();

                    temp_id = $(this).attr('id');
                    temp_array=$('#ingredientsArray').val().split(", ");
                    temp_array.splice($.inArray(temp_id, temp_array),1);


                    $('#ingredientsArray').val("");
                    for (let i = 0; i < temp_array.length; i++) {
                        temp_val = $('#ingredientsArray').val();
                        if (temp_val === "") {
                            $('#ingredientsArray').val(temp_array[i]);
                        }else{
                            $('#ingredientsArray').val(temp_val + ", " + temp_array[i]);
                        }
                    }
                    // console.log($('#ingredientsArray').val());

                    // Restore default options
                    $('#ingredientSelect').empty();
                    $('#ingredientSelect').append(selectAllIngredients);


                    console.log($('#ingredientSelect'));
                    // Remove used options
                    for (let j = 0; j < temp_array.length; j++) {
                        console.log(temp_array[j]);
                        $('#ingredientSelect option[value="' + temp_array[j] + '"]').remove(); // wip
                    }

                    

                  });
            });

            $(document).on("submit", "#addIngredientForm", function(e) {
                    $.ajax({
                        type: 'POST',
                        url: '/addIngredientAJAX',
                        data: $(this).serialize(),
                        success: function(response) {
                            $("#ingredientSelect option[value='"+response.id+"']").remove();
                            $('#selectedIngredients').append("<tr><td>" + response.id + "</td><td>" + response.name + "</td><td>" + response.protein+ "</td><td>" + response.fat + "</td><td>" + response.sugar + "</td><td>" + '<button id="' + response.id + '" class="remove btn btn-warning">Ubrat</button>' + "</td></tr>");
                            // console.log($('#selectedIngredients').val());
                            var temp_array = $('#ingredientsArray').val();
                            if (temp_array.length === 0) {
                                $('#ingredientsArray').val(response.id);
                            } else {
                                $('#ingredientsArray').val(temp_array + ", " + response.id);
                            }

                            // $("#addRecipe").css('visibility', 'hidden');
                            $("#right").css('visibility', 'hidden');
                            $("#wrong").css('visibility', 'hidden');
                            $(".loader").css('visibility', 'hidden');
                            
                        },
                        error: function(error) {
                            console.log(error);
                        }

                    });
                    e.preventDefault();
            });

            $(document).on("click", "#calcRecipe", function() {
                $(".loader").css('visibility', 'visible');
            });

            $(document).on("submit", "#calcRecipeForm", function(e) {
                    $.ajax({
                        type: 'POST',
                        url: '/calcRecipeAJAX',
                        data: $(this).serialize(),
                        success: function(response){

                            $('#ingredientsArray').val("");
                            $('#selectedIngredients').empty();
                            $('#selectedIngredients').append('<tr><th>Název</th><th>Bílkovina</th><th>Tuk</th><th>Sacharidy</th></tr>');

                            $('#ingredientSelect').empty();
                            $('#ingredientSelect').append(selectAllIngredients);

                            $('#selectedIngredientsAdd').empty();
                            $("#selectedIngredientsAdd").append('<tr><th>Název</th><th>Bílkovina</th><th>Tuk</th><th>Sacharidy</th></tr>');


                            if (response=="False"){
                                console.log("False");
                                // $("#addRecipe").css('visibility', 'visible');
                                $(".loader").css('visibility', 'hidden');
                                $("#right").css('visibility', 'hidden');
                                $("#wrong").css('visibility', 'visible');

                                return;
                            }
                            totalSugar = 0;
                            totalFat = 0;
                            totalProtein = 0;
                            var ingredients = response.array;
                            // ingredients to table
                            for (i = 0; i<response.array.length; i++ ){
                                $('#selectedIngredientsAdd').append("<tr><td>" + ingredients[i].name + "</td><td>" + ingredients[i].protein+ "</td><td>" + ingredients[i].fat + "</td><td>" + ingredients[i].sugar + "</td><td>" + Math.round(ingredients[i].amount*100)+ " g</td></tr>");  // wip
                                totalSugar += ingredients[i].sugar*ingredients[i].amount;
                                totalFat += ingredients[i].fat*ingredients[i].amount;
                                totalProtein += ingredients[i].protein*ingredients[i].amount;
                            }
                            

                            // $('#selectedIngredientsAdd').append("<tr><td>" + "-" + "</td><td>" + "Součty" + "</td><td>" + totalProtein+ "</td><td>" + totalFat + "</td><td>" + totalSugar+ "</td><td>" + "-" + "</td></tr>");


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
                                    $('#ingredientsAmount2').val(Math.round(ingredients[i].amount*100));
                                } else {
                                    $('#ingredientsAmount2').val(temp_array2 + ", " + Math.round(ingredients[i].amount*100));
                                }
                            }

                            // diet ID
                            $('#selectedDietID').val(response.dietID);

                            // change visibility
                            // $("#addRecipe").css('visibility', 'visible');
                            $(".loader").css('visibility', 'hidden');
                            $("#wrong").css('visibility', 'hidden');
                            $("#right").css('visibility', 'visible');

                        },
                        error: function(error) {
                            console.log(error);
                        }
                    });
                    e.preventDefault();
                });
        </script>
        
        <style type="text/css" media="screen">
            #wrong{
                visibility: hidden;
            }

            #right{
                visibility: hidden;
            }

            .loader {
                visibility: hidden;
                border: 16px solid #f3f3f3; /* Light grey */
                border-top: 16px solid #337ab7; /* Blue */
                border-radius: 50%;
                width: 120px;
                height: 120px;
                animation: spin 2s linear infinite;
                margin: 40px auto;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        % include('navbar.tpl')
        <div class="container row">
            <div class="col-md-7" style="margin-top: 40px">

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
                            <th>Název</th>
                            <th>Bílkovina</th>
                            <th>Tuk</th>
                            <th>Sacharidy</th>
                            <th></th>
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


            <div class="col-md-5" id=addRecipe style="position: relative;">

                <div class="loader"></div>

                <div id="wrong" class="offset-md-6" style="position:absolute; top:0px;">
                    <span class="problem" style="text-align: center">Recept nelze vytvořit</span>
                </div>

                <div id="right" style="position:absolute; top:0px;">
                    <form id="addRecipeForm" method="POST" action="/saveRecipeAJAX" class="form-group">
                        <label for="recipeName">Název receptu</label>
                        <input type="text" name="recipeName" required class="form-control"/>
                        
                        <table id="selectedIngredientsAdd" class="table">
                            <tr>
                                <th>Název</th>
                                <th>Bílkovina</th>
                                <th>Tuk</th>
                                <th>Sacharidy</th>
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

            
        </div>
    </body>
</html>

        