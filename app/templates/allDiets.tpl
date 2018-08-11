{% extends "base.tpl" %}
{% block title %}
    Všechny diety
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
    .inactive {
        background-color: var(--bgcolor_inactive);
        color: var(--color_inactive);
    }
    .inactive a{
        color: var(--color_inactive);
        
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
                    <tr class= {% if diet.active%} active {% else %} inactive {% endif %}>                        
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

