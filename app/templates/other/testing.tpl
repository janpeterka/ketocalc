{# {% extends "base.tpl" %}
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
{% endblock %} #}

{% extends "base.tpl" %}
{% block title %}
    Zpěvníky
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">

    body{
        background-color: #eee

    }
    div.songbook{
        border-radius: 6px;
        padding: 10px 30px;
        margin: 5px;
        background-color: #fff;
        box-shadow: 0 0 0 1px rgba(89,105,129,.1),0 1px 3px 0 rgba(89,105,129,.1),0 1px 2px 0 rgba(0,0,0,.05);


    }

    a.songbook{
        color: black;
    }
    </style>    
{% endblock %}

{% block script %}

{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
    <div class="container">
        <div class="main">
            <table>
            <td class="col-2"></td>

            <td class="col-8">
                <div class="songbook">
                    <a class="songbook" href="/static/files/songbooks/songbook_main.pdf" download> Hlavní zpěvník [PDF] </a>
                </div>
            </td>

            <td class="col-2"></td>
            </table>
            
        </div>
    </div>
{% endblock %}






