<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Všechny suroviny</title>
    % include('bootstrap.tpl')
    % include('styleBody.tpl')        
    </script>
</head>
<body>
    % include('navbar.tpl')
    <div class="col-6">
        <table id="ingredients" class="table">
            <tr>
                <th>Název</th>
                <th>Bílkovina</th>
                <th>Tuk</th>
                <th>Sacharidy</th>
            </tr>
            %for ingredient in ingredients:
                <tr>
                    <td><a href="/ingredient={{ingredient.id}}">{{ingredient.name}}</a></td>
                    <td>{{ingredient.protein}}</td>
                    <td>{{ingredient.fat}}</td>
                    <td>{{ingredient.sugar}}</td>
                </tr>
            %end
        </table>
    </div>    
</body>
</html>