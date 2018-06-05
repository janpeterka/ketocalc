{% extends "base.tpl" %}
{% block title %}
    Registrace
{% endblock %}

{% block style %}
    
{% endblock %}

{% block script %}
	<script type="text/javascript">
        $(document).on("change","#username", function(e) {
            $.ajax({
                type: 'POST',
                url: '/registerValidate',
                data: $(this).serialize(),
                success: function(response) {
                    if (response=="True") {
                        $("#wrongUsername").empty();
                    } else if (response=="False") {
                        $("#wrongUsername").empty();
                        $("#wrongUsername").append("<small class='form-text'>Jméno nemůžete použít!</small>");
                        // alert(response);
                    } else {
                    	continue;
                    }
                },
                error: function(error) {
                    console.log(error);
                }
            });
            e.preventDefault();
        });
        $(document).on('blur','#password',function(){
            if ($(this).val().length > 8){
                $("#wrongPassword").empty();
            } else {
                $("#wrongPassword").empty();
                $("#wrongPassword").append("<small class='form-text'>Heslo je příliš krátké!</small>");
            }

        });
        $(document).on('blur','#againPassword',function(){
            if ($(this).val() === $("#password").val()){
                $("#diffPassword").empty();
            } else {
                $("#diffPassword").empty();
                $("#diffPassword").append("<small class='form-text'>Hesla jsou rozdílná!</small>");
            }
        });
    </script>
{% endblock %}

{% block content %}
    {% include('navbar_login.tpl') %}
    <div class="container">
    	<form id="registerForm" action="/register" method="post" class="col-sm-6">

                <label for="username">Přihlašovací email</label>
                <input id="username" name="username" type="email" class="form-control" required value={{username}} >
                <span id=wrongUsername></span>

                <label for="password">Heslo (alespoň 8 znaků)</label>
                <input id="password" name="password" type="password" class="form-control" required />
                <span id=wrongPassword></span>

                <label for="password">Heslo znovu</label>
                <input id="againPassword" name="againPassword" type="password" class="form-control" required />
                <span id=diffPassword></span>

                <div class="form-row">

                    <div class="col">
                        <label for="firstname">Jméno</label>
                        <input name="firstname" type="text" class="form-control" required value={{firstname}} >
                    </div>
                    
                    <div class="col">
                        <label for="lastname">Příjmení</label>
                        <input name="lastname" type="text" class="form-control" required value={{lastname}} > <br>
                    </div>

                </div>

                <input id="registerButton" value="Registrovat" type="submit" class="btn btn-primary" />
                <a class="col-sm-2" href="/login">Přihlásit se</a><br>
            </form>
    </div>
{% endblock %}
