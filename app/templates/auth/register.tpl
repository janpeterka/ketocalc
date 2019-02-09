{% extends "base.tpl" %}
{% block title %}
    Registrace
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
    .warning{
        color : var(--color_warning);
    }
    </style>
    
{% endblock %}

{% block script %}
    <script>
        function toggleVisibility() {
            var x = $('#password')
            // console.log(x.attr("type"));
            if (x.attr("type") === "password"){
                x.attr("type", 'text');
            } else {
                x.attr("type", 'password');
            }
        }
    </script>
{% endblock %}

{% block content %}
    {% include('navbar_login.tpl') %}
    <div class="container">
        <div class="col-12">
           <form action="/register" method="post" class="form-group form-control" accept-charset="UTF-8">
                {{ form.csrf_token }}
                {% from "_formelement.tpl" import render_field %}

                {{ render_field(form.username, "form-control") }}
                {{ form.password.label }}
                <div class="form-row">
                    <div class="col-10">
                        {{ form.password(class_="form-control") }} 
                    </div>
                    <div class="col-2">
                        <input type="button" class="btn" onclick="toggleVisibility()" value="{{ texts.password_show}}">
                    </div>
                </div>

                <div class="form-row">
                    <div class="col">
                        {{ render_field(form.first_name, "form-control") }}
                    </div>
                    
                    <div class="col">
                        {{ render_field(form.last_name, "form-control") }}
                    </div>
                </div>
                <!-- {{ form.recaptcha }} -->
                {{ form.submit(class_='btn btn-primary')}}

                <a class="col-sm-2" href="/login">{{ texts.login }}</a><br>
            </form>
        </div>
    </div>
{% endblock %}

