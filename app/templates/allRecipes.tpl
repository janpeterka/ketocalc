{% extends "base.tpl" %}
{% block title %}
    Všechny recepty
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
        .diet{
            background-color: #a4f442;
            margin-right: 0px;
            padding-right: 0px;
        }
    </style>
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
        <div class="col-10">
            <table id="diets" class="table">

                {% for diet in diets: %}
                    <tr>
                        <th class='diet'><a href="/diet={{diet.id}}">{{ diet.name }}</a></th>
                    </tr>

                    {% for recipe in diet.recipes: %}
                        <tr>
                            <td><a href="/recipe={{recipe.id}}">{{ recipe.name }}</a></td>
                        </tr>
                    {% endfor %}
                {% endfor %}       

            </table>
            <div class="row">
                <form action="" class="form-inline">
                    <button class="newRecipe btn">Přidat recept</button>        
                </form>
                <form action="/printallrecipes" class="form-inline">
                    <input type="submit" class="btn" value="Vytisknout všechny recepty" />
                </form>
            </div>
        </div>    
    </div>
{% endblock %}

