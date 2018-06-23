{% extends "base.tpl" %}
{% block title %}
    Uživatel
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
        .edit__form{display: none;}
        .editHideButton{display: none;}     
        .warning{color: red;}       
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

        function validateRegister(){
            if ($(".password").val().length < 8){
                bootbox.alert("Heslo je příliš krátké!");
                return false
            }
            else if ($(".password").val() != $(".againPassword").val()){
                bootbox.alert("Hesla jsou rozdílná!");
                return false
            }
            else {
              return true  
            }
        }

        $(document).on('blur','.password',function(){
            if ($(this).val().length > 8){
                $(".wrongPassword").empty();
            } else {
                $(".wrongPassword").empty();
                $(".wrongPassword").append("<small class='form-text'>Heslo je příliš krátké!</small>");
            }

        });
        $(document).on('blur','.againPassword',function(){
            if ($(this).val() === $(".password").val()){
                $(".diffPassword").empty();
            } else {
                $(".diffPassword").empty();
                $(".diffPassword").append("<small class='form-text'>Hesla jsou rozdílná!</small>");
            }
        });
    
    </script>
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
    <div class="container">
        <div class="edit__form col-12">
            <form action="/user/edit" class="form-group" method="post" accept-charset="utf-8">
                <table class="table">
                    <tr>
                        <th>Přihlašovací jméno</th>
                        <th>Jméno</th>
                        <th>Příjmení</th>
                        <th></th>
                    </tr>
                    <tr>
                        <td>
                            {{ user.username }}
                            {# <input type="text" class="form-control" value="{{ user.username }}" /> #}
                        </td>
                        <td>
                            <input name="firstname" type="text" class="form-control" value="{{ user.firstname }}"/>
                        </td>
                        <td>
                            <input name="lastname" type="text" class="form-control" value="{{ user.lastname }}"/>
                        </td>
                        <td>
                            <input type="submit" class="btn btn-warning" value="Uložit změnu" />
                        </td>
                    </tr>
                </table>
            </form>

            <form action="/user/password_change" method="post" onsubmit="return validateRegister()" >
                <table class="table">
                    <td>
                        <input name="password" type="password" class="form-control password" placeholder="Nové heslo" />
                        <span class="warning wrongPassword"></span>
                    </td>
                    <td>
                        <input type="password" class="form-control againPassword" placeholder="Nové heslo znovu" />
                        <span class="warning diffPassword"></span>
                    </td>
                    <td>
                        <input type="submit" class="btn btn-warning" value="Změnit heslo">
                    </td>
                </table>
            </form>
        </div>

        <div class="data__table col-12">
            <table class="table">
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
        </div>

        <div>
            <form>
                <button type="button" class="editShowButton btn btn-warning">Upravit <i class="fas fa-pencil-alt"></i></button>
                <button type="button" class="editHideButton btn btn-warning">Zrušit úpravy <i class="fas fa-pencil-alt"></i></button>
            </form>
        </div>
    </div>
{% endblock %}

