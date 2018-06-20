{% extends "base.tpl" %}
{% block title %}
    Uživatel
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
        <div class="col-8">
            <form action="/user={{user.id}}/edit" class="edit__form form-group" method="post" accept-charset="utf-8">
                <table class="table">
                    <tr>
                        <th>Přihlašovací jméno</th>
                        <th>Jméno</th>
                        <th>Příjmení</th>
                    </tr>
                    <tr>
                        <td>
                            <input type="text" class="form-control" name="name" value="{{ user.username }}" />
                        </td>
                        <td>
                            <input type="text" class="form-control" pattern="[0-9]+([\.][0-9]+)?" name="fat" value="{{ user.firstname }}"/>
                        </td>
                        <td>
                            <input type="text" class="form-control" pattern="[0-9]+([\.][0-9]+)?" name="sugar" value="{{ user.lastname }}"/>
                        </td>
                        <td>
                            <input type="submit" class="btn btn-warning" value="Uložit změnu" />
                        </td>
                    </tr>
                </table>
            </form>

            <table class=" data__table table">
                <tr>
                    <th>Přihlašovací jméno</th>
                    <th>Jméno</th>
                    <th>Příjmení</th>
                </tr>
                <tr>
                    <td>{{ user.username }}</td>
                    <td>{{ user.firstname }}</td>
                    <td>{{ user.lastname }}</td>
                </tr>
             </table>

            <form>
                <button type="button" disabled class="editShowButton btn btn-warning">Upravit <i class="fas fa-pencil-alt"></i></button>
                <button type="button" disabled class="editHideButton btn btn-warning">Zrušit úpravy <i class="fas fa-pencil-alt"></i></button>
            </form>
        </div>
    </div>
{% endblock %}

