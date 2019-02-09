{% extends "base.tpl" %}
{% block title %}
    Feedback - Dejte nám vědět!
{% endblock %}

{% block style %}
    
{% endblock %}

{% block script %}
	
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
    <div class="container">
        <form action="/feedback" method="POST" class="form-group form-control" enctype="multipart/form-data">
            {{ form.csrf_token }}
            {% from "_formelement.tpl" import render_field %}
            {{ render_field(form.option, "form-control") }}
            {{ render_field(form.message, "form-control") }}
            {{ render_field(form.email, "form-control") }}
            {{ form.feedback_file(class_='form-control') }}
            {{ form.submit(class_='btn btn-primary col-sm-3') }}
        </form>
    </div>
{% endblock %}

