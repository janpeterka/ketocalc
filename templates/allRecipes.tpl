{% extends "base.tpl" %}
{% block title %}
    Všechny recepty
{% endblock %}

{% block style %}
    
{% endblock %}

{% block script %}
	<script>
        $(document).on("click", ".newRecipe", function() {
            var win = window.open('/newrecipe');
            win.focus();
        });
    </script>
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
    <div class="container">
        <div class="col-6">
            <table id="diets" class="table">
                <tr>
                    <th>Název</th>
                    <th>Dieta</th>
                </tr>
                {% for recipe in recipes: %}
                    <tr>
                        <td><a href="/recipe={{recipe.id}}">{{ recipe.name }}</a></td>
                        <td><a href="/diet={{recipe.dietID}}">{{ recipe.dietName }}</a></td>
                    </tr>
                {% endfor %}
            </table>
            <form action="/printallrecipes" class="form-inline">
                <button class="newRecipe btn">Přidat recept</button>    
                <input type="submit" class="btn" value="Vytisknout všechny recepty" />
            </form>
        </div>    
    </div>
{% endblock %}

