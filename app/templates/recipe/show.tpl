{% extends "base.tpl" %}
{% block title %}
    {% if show %}
        {{ texts.recipe}}
    {% else %}
        {{ texts.recipe_print}} - {{ recipe.name }}
    {% endif %}
{% endblock %}
    
{% block style %}

    {% if show %}
        <style type="text/css" media="screen">
            .edit__form{
                display: none;
            }

            .editHideButton{
                display: none;
            }
        </style>
    {% else %}
        <style type="text/css" media="screen">
            .totals {
                background-color: var(--bgcolor_totals);
            }      

            @media print {
                body {-webkit-print-color-adjust: exact;}
                .totals {
                    background-color: var(--bgcolor_totals);
                }
            } 
        </style>
    {% endif %}
{% endblock %}

{% block script %}
    {% if show %}
	<script type="text/javascript">

            $(document).on("click", ".editShowButton", function() {
                $('.edit__form').show();
                $('.data__table').hide();
                $('.editShowButton').hide();
                $('.editHideButton').show();
            });

            $(document).on("click", ".editHideButton", function() {
                $('.edit__form').hide();
                $('.data__table').show();
                $('.editShowButton').show();
                $('.editHideButton').hide();
            });

            $(document).on("click", ".printButton", function() {
                var win = window.open(window.location.href + '/print');
                win.focus();
            });
    
        </script>
        {% endif %}
{% endblock %}

{% block content %}
    {% if show %}
        {% include('navbar.tpl') %}
    {% endif %}
    <div class="container">
        <div class="col-12">
            {% if show %}
            <form action="/recipe={{recipe.id}}/edit" class="form-inline edit__form" method="post" accept-charset="utf-8">
                <input type="text" name="name" class="form-control col-4" value="{{ recipe.name }}"><br>
                <select name="size" class="form-control">
                    <option value="small">{{ texts.meal_size_small }} ({{ recipe.diet.small_size }})</option>
                    <option value="big">{{ texts.meal_size_big }} ({{ recipe.diet.big_size }})</option>
                </select>
                <input type="submit" value="{{ texts.recipe_edit }}" class="btn btn-warning">
            </form>
            {% endif %}

            {% if show %}
                <span class="data__table">
            {% else %}
                <span class="data__table d-print-table">
            {% endif %}

                <h2>{{ recipe.name }}</h2>

            {% if recipe.type == "small" %}
                <h5>{{ texts.meal_size_small }} ({{ recipe.diet.small_size }}%)</h5>
            {% elif recipe.type == "big" %}
                <h5>{{ texts.meal_size_big }} ({{ recipe.diet.big_size }}%)</h5> 
            {% endif %}

        </span>
            <table id="ingredients" class="table">
                <tr>
                    <th>{{ texts.title }}</th>
                    <th>{{ texts.energy_simple }}</th>
                    <th>{{ texts.protein_simple }}</th>
                    <th>{{ texts.fat_simple }}</th>
                    <th>{{ texts.sugar_simple }}</th>
                    <th>{{ texts.amount_simple }}</th>
                    <th></th>
                </tr>

                {% for ingredient in recipe.ingredients: %}
                    <tr>
                        <td>
                            <a href="/ingredient={{ingredient.id}}">{{ ingredient.name }}</a>
                        </td>
                        <td>{{ (ingredient.calorie / 100 * ingredient.amount)|round(2,'common') }}</td>
                        <td>{{ (ingredient.protein / 100 * ingredient.amount)|round(2,'common') }}</td>
                        <td>{{ (ingredient.fat / 100 * ingredient.amount)|round(2,'common') }}</td>
                        <td>{{ (ingredient.sugar / 100 * ingredient.amount)|round(2,'common') }}</td>
                        <td>{{ ingredient.amount|round(2,'common') }}</td>
                        <td></td>
                    </tr>
                {% endfor %}

                <tr class="totals">
                    <td>Celkem</td>
                    <td>{{ totals.calorie }}</td>
                    <td>{{ totals.protein }}</td>
                    <td>{{ totals.fat }}</td>
                    <td>{{ totals.sugar }}</td>
                    <td>{{ totals.amount|round(2,'common')  }}</td>
                    <td>Poměr: {{ totals.ratio }} : 1</td>
                </tr>
            </table>

            {% if show %}
            <div class="row">
                <form action="/recipe={{recipe.id}}/remove" method="post" class="form col-5"  accept-charset="utf-8" onsubmit="return confirm('{{ texts.recipe_delete_confirm }}');">
                    <button type="button" class="editShowButton btn btn-warning">{{ texts.edit }} {{ icons.edit }}</button>
                    <button type="button" class="editHideButton btn btn-warning">{{ texts.edit_cancel }} {{ icons.edit }}</button>
                    <button type="button" class="printButton btn">{{ texts.print }} {{ icons.print }}</button>
                    <button type="submit" class="btn btn-danger">{{ texts.recipe_delete}} {{ icons.delete }}</button>
                </form>

                <span class="col-2"></span>

					<!--
					<form action="/recipe={{recipe.id}}/export" class="form-inline col-5" method="post" accept-charset="utf-8">
                    <input type="submit" class="btn btn-secondary" value="Exportovat recept do diety" />
                    <select name="diet" class="form-control">
                            {% for diet in diets %}
                                <option value="{{ diet.id }}">{{ diet.name }}</option>
                            {% endfor %}
                    </select>
                </form> -->
            </div>
            {% endif %}
        </div>
    </div>
{% endblock %}

