{% extends "base.tpl" %}
{% block title %}
    Plánovaná odstávka
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
    {% include('navbar_empty.tpl') %}
    <div class="container">
        <div class="col-12 main">
            <table>
            <td class="col-2"></td>

            <td class="col-8">
            	<h1>Web je v dočasně mimo provoz</h1>
                Můžete zatím použít <a href="ketocalc.herokuapp.com">starou verzi aplikace</a> - své recepty tam najdete. <br>
                Odstávka by neměla trvat déle než 24 hodin.
            </td>

            <td class="col-2"></td>
            </table>
        </div>  
    </div>
{% endblock %}

