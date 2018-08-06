{% extends "base.tpl" %}
{% block title %}
    Nový recept
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">

        .recipe__wrong{
            display: none;
        }

        .recipe__right{
            display: none;
        }

       .container__main {
            margin-top: 40px;
        }

        .recipe__loader {
            display: none;
            border: 16px solid #f3f3f3; /* Light grey */
            border-top: 16px solid #337ab7; /* Blue */
            border-radius: 50%;
            width: 200px;
            height: 200px;
            animation: spin 2s linear infinite;
            margin: 40px auto;
        }

        .prerecipe__selected-ingredients__table tr {
            transition: background-color 0.5s ease;

        }

        .tr-mainIngredient {
            background-color: #a4f442;
        }

        .tr-fixedIngredient {
            background-color: grey;
        }

        .prerecipe__selected-ingredients__table tr td i {
            margin-right: 1em;
        }

        .fa-times {
            color: #8b0000;
            font-size: 12pt;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        #sliderVal{
            font-weight: bold;
        }

        .in{
            opacity: .9;
        }

    </style>
{% endblock %}

{% block script %}
	<script type="text/javascript">
            var prerecipe__ingredient_array = [];
            var recipe__ingredient_array = [];
            var recipe__ingredient_dietID = "";

            /// On ready - change visibility to default
            $(document).ready(function() {
                allIngredients = $(".prerecipe__add-ingredient__form__select").html();
                $(".recipe__right").hide();
                $(".recipe__wrong").hide();
                $(".recipe__loader").hide();
                prerecipe__selectedIngredients__table__empty();
                prerecipe__calc__form__empty();
                $('.js-example-basic-single').select2();
            });

            // ingredient select to actual
            function prerecipe__addIngredient__form__select__refresh(){
                $('.prerecipe__add-ingredient__form__select').empty();
                $('.prerecipe__add-ingredient__form__select').append(allIngredients);

                for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                    $('.prerecipe__add-ingredient__form__select option[value="' + prerecipe__ingredient_array[i].id + '"]').remove(); // wip
                }
            }

            // ingredient select to default
            function prerecipe__addIngredient__form__select__renew(){
                $('.prerecipe__add-ingredient__form__select').empty();
                $('.prerecipe__add-ingredient__form__select').append(allIngredients);
            }


            // empty prerecipe ingredients table
            function prerecipe__selectedIngredients__table__empty(){
                $('.prerecipe__selected-ingredients__table').empty();
                $(".prerecipe__selected-ingredients__table").append(
                    '<tr>'+
                        '<th>Název</th>'+
                        '<th>Kalorie</th>'+
                        '<th>Bílk.</th>'+
                        '<th>Tuk</th>'+
                        '<th>Sach.</th>'+
                        '<th></th>'+
                    '</tr>');
            }

            function prerecipe__selectedIngredients__table__add(ingredient){
                $('.prerecipe__selected-ingredients__table').append(
                '<tr id_value="' + ingredient.id + '">' +
                    "<td>" + ingredient.name + "</td>" +
                    "<td>" + ingredient.calorie + "</td>" +
                    "<td>" + ingredient.protein+ "</td>" +
                    "<td>" + ingredient.fat + "</td>"+
                    "<td>" + ingredient.sugar + "</td>"+
                    "<td>" +
                        '{{ icons.ingredient_fixed }}' +
                        '{{ icons.ingredient_main }}' +
                        '{{ icons.ingredient_remove }}' +
                    "</td>"+
                "</tr>");
            }

            // empty recipe ingredients table
            function recipe__right__form__ingredientTable__empty(){
                $('.recipe__right__form__ingredient-table').empty();
                $('.recipe__right__form__ingredient-table').append(
                    '<tr>'+
                        '<th>Název</th>'+
                        '<th>Kalorie</th>'+
                        '<th>Bílkovina</th>'+
                        '<th>Tuk</th>'+
                        '<th>Sacharidy</th>'+
                        '<th>Množství</th>'+
                        '<th></th>'+
                    '</tr>');
            }

            // add ingredient to recipe
            function recipe__right__form__addIngredient(ingredient){
                recipe__ingredient_array.push(ingredient)
            }

            // empty prerecipe form values
            function prerecipe__calc__form__empty(){
                prerecipe__ingredient_array.length = 0;
            }

            // empty recipe form values
            function recipe__right__form__empty(){
                recipe__ingredient_array.length = 0;
            }

            // remove prerecipe__form ingredient
            function prerecipe__calc__form__ingredients__remove(id){
                for (let i = 0; i < prerecipe__ingredient_array.length; i++) {
                    if (prerecipe__ingredient_array[i].id == id){
                        prerecipe__ingredient_array.splice(i, 1);
                        break;
                    }
                }
            }

            // add prerecipe__form ingredient
            function prerecipe__calc__form__ingredients__add(ingredient){
                // if already at least one ingredient in array/table
                if (prerecipe__ingredient_array.length > 0) {
                    var hasMain = false;
                    for (let i = 0; i < prerecipe__ingredient_array.length; i++) {
                        if (prerecipe__ingredient_array[i]['main']){
                            hasMain = true;
                        }
                    }

                    if (! hasMain){
                        prerecipe__ingredient_array[0]['main'] = true;
                        setMainIngredient(prerecipe__ingredient_array[0]['id']);
                    }
                }

                prerecipe__ingredient_array.push({'id': ingredient.id, 'name': ingredient.name, 'fixed': false, 'main': false, 'amount': 0});
            }


            // visibility
            function recipe__loader__show(){
                $(".recipe__loader").show();
                $(".recipe__right").hide();
                $(".recipe__wrong").hide();
            }

            function recipe__wrong__show(){
                $(".recipe__loader").hide();
                $(".recipe__wrong").show();
                $(".recipe__right").hide();
            }

            function recipe__right__show(){
                $(".recipe__loader").hide();
                $(".recipe__wrong").hide();
                $(".recipe__right").show();
            }

            function recipe__hideAll(){
                $(".recipe__loader").hide();
                $(".recipe__wrong").hide();
                $(".recipe__right").hide();
            }

            $(document).on("submit", ".recipe__right__form", function(e){
                $.ajax({
                        type: 'POST',
                        url: '/saveRecipeAJAX',
                        data: JSON.stringify({
                            'ingredients' : recipe__ingredient_array,
                            'dietID' : recipe__ingredient_dietID,
                            'name' : $('[name="recipe__right__form__name-input"]').val(),
                            'size' : $('[name="recipe__right__form__size-select"]').val()
                        }),
                        contentType: 'application/json;charset=UTF-8',
                        success: function(response){
                            var pathname = window.location.pathname.split("/")[0];
                            window.location.replace(pathname + response);
                        },
                        error: function(error) {
                            // console.log(error);
                        }
                });
                e.preventDefault();
            });

            $(document).on("submit", ".prerecipe__calc__form", function(e) {

                    // check conditions - ingredients types count
                    main_count = 0;
                    fixed_count = 0;
                    variable_count = 0;
                    for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                        if (prerecipe__ingredient_array[i].fixed == true){
                            fixed_count++;
                        } else if (prerecipe__ingredient_array[i].main == true){
                            main_count++;
                        } else {
                            variable_count++;
                        }
                    }
                    // main to variable if necessary
                    if (variable_count == 2 && main_count == 1){
                        for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                            if (prerecipe__ingredient_array[i].main == true){
                                prerecipe__ingredient_array[i].main = false;
                                main_count--;
                                variable_count++;
                        }
                      }
                    }

                    //nefixních (počítaná + hlavní) > 4
                    if (variable_count + main_count > 4){
                        bootbox.alert("Příliš mnoho počítaných surovin - počítané suroviny musí být právě 3");
                        $(".recipe__loader").hide();

                        return false;
                    }
                    //počítaná > 3
                    if (variable_count > 3){
                        bootbox.alert("Příliš mnoho počítaných surovin - počítané suroviny musí být právě 3");
                        $(".recipe__loader").hide();
                        return false;
                    }
                    //málo počítaných surovin
                    if (variable_count + main_count < 3){
                        bootbox.alert("Příliš málo počítaných surovin - počítané suroviny musí být právě 3");
                        $(".recipe__loader").hide();
                        return false;
                    }

                    // values for fixed
                    for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                        if (prerecipe__ingredient_array[i].fixed) {
                            prerecipe__ingredient_array[i].amount = parseFloat(prompt("Množství suroviny " + prerecipe__ingredient_array[i].name + ":","").replace(",","."));
                        }
                    }

                    $.ajax({
                        type: 'POST',
                        url: '/calcRecipeAJAX',
                        data: JSON.stringify({
                            'ingredients' : prerecipe__ingredient_array,
                            'dietID' : $('.select-diet').val()
                        }),
                        contentType: 'application/json;charset=UTF-8',
                        success: function(response){

                            // // empty recipe all
                            recipe__right__form__empty();
                            recipe__right__form__ingredientTable__empty();

                            if (response == "False"){
                                recipe__wrong__show();
                                return;
                            }

                            var ingredients = response.ingredients;
                            var totals = response.totals;

                            // ingredients to table
                            for ( let i = 0; i < ingredients.length; i++ ){
                                var ingredient_tr = ""

                                if (ingredients[i].main){
                                    ingredient_tr += '<tr class="tr-mainIngredient ">'
                                } else if (ingredients[i].fixed){
                                    ingredient_tr += '<tr class="tr-fixedIngredient">'
                                } else {
                                    ingredient_tr += '<tr class="tr-variableIngredient">' 
                                }

                                ingredient_tr +=    "<td>" + ingredients[i].name + "</td>" +
                                                    '<td><span id="calorie_' + ingredients[i].id + '">' + ingredients[i].calorie + "</span></td>" +
                                                    '<td><span id="protein_' + ingredients[i].id + '">' + ingredients[i].protein + "</span></td>" +
                                                    '<td><span id="fat_' + ingredients[i].id + '">' + ingredients[i].fat + "</span></td>" +
                                                    '<td><span id="sugar_' + ingredients[i].id + '">' + ingredients[i].sugar + "</span></td>" +
                                                    '<td><span id="amount_' + ingredients[i].id + '">' + ingredients[i].amount + " g</span></td>" +
                                                    '</tr>'

                                if (ingredients[i].main){
                                    ingredient_tr += '<tr>' +
                                            '<td id="slider_tr" name="'+ ingredients[i].id +'">' +
                                                '<input type="text"' +
                                                    'class="col"' +
                                                    'id="slider"' +
                                                    'data-slider-id="slider_data"' +
                                                    'name="slider"' +
                                                    'data-provide="slider"' + 
                                                    'data-slider-min="' + ingredients[i].min * 100 + '" '+
                                                    'data-slider-max="' + ingredients[i].max * 100 + '" '+
                                                    'data-slider-step="0.1" ' + 
                                                    'data-slider-value="' + ingredients[i].amount + '" '+
                                                    'data-slider-tooltip="show"' +
                                            '</td>' +

                                            '<td colspan=5>' +
                                                    ingredients[i].name +
                                            '</td>' +

                                        '</tr>'
                                }

                                $('.recipe__right__form__ingredient-table').append(ingredient_tr);
                                var mySlider = $("#slider").slider();

                            }

                            $('.recipe__right__form__ingredient-table').append(
                                "<tr>" +
                                    '<td><strong>Součet</strong></td>'+
                                    '<td><span id="totalCalorie">' +totals.calorie+'</span></td>' +
                                    '<td><span id="totalProtein">' +totals.protein+'</span></td>' +
                                    '<td><span id="totalFat">'     +totals.fat+'</span></td>' +
                                    '<td><span id="totalSugar">'   +totals.sugar+'</span>'+'</td>' +
                                    '<td><span id="totalWeight">'  +totals.amount+'</span> g</td>' +
                                '</tr>' +
                                '<tr>' +
                                    '<td></td>'+
                                    '<td></td>'+
                                    '<td></td>'+
                                    '<td></td>'+
                                    '<td></td>'+
                                    '<td><span id="totalRatio">'+totals.ratio+'</span> : 1</td>' +
                                '</tr>'
                                );

                            // ingredients to inputs
                            for (let i = 0; i < ingredients.length; i++ ){
                                recipe__right__form__addIngredient(ingredients[i]);
                            }

                            // diet ID
                            recipe__ingredient_dietID = response.diet.id
                            $('.recipe__right__form__diet-name').text(response.diet.name);

                            // change visibility
                            recipe__right__show();

                        },
                        error: function(error) {
                            // console.log(error);
                        }
                    });
                    e.preventDefault();
                });

            /// Adding ingredient from select to list of selected ingredients
            $(document).on("submit", ".prerecipe__add-ingredient__form", function(e) {
                    $.ajax({
                        type: 'POST',
                        url: '/addIngredientAJAX',
                        data: $(this).serialize(),
                        success: function(response) {
                            var ingredient = response;
                            prerecipe__calc__form__ingredients__add(ingredient);
                            prerecipe__addIngredient__form__select__refresh();
                            prerecipe__selectedIngredients__table__add(ingredient); // gets data from form__ings
                            recipe__hideAll();
                        },
                        error: function(error) {
                            // console.log(error);prerecipe__add-ingredient__form
                        }
                    });
                    e.preventDefault();
            });


            /// Removing ingredient from list of selected ingredients
            $(function(){
                  $('.prerecipe__selected-ingredients__table').on('click','tr i.remove',function(e){
                     e.preventDefault();

                    // remove from list
                    prerecipe__calc__form__ingredients__remove($(this).parents('tr').attr('id_value'));

                    // remove table line
                    $(this).parents('tr').remove();

                    // Refresh selection
                    prerecipe__addIngredient__form__select__refresh();

                    // Hide recipe form (discard)
                    $(".recipe__right").hide();
                  });
            });

            /// Setting main ingredient
            $(function(){
                  $('.prerecipe__selected-ingredients__table').on('click','tr i.set_main',function(e){
                     e.preventDefault();

                    // set main
                    setMainIngredient($(this).parents('tr').attr('id_value'));
                  });
            });

            /// Setting fixed ingredients
            $(function(){
                  $('.prerecipe__selected-ingredients__table').on('click','tr i.set_fixed',function(e){
                     e.preventDefault();

                    // toggle fixes
                    toggleFixedIngredient($(this).parents('tr').attr('id_value'));
                  });
            });


            /// Running loader animation
            $(document).on("click", ".prerecipe__calc__form__submit", function() {
                recipe__loader__show();
            });


            /// Recalculating amounts
            $(document).on("slideStop", "#slider", function(e) {
                recipe__loader__show();

                $.ajax({
                        type: 'POST',
                        url: '/recalcRecipeAJAX',
                        data: JSON.stringify({
                            'dietID'       : recipe__ingredient_dietID,
                            'ingredients'  : prerecipe__ingredient_array,
                            'slider'       : $('#slider').val()},
                            null, '\t'), // wip not sure why
                        contentType: 'application/json;charset=UTF-8',

                        success: function(response) {

                            if (response == "False"){
                                recipe__wrong__show();
                                return;
                            }

                            // ingredients
                            for (var i = 0; i < response.ingredients.length; i++) {
                                $('#amount_'+response.ingredients[i].id).text(response.ingredients[i].amount+" g");
                                $('#calorie_'+response.ingredients[i].id).text(response.ingredients[i].calorie);
                                $('#fat_'+response.ingredients[i].id).text(response.ingredients[i].fat);
                                $('#protein_'+response.ingredients[i].id).text(response.ingredients[i].protein);
                                $('#sugar_'+response.ingredients[i].id).text(response.ingredients[i].sugar);
                            }
                            recipe__ingredient_array = response.ingredients

                            // new totals
                            $('#totalFat').text(response.totals.fat);
                            $('#totalSugar').text(response.totals.sugar);
                            $('#totalProtein').text(response.totals.protein);
                            $('#totalCalorie').text(response.totals.calorie);
                            $('#totalWeight').text(response.totals.amount);
                            $('#totalRatio').text(response.totals.ratio);
                            recipe__right__show();

                        },
                        error: function(error) {
                        }

                    });
                    e.preventDefault();
            });

            function setMainIngredient(id){
                for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                    if (prerecipe__ingredient_array[i].id == id) {
                        prerecipe__ingredient_array[i].main = true;
                        prerecipe__ingredient_array[i].fixed = false;
                    } else {
                        prerecipe__ingredient_array[i].main = false;
                    }
                }

                $('.prerecipe__selected-ingredients__table tr').removeClass('tr-mainIngredient');
                $('.prerecipe__selected-ingredients__table').find('tr[id_value = "' + id +'"] ').addClass('tr-mainIngredient')
                $('.prerecipe__selected-ingredients__table').find('tr[id_value = "' + id +'"] ').removeClass('tr-fixedIngredient')
            }

            function toggleFixedIngredient(id){
                for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                    if (prerecipe__ingredient_array[i].id == id) {
                        if (prerecipe__ingredient_array[i].fixed){
                            prerecipe__ingredient_array[i].fixed = false;
                            $('.prerecipe__selected-ingredients__table').find('tr[id_value = "' + id +'"] ').removeClass('tr-fixedIngredient');
                        }else{
                            prerecipe__ingredient_array[i].fixed = true;
                            prerecipe__ingredient_array[i].main = false;
                            $('.prerecipe__selected-ingredients__table').find('tr[id_value = "' + id +'"] ').addClass('tr-fixedIngredient');
                            $('.prerecipe__selected-ingredients__table').find('tr[id_value = "' + id +'"] ').removeClass('tr-mainIngredient');

                        }
                    }
                }
            }
        </script>
{% endblock %}

{% block content %}
	{% include('navbar.tpl') %}
        <div class="container-fluid container__main">
            <div class="row">
                <div class="prerecipe col-lg-6 col-md-12">

                    <div class="prerecipe__add-ingredient col-12">
                        <form class="prerecipe__add-ingredient__form form-inline">
                            <select class="prerecipe__add-ingredient__form__select form-control js-example-basic-single"
                            name="prerecipe__add-ingredient__form__select">
                            {% for ingredient in ingredients: %}
                                <option name='{{ingredient.name}}' value="{{ingredient.id}}">{{ingredient.name}}</option>
                            {% endfor %}
                            </select>
                            <input type="submit" class="btn btn-primary add-ingredient-btn" value="Přidat surovinu" />
                        </form>
                    </div>

                    <div class="prerecipe__selected-ingredients col-11">
                        <form class="form-group">
                            <table class="prerecipe__selected-ingredients__table table"></table>
                        </form>
                    </div>

                    <div class="prerecipe__calc col-12">
                        <form class="prerecipe__calc__form form-inline">
                            <label for="select-diet">Název diety</label>
                            <select name="select-diet" class="select-diet form-control">
                            {% for diet in diets: %}
                                <option value="{{diet.id}}">{{ diet.name }}</option>
                            {% endfor %}
                            </select>
                            <input type="submit" class=" prerecipe__calc__form__submit btn btn-primary" value="Spočítat množství!" />
                        </form>
                    </div>

                </div>

                <div class="recipe col-lg-6 col-md-12">

                    <div class="recipe__loader"></div>

                    <div class="recipe__wrong">
                        <span class="problem">Recept nelze vytvořit</span>
                    </div>

                    <div class="recipe__right">
                        <form method="post" class="recipe__right__form form-group"  action="/saveRecipeAJAX" >
                            <label for="recipe__right__form__name-input">Název receptu</label>
                            <input type="text" name="recipe__right__form__name-input" required class="form-control"/>

                            <table class="recipe__right__form__ingredient-table table">
                                <tr>
                                    <th>Název</th>
                                    <th>Kalorie</th>
                                    <th>Bílkovina</th>
                                    <th>Tuk</th>
                                    <th>Sacharidy</th>
                                    <th>Množství</th>
                                    <th></th>
                                </tr>
                            </table>

                            <div class="form-inline">
                                <select name="recipe__right__form__size-select" class="form-control col-3">
                                    <option value="big">Velké jídlo</option>
                                    <option value="small">Malé jídlo</option>
                                </select>

                                <span class="col-4">Dieta: <span class="recipe__right__form__diet-name"></span></span>
                                <input type="submit" class="btn btn-primary col-4 " value="Uložit mezi recepty" />
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
{% endblock %}
