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
        </tr>

        {% for ingredient in ingredients %}
            {% if ingredient.main %}
                <tr class="tr-mainIngredient">
            {% elif ingredient.fixed %}
                <tr class="tr-fixedIngredient">
            {% else %}
                <tr class="tr-variableIngredient">
            {% endif %}

                    <td>{{ ingredient.name }} </td>
                    <td><span id="calorie_{{ingredient.id}}">{{ ingredient.calorie }}</span></td>
                    <td><span id="protein_{{ingredient.id}}">{{ ingredient.protein }}</span></td>
                    <td><span id="fat_{{ingredient.id}}">{{ ingredient.fat }}</span></td>
                    <td><span id="sugar_{{ingredient.id}}">{{ ingredient.sugar }}</span></td>
                    <td><span id="amount_{{ingredient.id}}">{{ ingredient.amount }} g</span></td>
                </tr>

            {% if ingredient.main %}
                <tr>
                    <td id="slider_tr" name="{ingredient.id}">
                        <input type="text" class="col" id="slider" data-slider-id="slider_data" name="slider" data-provide="slider" data-slider-min="{{ingredient.min * 100}}" data-slider-max="{{ingredient.max * 100}}" data-slider-step="0.1" data-slider-value="{{ingredient.amount}}" data-slider-tooltip="show">
                    </td>

                    <td colspan=5>
                        {{ingredient.name}}
                    </td>

                </tr>
            {% endif %}
        {% endfor %}

        <tr>
            <td><strong>Součet</strong></td>
            <td><span id="totalCalorie">{{ totals.calorie }}</span></td>
            <td><span id="totalProtein">{{ totals.protein }}</span></td>
            <td><span id="totalFat">{{ totals.fat }}</span></td>
            <td><span id="totalSugar">{{ totals.sugar }}</span></td>
            <td><span id="totalWeight">{{ totals.amount }}</span> g</td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td><span id="totalRatio">{{ totals.ratio }}</span> : 1</td>
        </tr>
    </table>

    <div class="form-inline">
        <select name="recipe__right__form__size-select" class="form-control col-3">
            <option value="big">Velké jídlo</option>
            <option value="small">Malé jídlo</option>
        </select>

        <span class="col-4">Dieta: {{ diet.name }}</span>
        {% if not trialrecipe %}
            <input type="submit" class="btn btn-primary col-4 " value="Uložit mezi recepty" />
        {% else %}
            <input type="button" onclick='trialSaveConfirm()' class="btn btn-primary col-4 " value="Uložit mezi recepty" />
        {% endif %}
    </div>
</form>