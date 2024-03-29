  Stimulus.register("simple-calculator", class extends Controller {
    static get targets() {
      return [
        "baseSelect",
        "select", "ingredientTable", "recipeDiet", "recipeName",
        "totals"
        ]
    }

    connect() {
    }

    _refresh_select(){
      this.selectTarget.innerHTML = this.baseSelectTarget.innerHTML;

      for (let i = 0, ingredient; ingredient = this._get_currently_selected()[i]; i++) {
        let option = this.selectTarget.querySelector("option[value='" + ingredient.id + "']");
        option.remove();
      }
    }

    // _float_to_fixed(data){
    //   return parseFloat(data).toFixed(2)
    // }

    add_ingredient(e){
      e.preventDefault();

      if (this.selectTarget.value == false){return false;}
      else{
        fetch("{{ url_for('RecipeCreatorView:addIngredientWithAmount') }}",{
          method: 'POST',
          body: JSON.stringify({'ingredient_id' : this.selectTarget.value}),
          headers: {'Content-Type': 'application/json,charset=UTF-8'}}
        ).then((response) => { return response.json(); }
        ).then((response) => {
          $(this.ingredientTableTarget).append(response['template_data']);
          this._refresh_select();
          this.calculate_recipe();
        });
      }
    }

    remove_ingredient(event){
      var id = event.target.parentNode.dataset.id

      for (let i = 0, row; row = this.ingredientTableTarget.rows[i]; i++) {
          if (row.dataset.id == id){
              row.remove()
          }
      }
      this._refresh_select();
      this.calculate_recipe();
    }

    _row_to_ingredient(row){
      var ingredient = {}
      ingredient['id'] = row.dataset.id
      ingredient['name'] = row.dataset.name
      ingredient['calorie'] = row.dataset.calorie
      ingredient['fat'] = row.dataset.fat
      ingredient['protein'] = row.dataset.protein
      ingredient['sugar'] = row.dataset.sugar
      ingredient['amount'] = $(row).find("input").first().val()

      return ingredient
    }

    _get_currently_selected(){
      return this._get_ingredients_from_table(this.ingredientTableTarget)
    }

    _get_ingredients_from_table(table){
      var ingredients = [];

      for (let i = 0, row; row = table.rows[i]; i++) {
        if ("id" in row.dataset){
          let ingredient = this._row_to_ingredient(row)
          ingredients.push(ingredient);
        }

      }
      return ingredients;
    }

    calculate_recipe(e){
      if (e != null){e.preventDefault();}

      var selected_ingredients = this._get_currently_selected()

      var totals = {
        "sugar": 0,
        "protein": 0,
        "fat": 0,
        "calorie": 0,
        "amount": 0
      }

      for (let i = 0, ingredient; ingredient = selected_ingredients[i]; i++) {
          totals["sugar"] += parseFloat(ingredient["sugar"]) * parseFloat(ingredient["amount"] / 100)
          totals["protein"] += parseFloat(ingredient["protein"]) * parseFloat(ingredient["amount"] / 100)
          totals["fat"] += parseFloat(ingredient["fat"]) * parseFloat(ingredient["amount"] / 100)
          totals["calorie"] += parseFloat(ingredient["calorie"]) * parseFloat(ingredient["amount"] / 100)
          totals["amount"] += parseFloat(ingredient["amount"])
      }

      totals["ratio"] = parseFloat(totals["fat"] / (totals["protein"] + totals["sugar"]))

      this._set_totals(totals)
    }

  save_recipe(e){
    e.preventDefault();
    fetch("{{ url_for('RecipeView:saveRecipeAJAX') }}", {
      method: 'POST',
      body: JSON.stringify({
        'ingredients' : this._get_currently_selected(),
        'dietID' : this.recipeDietTarget.value,
        'name' : this.recipeNameTarget.value,
      }),
      headers: {'Content-Type': 'application/json,charset=UTF-8'},
    })
    .then((response) => {
      return response.text(); })
    .then((response) => {
      var pathname = window.location.pathname.split("/")[0];
      window.location.replace(pathname + response);
    })
  }

  _set_totals(totals){
    var fields = ["calorie", "protein", "fat", "sugar", "amount"]
    for (let i = 0, field; field = fields[i]; i++) {
      this.totalsTarget.querySelector('[data-field=' + field + ']').innerHTML = _float_to_fixed(totals[field])
    }

    this.totalsTarget.querySelector('[data-field="ratio"]').innerHTML = "<em>" + _float_to_fixed(totals["ratio"]) + " : 1</em>"
  }

});

