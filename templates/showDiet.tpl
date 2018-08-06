{% extends "base.tpl" %}
{% block title %}
    Dieta: {{diet.name}}
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
                border: 16px solid #f3f3f3; /* Light grey */
                border-top: 16px solid #337ab7; /* Blue */
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
            <div class="col">
                <label for="recipes"><h2>Diety</h2></label>
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

            <div class="col">
                <table id="ingredients" class="table data__table">
                    <tr>
                        <th>Název</th>
                        <th>Bílkovina</th>
                        <th>Tuk</th>
                        <th>Sacharidy</th>
                    </tr>
                    <tr>
                        <td>{{diet.name}}</td>
                        <td>{{diet.protein}}</td>
                        <td>{{diet.fat}}</td>
                        <td>{{diet.sugar}}</td>
                    </tr>
                </table>

                <table class="table data__table">
                    <tr>
                        <th>Velikost jídla</th>
                        <th>Podíl</th>
                    </tr>
                    <tr>
                        <td>Velké jídlo</td>
                        <td>{{ diet.big_size }} %</td>
                    </tr>
                    <tr>
                        <td>Malé jídlo</td>
                        <td>{{ diet.small_size }} %</td>
                    </tr>
                </table>

                <form action="/diet={{diet.id}}/edit" class="edit__form form-group" method="post" accept-charset="utf-8">
                    <table class="table">
                        <tr>
                            <th>Název</th>
                            <th>Bílkovina</th>
                            <th>Tuk</th>
                            <th>Sacharidy</th>
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
                            <th>Velikost jídla</th>
                            <th>Podíl</th>
                        </tr>
                        <tr>
                            <td>Velké jídlo</td>
                            <td>
                                <input type="text" class="form-control" name="big_size" value="{{ diet.big_size }}" />
                            </td>
                        </tr>
                        <tr>
                            <td>Malé jídlo</td>
                            <td>
                                <input type="text" class="form-control" name="small_size"  value="{{ diet.small_size }}" /> 
                            </td>
                        </tr>
                    </table>
                    <input type="submit" class="btn btn-warning" value="Uložit změnu" />
                </form>

                <form action="/diet={{ diet.id }}/remove" method="post" accept-charset="utf-8">
                    <button type="button" class="editShowButton btn btn-warning">Upravit {{ icons.edit }}</button>
                    <button type="button" class="editHideButton btn btn-warning">Zrušit úpravy {{ icons.edit }}</button>
                    {% if diet.used == False %}
                        <button type="submit" class="btn btn-danger">Smazat dietu {{ icons.delete }}</button>
                    {% endif %}
                    <button type="button" class="printButton btn">Tisk {{ icons.print }}</button>
                </form>
                <form action="/diet={{ diet.id }}/archive" method="post" accept-charset="utf-8">
                    {% if diet.active == True %}
                        <button type="submit" class="btn">Archivovat {{ icons.archive }}</button>
                    {% else %}
                        <button type="submit" class="btn">Aktivovat {{ icons.unarchive }}</button>
                    {% endif %}
                </form>
            </div>  
        </div>  
        <div class="loader"></div> 
    </div> 
{% endblock %}

