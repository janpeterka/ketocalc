{% extends "base.tpl" %}
{% block title %}
    Uživatel
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
        .edit__form{
            display: none;
        }
        .editHideButton{
            display: none;
        }     
        .warning{
            color: var(--color_warning);
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

        function validateRegister(){
            if ($(".password").val().length < 8){
                bootbox.alert("Heslo je příliš krátké!");
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

        function toggleVisibility() {
            var x = $('#password')
            if (x.attr("type") === "password"){
                x.attr("type", 'text');
            } else {
                x.attr("type", 'password');
            }
        }

    </script>
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
    <div class="container">
        <div class="edit__form col-12">
            <form action="/user/edit" class="form-group" method="post" accept-charset="utf-8">
                <table class="table">
                    <tr>
                        <th>{{ texts.user_username}}</th>
                        <th>{{ texts.user_firstname}}</th>
                        <th>{{ texts.user_lastname}}</th>
                        <th></th>
                    </tr>
                    <tr>
                        <td>
                            {{ user.username }}
                            {# <input type="text" class="form-control" value="{{ user.username }}" /> #}
                        </td>
                        <td>
                            <input name="firstname" type="text" class="form-control" value="{{ user.first_name }}"/>
                        </td>
                        <td>
                            <input name="lastname" type="text" class="form-control" value="{{ user.last_name }}"/>
                        </td>
                        <td>
                            <input type="submit" class="btn btn-warning" value="{{ texts.edit_confirm }}" />
                        </td>
                    </tr>
                </table>
            </form>

            <form action="/user/password_change" method="post" onsubmit="return validateRegister()" >
                <table class="table">
                    <td>
                        <input id="password" name="password" type="password" class="form-control password" placeholder="{{ texts.password_new }}" />
                        <span class="warning wrongPassword"></span>
                    </td>
                    <td>
                        <!-- <input type="password" class="form-control againPassword" placeholder="{{ texts.password_new_again }}" /> -->
                        <!-- <span class="warning diffPassword"></span> -->
                        <input type="button" class="btn" onclick="toggleVisibility()" value="{{ texts.password_show }}">
                    </td>
                    <td>
                        <input type="submit" class="btn btn-warning" value="{{ texts.password_change }}">
                    </td>
                </table>
            </form>
        </div>

        <div class="data__table col-12">
            <table class="table">
                <tr>
                    <th>{{ texts.user_username}}</th>
                    <th>{{ texts.user_firstname}}</th>
                    <th>{{ texts.user_lastname}}</th>
                </tr>
                <tr>
                    <td>{{ user.username }}</td>
                    <td>{{ user.first_name }}</td>
                    <td>{{ user.last_name }}</td>
                </tr>
             </table>
        </div>

        <div>
            <form>
                <button type="button" class="editShowButton btn btn-warning">{{ texts.edit }} {{ icons.edit }}</button>
                <button type="button" class="editHideButton btn btn-warning">{{ texts.edit_cancel}} {{ icons.edit }}</button>
            </form>
        </div>
    </div>
{% endblock %}

