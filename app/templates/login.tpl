{% extends "base.tpl" %}
{% block title %}
    Přihlašování
{% endblock %}

{% block style %}
    
{% endblock %}

{% block script %}

{% endblock %}

{% block content %}
    {% include('navbar_login.tpl') %}
    <div class="container">
    	<div class="col-12">
    		<form action="/login" method="post" class="form-group form-control" >
                {{ form.csrf_token }}
                {% from "_formelement.tpl" import render_field %}
                {{ render_field(form.username, "form-control") }}
                {{ render_field(form.password, "form-control") }}
                {{ render_field(form.submit, "btn btn-primary col-sm-3", False) }}
            	<a class="col-sm-2" href="/register">Registrovat</a>
    	    </form>
    	</div>
    </div>
{% endblock %}

