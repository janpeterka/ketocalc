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
                        <th>Bílkovina</th>
                        <th>Tuk</th>
                        <th>Sacharidy</th>
                    </tr>
                    <tr>
                        <td>{{diet.protein}}</td>
                        <td>{{diet.fat}}</td>
                        <td>{{diet.sugar}}</td>
                    </tr>
                </table>
            </div>     
            
        </div> 

        <form id="removeIngredient" action="/diet={{diet.id}}/remove" method="post" accept-charset="utf-8">
            <input id="ajaxButton" type="submit" class="btn btn-danger" value="Smazat dietu" />
        </form>

    </body>
</html>