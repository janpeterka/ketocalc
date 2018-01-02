<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Recept</title>
    % include('bootstrap.tpl')
    % include('styleBody.tpl')

</head>
<body>
    % include('navbar.tpl')
    <div class="col-6">
        <span>{{recipe.name}}</span>
        <table id="ingredients" class="table">
            <tr>
                <th>Název</th>
                <th>Bílkovina</th>
                <th>Tuk</th>
                <th>Sacharidy</th>
                <th>Množství</th>
            </tr>
            % for ingredient in ingredients:
                <tr>
                    <td>
                        <a href="/ingredient={{ingredient.id}}">{{ingredient.name}}</a>
                    </td>
                    <td>{{ingredient.protein}}</td>
                    <td>{{ingredient.fat}}</td>
                    <td>{{ingredient.sugar}}</td>
                    <td>{{ingredient.amount}}</td>
                </tr>
            % end     
        </table>

        <form id="removeRecipe" action="/recipe={{recipe.id}}/remove" method="post" accept-charset="utf-8">
            <input id="ajaxButton" type="submit" class="btn btn-danger" value="Smazat recept" />
        </form>
    </div>


</body>
</html>