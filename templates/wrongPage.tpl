{% extends "base.tpl" %}
{% block title %}
    Tady nemáte co pohledávat
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
    {# {% include('navbar_login.tpl') %} #}
    <div class="container">
        <div class="main">
        	<h1>Na této stránce byste neměli být</h1>
            Radši se vraťte na <a href="/">hlavní stránku</a>
        </div>
    </div>
{% endblock %}

