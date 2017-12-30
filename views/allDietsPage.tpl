<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Všechny diety</title>
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
                <th>Sacharidy</th>
                <th>Tuk</th>
                <th>Bílkovina</th>
            </tr>
            %for diet in diets:
                <tr>
                    <td><a href="/diet={{diet.id}}">{{diet.name}}</a></td>
                    <td>{{diet.sugar}}</td>
                    <td>{{diet.fat}}</td>
                    <td>{{diet.protein}}</td>
                </tr>
            %end
        </table>
    </div>    
</body>
</html>