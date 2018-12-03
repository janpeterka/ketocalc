{% extends "base.tpl" %}
{% block title %}
    Všechny recepty
{% endblock %}

{% block style %}{% endblock %}

{% block script %}{% endblock %}

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
                    <a href="/newrecipe" target="_blank"><button class="btn">Přidat recept</button></button>
                </form>
                <form action="/printallrecipes" class="form-inline">
                    <input type="submit" class="btn" value="Vytisknout všechny recepty" />
                </form>
            </div>
        </div>    
    </div>
{% endblock %}

