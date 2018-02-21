{% extends "base.tpl" %}
{% block title %}
    Vytisknout všechny recepty
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
		.totals {
			background-color: lightgrey;
		}      

		@media print {
			body {-webkit-print-color-adjust: exact;}
			.totals {
				background-color: lightgrey;
			}
		}
    </style>
{% endblock %}

{% block script %}
	
{% endblock %}

{% block content %}
    <div class="container">
        <div class="col-12 d-print-flex">
            {% for recipe in recipes:%}
                <h2>{{ recipe.name }}</h2>   
                <table id="ingredients" class="table">
                    <tr>
                        <th><strong>Název</strong></th>
                        <th><strong>Bílkovina</strong></th>
                        <th><strong>Tuk</strong></th>
                        <th><strong>Sacharidy</strong></th>
                        <th><strong>Množství</strong></th>
                        <th></th>
                    </tr>


                    {% for ingredient in recipe.ingredients: %}
                        <tr>
                            <td><strong>{{ ingredient.name }}</strong></td>
                            <td>{{ ingredient.protein }} g</td>
                            <td>{{ ingredient.fat }} g</td>
                            <td>{{ ingredient.sugar }} g</td>
                            <td>{{ ingredient.amount}} g</td>
                            <td></td>
                        </tr>
                    {% endfor %}

                    <tr class="totals">
                        <td><strong>Celkem</strong></td>
                        <td>{{ recipe.totals.protein }}</td>
                        <td>{{ recipe.totals.fat }}</td>
                        <td>{{ recipe.totals.sugar }}</td>
                        <td>{{ recipe.totals.amount }} g</td>
                        <td>{{ recipe.totals.eq }} : 1</td>
                    </tr>

                </table>
            {% endfor %}
        </div>
    </div>
{% endblock %}

