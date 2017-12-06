<!DOCTYPE html>
<html>
    <head>
    	<meta charset="utf-8">
    	<meta http-equiv="X-UA-Compatible" content="IE=edge">
    	<title>Add new recipe</title>

        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
        <script type="text/javascript">
            $(document).ready(function() {
                $('form').submit(function(e) {
                    $.ajax({
                        type: 'POST',
                        url: '/addIngredientAJAX',
                        data: $(this).serialize(),
                        success: function(response) {
                            $('#selectedIngredients').append("<tr><td>" + response.id + "</td><td>" + response.name + "</td><td>" + response.sugar+ "</td><td>" + response.fat + "</td><td>" + response.protein + "</td></tr>");
                        },
                        error: function(error) {
                            console.log(error);
                        }

                    });
                    e.preventDefault();
                });
            });
            $(document).ready(function(){
                $('#calcRecipe').click(function(){
                    $.ajax({
                      type: 'POST',
                      url: '/calcRecipeAJAX',
                      success: function(data){
                        alert(data);
                      }
                    });
                });

            });
        </script>
    </head>
    <body>
        <form id="addIngredientForm" method="POST" action="/addIngredientAJAX">

            <select name="diet">
            %for diet in diets:
                <option value="{{diet.id}}">{{diet.name}}</option>
            %end
            </select><br>

            <select name="ingredient">
            %for ingredient in ingredients:
                <option value="{{ingredient[0]}}">{{ingredient[1]}}</option>
            %end
            </select>
            <input id="ajaxButton" type="submit" value="Add ingredient" />
        </form>

        <div id="selectedIngredientsDiv">
            <table id="selectedIngredients" style="width:50%; border: 1px solid black;">
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Sugar</th>
                    <th>Fat</th>
                    <th>Protein</th>
                </tr>
            </table>
            <input id="calcRecipe" type="submit" value="Calculate recipe" />
        </div>

    </body>
</html>

        