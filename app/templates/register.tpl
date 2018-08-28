{% extends "base.tpl" %}
{% block title %}
    Registrace
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
    .warning{
        color : var(--color_warning);
    }
    </style>
    
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
                        console.log("Name ok")
                        $("#wrongUsername").empty();
                    } else if (response=="False") {
                        $("#wrongUsername").empty();
                        $("#wrongUsername").append("<small class='form-text'>Email nemůžete použít!</small>");
                    }
                },
                error: function(error) {
                    console.log(error);
                }
            });
            e.preventDefault();
        });
    </script>
{% endblock %}

{% block content %}
    {% include('navbar_login.tpl') %}
    <div class="container">
    	<form action="/register" method="post" class="form-group form-control col-sm-6" accept-charset="UTF-8">
                {{ form.csrf_token }}
                {% from "_formelement.tpl" import render_field %}

                {{ render_field(form.username, "form-control") }}
                {{ render_field(form.password, "form-control") }}
                {{ render_field(form.password_again, "form-control") }}

                <div class="form-row">

                    <div class="col">
                        {{ render_field(form.first_name, "form-control") }}
                    </div>
                    
                    <div class="col">
                        {{ render_field(form.last_name, "form-control") }}
                    </div>

                </div>
                {{ render_field(form.recaptcha) }}
                {{ render_field(form.submit, "btn btn-primary", False) }}

                <a class="col-sm-2" href="/login">Přihlásit se</a><br>
            </form>
    </div>
{% endblock %}

