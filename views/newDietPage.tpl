<!DOCTYPE html>
<html>
    <head>
    	<meta charset="utf-8">
    	<meta http-equiv="X-UA-Compatible" content="IE=edge">
    	<title>Nová dieta</title>
        % include('bootstrap.tpl')
        % include('styleBody.tpl')
    </head>
    <body>
        <form id="newIngredientForm" method="POST" action="/addDietAJAX" class="form-group col-sm-5">
            <label for="name">Název diety</label>
            <input type="text" name="name" class="form-control" />
            <label for="sugar">Množství cukru / 1 jídlo</label>
            <input type="number" name="sugar" class="form-control" step="0.01"/>
            <label for="fat">Množství tuku / 1 jídlo</label>
            <input type="number" name="fat" class="form-control" step="0.01"/>
            <label for="protein">Množství bílkovin / 1 jídlo</label>
            <input type="number" name="protein" class="form-control" step="0.01"/><br>
            <input id="ajaxButton" type="submit" class="btn btn-primary" value="Přidat dietu" />
        </form>

    </body>
</html>

        