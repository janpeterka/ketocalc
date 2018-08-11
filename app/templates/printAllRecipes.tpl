{% extends "base.tpl" %}
{% block title %}
    Vytisknout všechny recepty
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
		.totals {
			background-color: var(--bgcolor-totals);
		}      

		@media print {
			body {-webkit-print-color-adjust: exact;}
			.totals {
				background-color: var(--bgcolor-totals);
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
                {% if recipe.size == "small" %}
                    <h5>Malé jídlo ({{ recipe.diet.small_size }}%)</h5>
                {% elif recipe.size == "big" %}
                    <h5>Velké jídlo ({{ recipe.diet.big_size }}%)</h5> 
                {% endif %}
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
                            <td>{{ ingredient.protein|round(2,'common') }} g</td>
                            <td>{{ ingredient.fat|round(2,'common') }} g</td>
                            <td>{{ ingredient.sugar|round(2,'common') }} g</td>
                            <td>{{ ingredient.amount|round(2,'common') }} g</td>
                            <td></td>
                        </tr>
                    {% endfor %}

                    <tr class="totals">
                        <td><strong>Celkem</strong></td>
                        <td>{{ recipe.totals.protein|round(2,'common') }}</td>
                        <td>{{ recipe.totals.fat|round(2,'common') }}</td>
                        <td>{{ recipe.totals.sugar|round(2,'common') }}</td>
                        <td>{{ recipe.totals.amount|round(2,'common') }} g</td>
                        <td>{{ recipe.totals.ratio }} : 1</td>
                    </tr>

                </table>
            {% endfor %}
        </div>
    </div>
{% endblock %}

