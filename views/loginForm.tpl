<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Login to KetoCalc</title>
	% include('bootstrap.tpl')
	% include('styleBody.tpl')
</head>
<body>
	<div class="col-sm-6">
		<form action="./login" method="post" class="form-group" >
	        <label for="username">Přihlašovací email</label>
	        <input name="username" type="text" class="form-control" />

	        <label for="password">Heslo</label>
	        <input name="password" type="password" class="form-control" />

	        	<input value="Login" type="submit" class="btn btn-primary col-sm-3" />
        	<a class="col-sm-2" href="/register">Registrovat</a>
	    </form>
	    
	</div>
</body>
</html>