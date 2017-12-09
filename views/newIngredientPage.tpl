<!DOCTYPE html>
<html>
    <head>
    	<meta charset="utf-8">
    	<meta http-equiv="X-UA-Compatible" content="IE=edge">
    	<title>Nová surovina</title>
        % include('bootstrap.tpl')
        % include('styleBody.tpl')
    </head>
    <body>
        <form id="newIngredientForm" method="POST" action="/newIngredientAJAX" class="form-group col-sm-4">

            <label for="name">Název suroviny</label>
            <input type="text" name="name" class="form-control" />
            <label for="sugar">Množství cukru / 100 g</label>
            <input type="number" name="sugar" class="form-control" step="0.01"/>
            <label for="fat">Množství tuku / 100 g</label>
            <input type="number" name="fat" class="form-control" step="0.01"/>
            <label for="protein">Množství bílkovin / 100 g</label>
            <input type="number" name="protein" class="form-control" step="0.01"/><br>
            <input id="ajaxButton" type="submit" class="btn btn-primary" value="Přidat surovinu" />
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

        