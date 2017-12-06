<!DOCTYPE html>
<html>
    <head>
    	<meta charset="utf-8">
    	<meta http-equiv="X-UA-Compatible" content="IE=edge">
    	<title>Add new ingredient</title>
    </head>
    <body>
        <form id="newIngredientForm" method="POST" action="/newIngredientAJAX">
            <label><input type="text" name="name"/>Název</label><br>
            <label><input type="number" name="sugar" step="0.01"/>Cukr</label><br>
            <label><input type="number" name="fat" step="0.01"/>Tuk</label><br>
            <label><input type="number" name="protein" step="0.01"/>Bílkovina</label><br>
            <input id="ajaxButton" type="submit" value="Add ingredient" />
        </form>

        <!-- <div id="selectedIngredientsDiv">
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
        </div> -->

    </body>
</html>

        