{% extends "base.tpl" %}
{% block title %}
    Vytisknout recept - {{ recipe.name }}
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

            <span class="data__table d-print-table"><h2>{{ recipe.name }}</h2></span>            
            <table id="ingredients" class="table">
                <tr>
                    <th><strong>Název</strong></th>
                    <th><strong>Bílkovina</strong></th>
                    <th><strong>Tuk</strong></th>
                    <th><strong>Sacharidy</strong></th>
                    <th><strong>Množství</strong></th>
                    <th></th>
                </tr>

                {% for ingredient in ingredients: %}
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
                    <td>{{ totals.protein }}</td>
                    <td>{{ totals.fat }}</td>
                    <td>{{ totals.sugar }}</td>
                    <td>{{ totals.amount }} g</td>
                    <td>{{ totals.eq }} : 1</td>
                </tr>
            </table>
            </div>
        </div>
    </div>
{% endblock %}

