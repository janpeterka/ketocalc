<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Vítejte {{username}}</title>
    % include('bootstrap.tpl')
    % include('styleBody.tpl')
</head>
<body>
    
    <div>
        <a href="/newdiet">Make new diet</a> <br>
        <a href="/newrecipe">Make new recipe</a> <br>
    </div>


    <div>
        Seznam receptů:
        <ul>
        %for recipe in recipes:
            <li><a href="/recipe={{recipe.id}}">{{recipe.name}}</a></li>
        %end
        </ul>
    </div>
</body>
</html>