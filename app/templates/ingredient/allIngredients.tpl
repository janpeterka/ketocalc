{% extends "base.tpl" %}
{% block title %}
    Všechny suroviny	
{% endblock %}

{% block style %}
{% endblock %}

{% block script %}
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
    <div class="container">
        <div class="col-10">
            <table id="ingredients" class="table">
                <tr>
                    <th>Název</th>
                    <th>Energie (kJ)</th>
                    <th>Bílkovina (g/100g)</th>
                    <th>Tuk (g/100g)</th>       
                    <th>Sacharidy (g/100g)</th>
                </tr>
                {% for ingredient in ingredients: %}
                    <tr>
                        <td><a href="/ingredient={{ingredient.id}}">{{ ingredient.name }}</a></td>
                        <td>{{ ingredient.calorie }}</td>
                        <td>{{ ingredient.protein }}</td>
                        <td>{{ ingredient.fat }}</td>
                        <td>{{ ingredient.sugar }}</td>
                    </tr>
                {% endfor %}
            </table>
            <a href="/newingredient" target="_blank"><button class="btn btn-secondary" style="margin-left: 5px">Přidat surovinu</button></a>
        </div> 
    </div>
{% endblock %}

