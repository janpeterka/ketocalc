{% extends "base.html.j2" %}
{% block title %}
    Plánovaná odstávka
{% endblock %}

{% block style %}{% endblock %}

{% block script %}{% endblock %}

{% block navbar %}
    {% include('navbar_empty.tpl') %}
{% endblock %}

{% block content %}
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

