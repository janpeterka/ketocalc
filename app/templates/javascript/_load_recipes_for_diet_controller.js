Stimulus.register("load-recipes-for-diet", class extends Controller {
    static get targets() {
        return ["diets", "recipes", "submit"]
    }

    connect() {
        this.load_recipes();
    }

    load_recipes(){
        this.submitTarget.disabled=true;
        this.submitTarget.value="Přidat recept";

        fetch("{{ url_for('RecipesView:load_recipes_AJAX') }}",{
            method: 'POST',
            body: JSON.stringify({'diet_id' : this.dietsTarget.value}),
            headers: {'Content-Type': 'application/json,charset=UTF-8'}}
        ).then((response) => {
            return response.json(); }
        ).then((response) => {
            this.clear_recipe_options();
            for (let i = 0, recipe; recipe = response[i]; i++) {
                this.add_recipe_option(recipe);
            }

            if (response.length == 0) {
                this.submitTarget.value="Není vybraný recept";
            } else {
                this.submitTarget.disabled=false;
            }

        }).catch((error) => {
            console.error('Error:', error);
        });
    }


    clear_recipe_options(){
        this._remove_options(this.recipesTarget);
    }

    add_recipe_option(recipe){
        var option = document.createElement('option');
        option.value = recipe.id;
        option.innerHTML = recipe.name;
        this.recipesTarget.appendChild(option);
    }

    _remove_options(selectElement) {
       var i, L = selectElement.options.length - 1;
       for(i = L; i >= 0; i--) {
          selectElement.remove(i);
       }
    }


});
