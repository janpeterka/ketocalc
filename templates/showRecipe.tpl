{% extends "base.tpl" %}
{% block title %}
	Recept
{% endblock %}
    
{% block style %}
    <style type="text/css" media="screen">
            .edit__form{
                display: none;
            }

            .editHideButton{
                display: none;
            }            
        </style>
{% endblock %}

{% block script %}
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
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
    <div class="container">
        <div class="col-12">
            <form action="/recipe={{recipe.id}}/edit" class="form-inline edit__form" method="post" accept-charset="utf-8">
                <input type="text" name="name" class="form-control col-4" value="{{ recipe.name }}"><br>
                <select name="size" class="form-control">
                    <option value="small">Malé jídlo ({{ diet.small_size }})</option>
                    <option value="big">Velké jídlo ({{ diet.big_size }})</option>
                </select>
                <input type="submit" value="Změnit recept" class="btn btn-warning">
            </form>

            <span class="data__table">

                <h2>{{ recipe.name }}</h2>

            {% if recipe.size == "small" %}
                <h5>Malé jídlo ({{ diet.small_size }}%)</h5>
            {% elif recipe.size == "big" %}
                <h5>Velké jídlo ({{ diet.big_size }}%)</h5> 
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

                {% for ingredient in ingredients: %}
                    <tr>
                        <td>
                            <a href="/ingredient={{ingredient.id}}">{{ ingredient.name }}</a>
                        </td>
                        <td>{{ ingredient.calorie }} kcal</td>
                        <td>{{ ingredient.protein }} g</td>
                        <td>{{ ingredient.fat }} g</td>
                        <td>{{ ingredient.sugar }} g</td>
                        <td>{{ ingredient.amount}} g</td>
                        <td></td>
                    </tr>
                {% endfor %}

                <tr>
                    <td>Celkem</td>
                    <td>{{ totals.calorie }} kcal</td>
                    <td>{{ totals.protein }} g</td>
                    <td>{{ totals.fat }} g</td>
                    <td>{{ totals.sugar }} g</td>
                    <td>{{ totals.amount }} g</td>
                    <td>Poměr: {{ totals.eq }} : 1</td>
                </tr>
            </table>
            <div class="row">
                <form action="/recipe={{recipe.id}}/remove" method="post" class="form col-5"  accept-charset="utf-8">
                    <input type="button" class="editShowButton btn btn-warning" value="Upravit recept" />
                    <input type="button" class="editHideButton btn btn-warning" value="Zrušit úpravy" />
                    <input type="button" class="printButton btn" value="Vytisknout" />
                    <input type="submit" class="btn btn-danger" value="Smazat recept" />
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
        </div>
    </div>
{% endblock %}

