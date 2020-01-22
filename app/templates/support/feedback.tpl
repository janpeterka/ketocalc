{% extends "base.html.j2" %}
{% block title %}
    Feedback - Dejte nám vědět!
{% endblock %}

{% block style %}{% endblock %}

{% block script %}{% endblock %}

{% block content %}
    <div class="container">
        <form action="{{ url_for('SupportView:feedback') }}" method="POST" class="form-group form-control" enctype="multipart/form-data">
            {{ form.csrf_token }}
            {% from "_form_element.html.j2" import render_field %}
            {{ render_field(form.option, "form-control") }}
            {{ render_field(form.message, "form-control") }}
            {{ render_field(form.email, "form-control") }}
            {{ form.feedback_file(class_='form-control') }}
            {{ form.submit(class_='btn btn-primary col-sm-3') }}
        </form>
        <span>nebo mi napište na <a href="mailto:ketocalc.jmp@gmail.com">e-mail</a></span>
    </div>
{% endblock %}

