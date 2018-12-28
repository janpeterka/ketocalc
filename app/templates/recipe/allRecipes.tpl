{% extends "base.tpl" %}
{% block title %}
    Všechny recepty
{% endblock %}

{% block style %}{% endblock %}
<!-- <style type="text/css">  
    .btn{
        margin-top: 5px;
    }
</style> -->

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
            <div style="margin-left: 15px">
                <div class="row">
                    <a href="/newrecipe" target="_blank" class="btn btn-secondary">Přidat recept</a>
                </div>

                <div class="row" style="margin-top: 5px">
                    <a href="/printallrecipes" target="_black" class="btn btn-secondary"> Vytisknout všechny recepty {{ icons.print }}</a>
<!--                     <form action="/printallrecipes" class="form-inline">
                        <input type="submit" class="btn btn-secondary" value="Vytisknout všechny recepty" />
                    </form> -->
                </div>
            </div>
            
        </div>    
    </div>
{% endblock %}

