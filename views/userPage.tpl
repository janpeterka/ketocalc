<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Login to KetoCalc</title>
</head>
<body>
	hi {{username}} <br>
    <a href="/newdiet">Make new diet</a> <br>
    <a href="/newrecipe">Make new recipe</a> <br>

    <ul>
    %for recipe in recipes:
        <li><a href="/recipe={{recipe}}">{{recipe}}</a></li>
    %end
    </ul>

</body>
</html>