{% extends "base.tpl" %}
{% block title %}
    Něco se nepovedlo
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
    .main{
        margin-left: auto;
        margin-right: auto;
        margin-top: 20px;
    }
    </style>    
{% endblock %}

{% block script %}

{% endblock %}

{% block content %}
    {# {% include('navbar.tpl') %} #}
    <div class="container">
    	<div class="col-12 main">
    		<h1>Něco se nepovedlo.</h1>
            <a href="/feedback">Napište mi</a> a já to zkusím rychle opravit.
            <p>Zatím se můžete vrátit na <a href="/">hlavní stránku</a></p>
    	</div>
    </div>
{% endblock %}

