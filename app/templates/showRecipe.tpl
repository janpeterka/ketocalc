{% extends "base.tpl" %}
{% block title %}
    {% if show %}
        Recept
    {% else %}
        Vytisknout recept - {{ recipe.name }}
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
                    <option value="small">Malé jídlo ({{ recipe.diet.small_size }})</option>
                    <option value="big">Velké jídlo ({{ recipe.diet.big_size }})</option>
                </select>
                <input type="submit" value="Změnit recept" class="btn btn-warning">
            </form>
            {% endif %}

            {% if show %}
                <span class="data__table">
            {% else %}
                <span class="data__table d-print-table">
            {% endif %}

                <h2>{{ recipe.name }}</h2>

            {% if recipe.type == "small" %}
                <h5>Malé jídlo ({{ recipe.diet.small_size }}%)</h5>
            {% elif recipe.type == "big" %}
                <h5>Velké jídlo ({{ recipe.diet.big_size }}%)</h5> 
            {% endif %}

        </span>
            <table id="ingredients" class="table">
                <tr>
                    <th>Název</th>
                    <th>Kalorie</th>
                    <th>Bílkovina</th>
                    <th>Tuk</th>
                    <th>Sacharidy</th>
                    <th>Množství</th>
                    <th></th>
                </tr>

                {% for ingredient in recipe.ingredients: %}
                    <tr>
                        <td>
                            <a href="/ingredient={{ingredient.id}}">{{ ingredient.name }}</a>
                        </td>
                        <td>{{ (ingredient.calorie / 100 * ingredient.amount)|round(2,'common') }} kcal</td>
                        <td>{{ (ingredient.protein / 100 * ingredient.amount)|round(2,'common') }} g</td>
                        <td>{{ (ingredient.fat / 100 * ingredient.amount)|round(2,'common') }} g</td>
                        <td>{{ (ingredient.sugar / 100 * ingredient.amount)|round(2,'common') }} g</td>
                        <td>{{ ingredient.amount|round(2,'common') }} g</td>
                        <td></td>
                    </tr>
                {% endfor %}

                <tr class="totals">
                    <td>Celkem</td>
                    <td>{{ totals.calorie }} kcal</td>
                    <td>{{ totals.protein }} g</td>
                    <td>{{ totals.fat }} g</td>
                    <td>{{ totals.sugar }} g</td>
                    <td>{{ totals.amount|round(2,'common')  }} g</td>
                    <td>Poměr: {{ totals.ratio }} : 1</td>
                </tr>
            </table>

            {% if show %}
            <div class="row">
                <form action="/recipe={{recipe.id}}/remove" method="post" class="form col-5"  accept-charset="utf-8" onsubmit="return confirm('Opravdu chcete smazat recept?');">
                    <button type="button" class="editShowButton btn btn-warning">Upravit {{ icons.edit }}</button>
                    <button type="button" class="editHideButton btn btn-warning">Zrušit úpravy {{ icons.edit }}</button>
                    <button type="button" class="printButton btn">Tisk {{ icons.print }}</button>
                    <button type="submit" class="btn btn-danger">Smazat recept {{ icons.delete }}</button>
                </form>

                <span class="col-2"></span>

					<!--
					<form action="/recipe={{recipe.id}}/export" class="form-inline col-5" method="post" accept-charset="utf-8">
                    <input type="submit" class="btn" value="Exportovat recept do diety" />
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

