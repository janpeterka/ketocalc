<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Všechny recepty</title>
    % include('bootstrap.tpl')
    % include('styleBody.tpl')        
    </script>
</head>
<body>
    % include('navbar.tpl')
    <div class="col-6">
        <table id="diets" class="table">
            <tr>
                <th>Název</th>
                <th>Dieta</th>
            </tr>
            %for recipe in recipes:
                <tr>
                    <td><a href="/recipe={{recipe.id}}">{{recipe.name}}</a></td>
                    <td><a href="/diet={{recipe.dietID}}">{{recipe.dietName}}</a></td>
                </tr>
            %end
        </table>
    </div>    
</body>
</html>