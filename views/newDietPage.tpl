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
        % include('navbar.tpl')
        <form id="newDietForm" method="POST" action="/newdiet" class="form-group col-sm-5">
            <label for="name">Název diety</label>
            <input type="text" name="name" class="form-control"  value={{name}}>
            <label for="protein">Množství bílkovin / 1 jídlo</label>
            <input type="text" pattern="[0-9]+([\.,][0-9]+)?" name="protein" class="form-control" step="0.01" value={{protein}}><br>
            <label for="fat">Množství tuku / 1 jídlo</label>
            <input type="text" pattern="[0-9]+([\.,][0-9]+)?" name="fat" class="form-control" step="0.01" value={{fat}}>
            <label for="sugar">Množství sacharidů / 1 jídlo</label>
            <input type="text" pattern="[0-9]+([\.,][0-9]+)?" name="sugar" class="form-control" step="0.01" value={{sugar}}>
            <input id="ajaxButton" type="submit" class="btn btn-primary" value="Přidat dietu" /><br>
            <span id=genProblem class="problem">{{problem}}</span>

        </form>

    </body>
</html>

        