{% extends "base.tpl" %}
{% block title %}
    Všechny suroviny	
{% endblock %}

{% block style %}
    
{% endblock %}

{% block script %}
	<script>
        $(document).on("click", ".newIngredient", function() {
            var win = window.open('/newingredient');
            win.focus();
        });
    </script>
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
    <div class="container">
        <div class="col-6">
            <table id="ingredients" class="table">
                <tr>
                    <th>Název</th>
                    <th>Kalorie</th>
                    <th>Bílkovina</th>
                    <th>Tuk</th>
                    <th>Sacharidy</th>
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
            <button class="newIngredient btn">Přidat surovinu</button>
        </div> 
    </div>
{% endblock %}

