{% extends "base.tpl" %}
{% block title %}
    Surovina
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
        .edit__form{display: none;}
        .editHideButton{display: none;}            
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
    
    </script>
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
    <div class="container">
        <div class="col-12">
            <form action="/ingredient={{ingredient.id}}/edit" class="edit__form form-group" method="post" accept-charset="utf-8">
                <table class="table">
                    <tr>
                        <th>Název</th>
                        <th>Kalorie</th>
                        <th>Bílkovina</th>
                        <th>Tuk</th>
                        <th>Sacharidy</th>
                        <th>Upravit</th>
                    </tr>
                    <tr>
                        <td>
                            <input type="text" class="form-control" name="name" value="{{ ingredient.name }}" />
                        </td>
                        <td>
                            <input type="text" class="form-control" name="calorie" value="{{ ingredient.calorie }}" />
                        </td>
                        <td>
                            {% if used == False %}
                                <input type="text" class="form-control" pattern="[0-9]+([\.][0-9]+)?" name="protein" value="{{ ingredient.protein }}"/>
                            {% else %}
                                {{ ingredient.protein }}
                            {% endif %}
                        </td>
                        <td>
                            {% if used == False %}
                                <input type="text" class="form-control" pattern="[0-9]+([\.][0-9]+)?" name="fat" value="{{ ingredient.fat }}"/>
                            {% else %}
                                {{ ingredient.fat }}
                            {% endif %}
                        </td>
                        <td>
                            {% if used == False %}
                                <input type="text" class="form-control" pattern="[0-9]+([\.][0-9]+)?" name="sugar" value="{{ ingredient.sugar }}"/>
                            {% else %}
                                {{ ingredient.sugar }}
                            {% endif %}
                        </td>
                        <td>
                            <input type="submit" class="btn btn-warning" value="Uložit změnu" />
                        </td>
                    </tr>
                </table>
            </form>

            <table class=" data__table table">
                <tr>
                    <th>Název</th>
                    <th>Kalorie</th>
                    <th>Bílkovina</th>
                    <th>Tuk</th>
                    <th>Sacharidy</th>
                </tr>
                <tr>
                    <td>{{ ingredient.name }}</td>
                    <td>{{ ingredient.calorie }}</td>
                    <td>{{ ingredient.protein }}</td>
                    <td>{{ ingredient.fat }}</td>
                    <td>{{ ingredient.sugar }}</td>
                </tr>
             </table>

            <form action="/ingredient={{ingredient.id}}/remove" onsubmit="return confirm('Opravdu chcete smazat recept?');" method="post" accept-charset="utf-8">
                <button type="button" class="editShowButton btn btn-warning">Upravit <i class="fas fa-pencil-alt"></i></button>
                <button type="button" class="editHideButton btn btn-warning">Zrušit úpravy <i class="fas fa-pencil-alt"></i></button>
                {% if used == False %}
                    <button type="submit" class="btn btn-danger">Smazat surovinu <i class="fas fa-trash"></i></button>
                {% else %}
                    <button type="submit" class="btn btn-danger" disabled>Nelze smazat <i class="fas fa-trash"></i></button>
                    {# <input type="submit" class="btn btn-danger" disabled value="Nelze smazat" /> #}
                {% endif %}
            </form>
        </div>
    </div>
{% endblock %}

