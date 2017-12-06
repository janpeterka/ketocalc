<!DOCTYPE html>
<html>
    <head>
    	<meta charset="utf-8">
    	<meta http-equiv="X-UA-Compatible" content="IE=edge">
    	<title>Add new ingredient</title>
    </head>
    <body>
        <form id="newIngredientForm" method="POST" action="/addDietAJAX">
            <label><input type="text" name="name"/>Název</label><br>
            <label><input type="number" name="sugar" step="0.01"/>Cukr / jídlo</label><br>
            <label><input type="number" name="fat" step="0.01"/>Tuk / jídlo</label><br>
            <label><input type="number" name="protein" step="0.01"/>Bílkovina / jídlo</label><br>
            <input id="ajaxButton" type="submit" value="Add diet" />
        </form>

    </body>
</html>

        