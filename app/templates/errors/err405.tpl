{% extends "base.html.j2" %}
{% block title %}
    Tady nemáte co pohledávat
{% endblock %}

{% block style %}{% endblock %}

{% block script %}{% endblock %}

{% block navbar %}
    {% include('navbar_empty.tpl') %}
{% endblock %}

{% block content %}
    <div class="container error_main">
        <h1>Na této stránce byste neměli být</h1>
        Radši se vraťte na <a href="{{ url_for('IndexView:index)') }}">hlavní stránku</a>
    </div>
{% endblock %}

