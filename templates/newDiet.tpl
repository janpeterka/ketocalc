{% extends "base.tpl" %}
{% block title %}
    Nová dieta
{% endblock %}

{% block style %}
    
{% endblock %}

{% block script %}
	
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
        <div class="container">
            <form id="newDietForm" method="POST" action="/newdiet" class="form-group col-6">
                <label for="name">Název diety</label>
                <input type="text" name="name" class="form-control"  value={{name}}>
                <label for="protein">Množství bílkovin / den</label>
                <input type="text" pattern="[0-9]+([\.][0-9]+)?" name="protein" class="form-control" step="0.01" value={{protein}}><br>
                <label for="fat">Množství tuku / den</label>
                <input type="text" pattern="[0-9]+([\.][0-9]+)?" name="fat" class="form-control" step="0.01" value={{fat}}>
                <label for="sugar">Množství sacharidů / den</label>
                <input type="text" pattern="[0-9]+([\.][0-9]+)?" name="sugar" class="form-control" step="0.01" value={{sugar}}>
                <label for="small_size">Procentuální velikost malého jídla</label>
                <input type="text" pattern="[0-9]+([\.][0-9]+)?" name="small_size" class="form-control" step="0.1" value="0">
                <label for="big_size">Procentuální velikost velkého jídla</label>
                <input type="text" pattern="[0-9]+([\.][0-9]+)?" name="big_size" class="form-control" step="0.1" value="0">

                <input id="ajaxButton" type="submit" class="btn btn-primary" value="Přidat dietu" /><br>
            </form>
        </div>
{% endblock %}

