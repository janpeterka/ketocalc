<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Dieta: {{diet.name}}</title>
    % include('bootstrap.tpl')
    % include('styleBody.tpl')
</head>
<body>
    % include('navbar.tpl')

    <div class="container row">
         <div class="col-8">
            <label for="recipes">Recepty</label>
            <ul name="recipes">
            % for recipe in recipes:
                    <li><a href="/recipe={{recipe.id}}">{{recipe.name}}</a></li>
            % end 
            </ul>
        </div>  
        <div class="col-4">
            <table id="ingredients" class="table">
                <tr>
                    <th>Sacharidy</th>
                    <th>Tuk</th>
                    <th>Bílkovina</th>
                </tr>
                <tr>
                    <td>{{diet.sugar}}</td>
                    <td>{{diet.fat}}</td>
                    <td>{{diet.protein}}</td>
                </tr>
            </table>
        </div>     
        
    </div> 

</body>
</html>