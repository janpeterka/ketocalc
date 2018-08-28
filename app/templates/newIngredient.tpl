{% extends "base.tpl" %}
{% block title %}
    Nová surovina
{% endblock %}

{% block style %}
    
{% endblock %}

{% block script %}
	
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
        <div class="container">
            <form method="POST" action="/newingredient" class="form-group col-6" accept-charset="UTF-8">
                {{ form.csrf_token }}
                {% from "_formelement.tpl" import render_field %}
                {{ render_field(form.name, "form-control") }}
                {{ render_field(form.protein, "form-control") }}
                {{ render_field(form.fat, "form-control") }}
                {{ render_field(form.sugar, "form-control") }}
                {{ render_field(form.calorie, "form-control") }}
                {{ render_field(form.submit, "btn btn-primary col-sm-3", False) }}
            </form>
        </div>
{% endblock %}

