{% extends "base.tpl" %}
{% block title %}
    Logging
{% endblock %}

{% block style %}
{% endblock %}

{% block script %}
{% endblock %}

{% block content %}
    {% include('navbar_empty.tpl') %}
    <div class="container">
        <div class="main">
            <table>
            <td class="col-2"></td>

            <td class="col-8">
                {% for log in logs: %}
                    <table>
                        <th>{{ log }}</th>
                    </table>
                {% endfor %}
            </td>

            <td class="col-2"></td>
            </table>
        	
        </div>
    </div>
{% endblock %}







