Stimulus.register("recipe-reactions", class extends Controller {
    
    static get targets() {
        return ["recipes"]
    }

    connect() {
        this.public = (this.recipesTarget.dataset.public == "True") ? true : false
        this.add_reaction_buttons();
    }

    add_reaction_buttons() {
        for (let i = 0, recipe; recipe = this.recipesTarget.children[i]; i++) {
            this._set_recipe_icon(recipe)
        }
    }

    toggle_reaction(event){
        var recipe = event.target.parentNode.parentNode
        fetch("{{ url_for('RecipeView:toggle_reaction_AJAX') }}",{
            method: 'POST',
            body: JSON.stringify({'recipe_id' : recipe.dataset.recipeId}),
            headers: {'Content-Type': 'application/json,charset=UTF-8'}}
        ).then((response) => {
            return response.json(); }
        ).then((response) => {
            recipe.dataset.reaction=response
            this._set_recipe_icon(recipe, true)
        });
    }

    _set_recipe_icon(recipe, from_toggle=false){
        var icon_cell = recipe.children[recipe.children.length - 2]
        // remove old icon
        if (icon_cell.getElementsByTagName('i').length > 0) {
            icon_cell.getElementsByTagName('i')[0].remove()
        }

        if (from_toggle) {
            this._set_recipe_count(recipe)
        }

        var icon_type = (recipe.dataset.reaction == "true") ? "full" : "empty" 
        var icon = this._heart_icon(recipe, icon_type)

        icon_cell.innerHTML = icon.outerHTML
    }

    _set_recipe_count(recipe){
        var last_cell = recipe.children[recipe.children.length - 1]

        if (recipe.dataset.reaction == "true"){
            last_cell.getElementsByTagName('span')[0].innerHTML++;
        } else if (recipe.dataset.reaction == "false") {
            last_cell.getElementsByTagName('span')[0].innerHTML--;
        }

    }


    _heart_icon(recipe, type){
        var icon = document.createElement("i")
        icon.className = "fa-heart color-red"
        icon.dataset.recipeId = recipe.dataset.recipeId
        if (this.public) {
            icon.style.cursor = "not-allowed"
        } else {
            icon.dataset.action = 'click->recipe-reactions#toggle_reaction'
        }

        if (type == "full") {
            icon.classList.add('fas')
        } else if (type == "empty") {
            icon.classList.add('far')
        }

        return icon
    }

});