<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Registrace</title>
    % include('bootstrap.tpl') 
    % include('styleBody.tpl')
</head>
<body>
	<form action="./register" method="post" class="form-group col-sm-6">
            <label for="username">Přihlašovací jméno</label>
            <input name="username" type="text" class="form-control" />
            <label for="password">Heslo</label>
            <input name="password" type="password" class="form-control" />
            <label for="firstname">Jméno</label>
            <input name="firstname" type="text" class="form-control" />
            <label for="lastname">Příjmení</label>
            <input name="lastname" type="text" class="form-control" /> <br>
            <input value="Registrovat" type="submit" class="btn btn-primary"/>
        </form>
</body>
</html>