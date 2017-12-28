<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Surovina</title>
    % include('bootstrap.tpl')
    % include('styleBody.tpl')

</head>
<body>
    % include('navbar.tpl')
    <div class="col-6">
        <span>{{ingredient.name}}</span>
        <table id="ingredients" class="table">
            <tr>
                <th>ID</th>
                <th>Název</th>
                <th>Sacharidy</th>
                <th>Tuk</th>
                <th>Bílkovina</th>
            </tr>
            <tr>
                <td>{{ingredient.id}}</td>
                <td>{{ingredient.name}}</td>
                <td>{{ingredient.sugar}}</td>
                <td>{{ingredient.fat}}</td>
                <td>{{ingredient.protein}}</td>
            </tr>    
        </table>

        <form id="removeIngredient" action="/ingredient={{ingredient.id}}/remove" method="post" accept-charset="utf-8">
            <input id="ajaxButton" type="submit" class="btn btn-danger" value="Smazat surovinu" />
        </form>
    </div>


</body>
</html>