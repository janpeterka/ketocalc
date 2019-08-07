{% extends "base.html.j2" %}
{% block title %}
    Registrace
{% endblock %}

{% block script %}
    <script type="text/javascript" src="{{ url_for('static', filename='toggle_visibility.js') }}"></script>
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

                {{ render_field(form.username, class="form-control") }}
                {{ form.password.label }}
                <div class="form-group">
                    {{ render_field(form.password, class="form-control", label=False)}}
                    <span class="fa fa-fw fa-eye field-icon" onmouseover="turnOnVisibility()", onmouseout="turnOffVisibility()"></span>
                </div>

                <div class="form-row">
                    <div class="col">
                        {{ render_field(form.first_name, class="form-control") }}
                    </div>
                    
                    <div class="col">
                        {{ render_field(form.last_name, class="form-control") }}
                    </div>
                </div>
                {{ render_field(form.recaptcha) }}
                {{ form.submit(class_='btn btn-primary')}}

                <a class="col-sm-2" href="/login">{{ texts.login }}</a><br>
            </form>
        </div>
    </div>
{% endblock %}

