{% extends "base.tpl" %}
{% block title %}
    Nová dieta
{% endblock %}

{% block style %}
    
{% endblock %}

{% block script %}
<script type="text/javascript">
</script>
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
        <div class="container">
            <form method="POST" action="/newdiet" class="form-group col-6" accept-charset="UTF-8">
                <label for="name">Název diety</label>
                <input type="text" name="name" class="form-control" required placeholder="Nová dieta">
                <label for="protein">Množství bílkovin / den</label>
                <input type="text" pattern="[0-9]+([\.][0-9]+)?" name="protein" class="form-control" step="0.01" required placeholder="0.0">
                <label for="fat">Množství tuku / den</label>
                <input type="text" pattern="[0-9]+([\.][0-9]+)?" name="fat" class="form-control" step="0.01" required placeholder="0.0">
                <label for="sugar">Množství sacharidů / den</label>
                <input type="text" pattern="[0-9]+([\.][0-9]+)?" name="sugar" class="form-control" step="0.01" required placeholder="0.0">
                <label for="small_size">Procentuální velikost malého jídla</label>
                <input type="text" pattern="[0-9]+([\.][0-9]+)?" name="small_size" class="form-control" step="0.1" required placeholder="0">
                <label for="big_size">Procentuální velikost velkého jídla</label>
                <input type="text" pattern="[0-9]+([\.][0-9]+)?" name="big_size" class="form-control" step="0.1" required placeholder="0">
                <input type="submit" class="btn btn-primary" value="Přidat dietu" />
            </form>
        </div>
{% endblock %}

