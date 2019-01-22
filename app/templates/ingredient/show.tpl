{% extends "base.tpl" %}
{% block title %}
     {{ texts.ingredient }}
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
        .edit__form{display: none;}
        .editHideButton{display: none;}            
    </style>
{% endblock %}

{% block script %}
    <script type="text/javascript">

        $(document).ready(function() {
            $('.edit__form').hide();
            $('.data__table').show();
            $('.editShowButton').show();
            $('.editHideButton').hide();
        });
            
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
    
    </script>
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
    <div class="container">
        <div class="row">
  
            <div class="col-4">
                <label for="recipes"><h3>{{ texts.recipe_list }}</h3></label>
                <ul name="recipes">
                    {% for recipe in recipes %}
                        <li><a href='/recipe={{ recipe.id }}'>{{ recipe.name }}</a></li>
                    {% endfor %}
                </ul>
            </div>

            <div class="col-8">
                <form action="/ingredient={{ingredient.id}}/edit" class="edit__form form-group" method="post" accept-charset="utf-8">
                    <table class="table">
                        <tr>
                            <th>{{ texts.title }}</th>
                            <th>{{ texts.energy_100 }}</th>
                            <th>{{ texts.protein_100 }}</th>
                            <th>{{ texts.fat_100 }}</th>
                            <th>{{ texts.sugar_100 }}</th>
                            <th>{{ texts.edit }}</th>
                        </tr>
                        <tr>
                            <td>
                                <input type="text" class="form-control" name="name" value="{{ ingredient.name }}" />
                            </td>
                            <td>
                                <input type="text" class="form-control" name="calorie" value="{{ ingredient.calorie }}" />
                            </td>
                            <td>
                                {% if ingredient.used == False %}
                                    <input type="text" class="form-control" pattern="[0-9]+([\.][0-9]+)?" name="protein" value="{{ ingredient.protein }}"/>
                                {% else %}
                                    {{ ingredient.protein }}
                                {% endif %}
                            </td>
                            <td>
                                {% if ingredient.used == False %}
                                    <input type="text" class="form-control" pattern="[0-9]+([\.][0-9]+)?" name="fat" value="{{ ingredient.fat }}"/>
                                {% else %}
                                    {{ ingredient.fat }}
                                {% endif %}
                            </td>
                            <td>
                                {% if ingredient.used == False %}
                                    <input type="text" class="form-control" pattern="[0-9]+([\.][0-9]+)?" name="sugar" value="{{ ingredient.sugar }}"/>
                                {% else %}
                                    {{ ingredient.sugar }}
                                {% endif %}
                            </td>
                            <td>
                                <input type="submit" class="btn btn-warning" value="{{ texts.edit_confirm}}" />
                            </td>
                        </tr>
                    </table>
                </form>

                <table class=" data__table table">
                    <tr>
                        <th>{{ texts.title }}</th>
                        <th>{{ texts.energy_100 }}</th>
                        <th>{{ texts.protein_100 }}</th>
                        <th>{{ texts.fat_100 }}</th>
                        <th>{{ texts.sugar_100 }}</th>
                    </tr>
                    <tr>
                        <td>{{ ingredient.name }}</td>
                        <td>{{ ingredient.calorie }}</td>
                        <td>{{ ingredient.protein }}</td>
                        <td>{{ ingredient.fat }}</td>
                        <td>{{ ingredient.sugar }}</td>
                    </tr>
                 </table>

                <form action="/ingredient={{ingredient.id}}/remove" onsubmit="return confirm('{{ texts.ingredient_delete_confirm }}');" method="post" accept-charset="utf-8">
                    <button type="button" class="editShowButton btn btn-warning">{{ texts.edit }} {{ icons.edit }}</button>
                    <button type="button" class="editHideButton btn btn-warning">{{ texts.edit_cancel }} {{ icons.edit }}</button>
                    {% if ingredient.used == False %}
                        <button type="submit" class="btn btn-danger">{{ texts.ingredient_delete }} {{ icons.delete }}</button>
                    {% else %}
                        <button type="submit" class="btn btn-danger" disabled>{{ texts.delete_error }} {{ icons.delete }}</button>
                    {% endif %}
                </form>
            </div>

        </div>
    </div>
{% endblock %}

