{% extends "base.tpl" %}
{% block title %}
    Něco se nepovedlo
{% endblock %}

{% block style %}{% endblock %}

{% block script %}{% endblock %}

{% block content %}
    {% include('navbar_empty.tpl') %}
    <div class="container error_main">
		<h1>Něco se nepovedlo.</h1>
        <a href="/feedback">Napište mi</a> a já to zkusím rychle opravit.
        <p>Zatím se můžete vrátit na <a href="/">hlavní stránku</a></p>
    </div>
{% endblock %}

