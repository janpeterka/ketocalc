{% extends "base.html.j2" %}
{% block title %}
    Tato stránka neexistuje
{% endblock %}

{% block style %}{% endblock %}

{% block script %}{% endblock %}

{% block navbar %}
    {% include('navbar_empty.tpl') %}
{% endblock %}

{% block content %}
    <div class="container error_main">
    	<h1>Tato stránka neexistuje.</h1>
        Jste si jistí, že jste chtěli být tady? Pokud ano, <a href="{{ url_for('SupportView:feedback)')}}">napište mi</a> a já to zkusím rychle opravit.
        <p>Zatím se můžete vrátit na <a href="{{ url_for('IndexView:index)')}}">hlavní stránku</a></p>
    </div>
{% endblock %}

