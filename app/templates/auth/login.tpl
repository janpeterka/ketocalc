{% extends "base.tpl" %}
{% block title %}
    Přihlašování
{% endblock %}

{% block style %}{% endblock %}
{% block script %}
    <script>
        function toggleVisibility() {
            var x = $('#password')
            if (x.attr("type") === "password"){
                x.attr("type", 'text');
            } else {
                x.attr("type", 'password');
            }
        }
    </script>
{% endblock %}

{% block content %}
    {% include('navbar_login.tpl') %}
    <div class="container">
    	<div class="col-12">
    		<form action="/login" method="post" class="form-group form-control" >
                {{ form.csrf_token }}
                {% from "_formelement.tpl" import render_field %}
                {{ render_field(form.username, "form-control") }}
                {{form.password.label}}
                <div class="form-row">
                    <div class="col-10">
                        {{ form.password(class_="form-control") }} 
                    </div>
                    <div class="col-2">
                        <input type="button" class="btn" onclick="toggleVisibility()" value="{{ texts.password_show }}">
                    </div>
                </div>
                {{ form.submit(class_='btn btn-primary col-sm-3') }}
               <a href="{{ url_for('google.login')}}""><button type="button" class="loginBtn loginBtn--google">{{ texts.login_google}}</button></a>
                <a class="col-sm-2" href="/register">{{ texts.register }}</a>
    	    </form>
    	</div>
    </div>
{% endblock %}

