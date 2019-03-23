{% extends "base.tpl" %}
{% block title %}
    Tady nemáte co pohledávat
{% endblock %}

{% block style %} 
{% endblock %}

{% block script %}
{% endblock %}

{% block content %}
    {% include('navbar_empty.tpl') %}
    <div class="container error_main">
        <h1>Na této stránce byste neměli být</h1>
        Radši se vraťte na <a href="/">hlavní stránku</a>
    </div>
{% endblock %}

