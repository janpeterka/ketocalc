{% extends "base.tpl" %}
{% block title %}
    Tato stránka neexistuje
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
    .main{
        margin-left: auto;
        margin-right: auto;
        margin-top: 20px;
    }
    </style>
{% endblock %}

{% block script %}

{% endblock %}

{% block content %}
    {# {% include('navbar_login.tpl') %} #}
    <div class="container">
        <div class="col-12 main">
            <table>
            <td class="col-2"></td>

            <td class="col-8">
            	<h1>Tato stránka neexistuje.</h1>
                Jste si jistí, že jste chtěli být tady? Pokud ano, <a href="/feedback">napište mi</a> a já to zkusím rychle opravit.
                <p>Zatím se můžete vrátit na <a href="/">hlavní stránku</a></p>
            </td>

            <td class="col-2"></td>
            </table>
        </div>  
    </div>
{% endblock %}

