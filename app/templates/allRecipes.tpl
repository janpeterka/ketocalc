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
            <div style="margin-left: 10px">
                <div class="row">
                    <a href="/newrecipe" target="_blank" style="margin-left: 3px"><button class="btn btn-secondary">Přidat recept</button></a>
                </div>

                <div class="row">
                    <form action="/printallrecipes" class="form-inline">
                        <input type="submit" class="btn btn-secondary" value="Vytisknout všechny recepty" />
                    </form>
                </div>
            </div>
            
        </div>    
    </div>
{% endblock %}

