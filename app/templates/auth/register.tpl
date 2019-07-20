{% extends "base.html.j2" %}
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
            if (x.attr("type") === "password"){
                x.attr("type", 'text');
            } else {
                x.attr("type", 'password');
            }
        }
    </script>
{% endblock %}

{% block content %}
    <div class="container">
        <div class="col-10">
           <form action="/register" method="post" class="form-group form-control" accept-charset="UTF-8">
                <div class="mx-auto" style="width: 200px;">
                    <a href="{{ url_for('google.login')}}" >
                        <button type="button" class="btn btn-social btn-google">
                            <span class="fab fa-google"></span> {{ texts.register_google }}
                        </button>
                    </a>
                    <p class="text-left" style="color:grey;">nebo</p>
                </div>
                
                <hr class="col-xs-12">

                {{ form.csrf_token }}
                {% from "_form_element.html.j2" import render_field %}

                {{ render_field(form.username, "form-control") }}
                {{ form.password.label }}
                <div class="form-row">
                    <div class="col-10">
                        {{ render_field(form.password(class_="form-control", label=False)) }} 
                    </div>
                    <div class="col-2">
                        <input type="button" class="btn" onclick="toggleVisibility()" value="{{ texts.password_show }}">
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
                {{ render_field(form.recaptcha) }}
                {{ form.submit(class_='btn btn-primary')}}

                <a class="col-sm-2" href="/login">{{ texts.login }}</a><br>
            </form>
        </div>
    </div>
{% endblock %}

