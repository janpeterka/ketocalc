{% extends "base.tpl" %}
{% block title %}
    {{ texts.ingredient_all }}	
{% endblock %}

{% block style %}
{% endblock %}

{% block script %}
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
    <div class="container">
        <div class="col-12">
            <table id="ingredients" class="table">
                <tr>
                    <th>{{ texts.title }}</th>
                    <th>{{ texts.energy_100 }}</th>
                    <th>{{ texts.protein_100 }}</th>
                    <th>{{ texts.fat_100 }}</th>       
                    <th>{{ texts.sugar_100 }}</th>
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
            <a href="/newingredient" target="_blank"><button class="btn btn-secondary" style="margin-left: 5px">{{ texts.ingredient_add }}</button></a>
        </div> 
    </div>
{% endblock %}
