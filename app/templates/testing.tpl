{% extends "base.tpl" %}
{% block title %}
    Testování
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
                {% for test in tests: %}
                    <table>
                        <th>test.name</th>
                        <tr>test.result</tr>
                    </table>

                {% endfor %}
            </td>

            <td class="col-2"></td>
            </table>
        	
        </div>
    </div>
{% endblock %}
