{% extends "base.tpl" %}
{% block title %}
    Všechny diety
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
    .False {
        background-color: lightgrey;
        color: grey;
    }
    .False a{
        color: grey;
        
    }
    </style>
{% endblock %}

{% block script %}
	<script>
        $(document).on("click", ".newDiet", function() {
            var win = window.open('/newdiet');
            win.focus();
        });
    </script>
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
    <div class="container">
        <div class="col-6">
            <table id="diets" class="table">
                <tr>
                    <th>Název</th>
                    <th>Bílkovina</th>
                    <th>Tuk</th>
                    <th>Sacharidy</th>
                    <th>Aktivní</th>
                </tr>
                {% for diet in diets: %}
                    <tr class= {{ diet.active }}>                         
                        <td><a href="/diet={{diet.id}}">{{ diet.name }}</a></td>
                        <td>{{ diet.protein }}</td>
                        <td>{{ diet.fat }}</td>
                        <td>{{ diet.sugar }}</td>
                        <td>
                            {% if diet.active %}
                                Ano
                            {% else %}
                                Ne
                            {% endif %}
                    </tr>
                {% endfor %}
            </table>
            <button class="newDiet btn">Přidat dietu</button>
        </div>    
    </div>
{% endblock %}

