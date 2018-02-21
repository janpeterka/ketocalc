{% extends "base.tpl" %}
{% block title %}Vítejte {{firstname}}{% endblock %}
{% block script %}
	   <script type="text/javascript">

        $(document).ready(function() {
            $("#selectDietForm").submit();
        });

        $(document).on("submit", "#selectDietForm", function(e) {
            $.ajax({
                type: 'POST',
                url: '/selectDietAJAX',
                data: $(this).serialize(),
                success: function(response) {
                    var recipes = response.array;
                    var dietID = response.dietID[0];
                    // recipes to table
                    $('#recipeList').empty();
                    for (i = 0; i<response.array.length; i++ ){
                        $('#recipeList').append("<li><a href='/recipe=" + recipes[i].id + "'>" + recipes[i].name + "</a></li>");
                    }
                },
                error: function(error) {
                    console.log(error);
                }

            });
            e.preventDefault();
        });
        
    </script>
{% endblock %}

{% block content %}
	{% include('navbar.tpl') %}
    <div class="container">
        <div class="row">
            <div class="col">
                <h4>Seznam receptů:</h4>
                <ul id="recipeList"></ul>
            </div>

            <div class="form-inline col" style="display: block;">
                <form id="selectDietForm" method="POST" action="/selectDietAJAX">
                    <select id="selectDiet" name="selectDiet" class="form-control">
                        {% for diet in diets: %}
                            <option value="{{diet.id}}">{{ diet.name }}</option>
                        {% endfor %}
                    </select>
                    <input id="ajaxButton" type="submit" class="btn btn-primary" value="Změnit dietu" />
                </form>
            </div>
        </div>
    </div>
{% endblock %}

