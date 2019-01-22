{% extends "base.tpl" %}
{% block title %}
    {{ texts.diet }}: {{ diet.name }}
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
            .btn{
                margin-top: 5px;
            }
            .edit__form{
                display: none;
            }

            .editHideButton{
                display: none;
            }    

            .loader {
                display: none;
                border: 16px solid var(--color_loader_outer); /* Light grey */
                border-top: 16px solid var(--color_loader_inner); /* Blue */
                border-radius: 50%;
                width: 300px;
                height: 300px;
                animation: spin 2s linear infinite;
                margin: 80px auto;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
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

            // $(document).on("click", ".export__button", function() {
            //     $('.row').hide();
            //     $('.loader').show();
            // });

            $(document).on("click", ".printButton", function() {
                var win = window.open(window.location.href + '/print');
                win.focus();
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
                {% for recipe in recipes: %}
                        <li><a href="/recipe={{recipe.id}}">{{ recipe.name }}</a></li>
                {% endfor %} 
                </ul>

                <form action="/diet={{ diet.id }}/export" class="form-inline" method="post">
                    {% if recipes|length > 0 %}
                        <!-- <input type="submit" class="btn btn-default export__button" value="Exportovat recepty do diety"> -->
                        <select name="diet" class="form-control">
                        {% for diet in diets %}
                            <option value="{{ diet.id }}">{{ diet.name }}</option>
                        {% endfor %}
                        </select>
                    {% endif %}
                </form>
            </div>

            <div class="col-8">
                <table id="ingredients" class="table data__table">
                    <tr>
                        <th>{{ texts.title }}</th>
                        <th>{{ texts.protein_simple }}</th>
                        <th>{{ texts.fat_simple }}</th>
                        <th>{{ texts.sugar_simple }}</th>
                    </tr>
                    <tr>
                        <td>{{ diet.name }}</td>
                        <td>{{ diet.protein }}</td>
                        <td>{{ diet.fat }}</td>
                        <td>{{ diet.sugar }}</td>
                    </tr>
                </table>

                <table class="table data__table">
                    <tr>
                        <th>{{ texts.meal_size }}</th>
                        <th>{{ texts.meal_portion }}</th>
                    </tr>
                    <tr>
                        <td>{{ texts.meal_size_big }}</td>
                        <td>{{ diet.big_size }} %</td>
                    </tr>
                    <tr>
                        <td>{{ texts.meal_size_small }}</td>
                        <td>{{ diet.small_size }} %</td>
                    </tr>
                </table>

                <form action="/diet={{diet.id}}/edit" class="edit__form form-group" method="post" accept-charset="utf-8">
                    <table class="table">
                        <tr>
                            <th>{{ texts.title }}</th>
                            <th>{{ texts.protein_simple }}</th>
                            <th>{{ texts.fat_simple }}</th>
                            <th>{{ texts.sugar_simple }}</th>
                        </tr>
                        <tr>
                            <td>
                                <input type="text" class="form-control" name="name" size="12" value="{{ diet.name }}" />
                            </td>
                            <td>
                                {% if diet.used == False %}
                                    <input type="text" class="form-control" pattern="[0-9]+([\.][0-9]+)?" name="protein" value="{{ diet.protein }}"/>
                                {% else %}
                                    {{ diet.protein }}
                                {% endif %}
                            </td>
                            <td>
                                {% if diet.used == False %}
                                    <input type="text" class="form-control" pattern="[0-9]+([\.][0-9]+)?" name="fat" value="{{ diet.fat }}"/>
                                {% else %}
                                    {{ diet.fat }}
                                {% endif %}
                            </td>
                            <td>
                                {% if diet.used == False %}
                                    <input type="text" class="form-control" pattern="[0-9]+([\.][0-9]+)?" name="sugar" value="{{ diet.sugar }}"/>
                                {% else %}
                                    {{ diet.sugar }}
                                {% endif %}
                            </td>
                        </tr>
                    </table>

                    <table class="table edit__form">
                        <tr>
                            <th>{{ texts.meal_size }}</th>
                            <th>{{ texts.meal_portion }}</th>
                        </tr>
                        <tr>
                            <td>{{ texts.meal_size_big }}</td>
                            <td>
                                <input type="text" class="form-control" name="big_size" value="{{ diet.big_size }}" />
                            </td>
                        </tr>
                        <tr>
                            <td>{{ texts.meal_size_small }}</td>
                            <td>
                                <input type="text" class="form-control" name="small_size"  value="{{ diet.small_size }}" /> 
                            </td>
                        </tr>
                    </table>
                    <input type="submit" class="btn btn-warning" value="{{ texts.edit_confirm }}" />
                </form>

                <form action="/diet={{ diet.id }}/remove" method="post" accept-charset="utf-8">
                    <button type="button" class="editShowButton btn btn-warning">{{ texts.edit }} {{ icons.edit }}</button>
                    <button type="button" class="editHideButton btn btn-warning">{{ texts.edit_cancel }} {{ icons.edit }}</button>
                    {% if diet.used == False %}
                        <button type="submit" class="btn btn-danger">{{ texts.diet_delete }} {{ icons.delete }}</button>
                    {% endif %}
                    <button type="button" class="printButton btn btn-secondary">{{ texts.print }} {{ icons.print }}</button>
                </form>
                <form action="/diet={{ diet.id }}/archive" method="post" accept-charset="utf-8">
                    {% if diet.active == True %}
                        <button type="submit" class="btn btn-secondary">{{ texts.archive }} {{ icons.archive }}</button>
                    {% else %}
                        <button type="submit" class="btn btn-secondary">{{ texts.unarchive }} {{ icons.unarchive }}</button>
                    {% endif %}
                </form>
            </div>  
        </div>  
        <div class="loader"></div> 
    </div> 
{% endblock %}

