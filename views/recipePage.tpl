<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Recept</title>
    % include('bootstrap.tpl')
    % include('styleBody.tpl')

    <!-- <script type="text/javascript">
        $(document).on("submit", "#selectDietForm", function(e) {
            $.ajax({
                type: 'POST',
                url: '/selectDietAJAX',
                data: $(this).serialize(),
                success: function(response) {
                    var recipes = response.array;
                    // console.log(recipes);
                    // console.log(recipes[0]);
                    // console.log(recipes[0].id);

                    var dietID = response.dietID[0];
                    // recipes to table
                    $('#recipeList').empty();
                    // $('#recipeList').append("<label for='recipeList'>" + dietID + "</label>");
                    for (i = 0; i<response.array.length; i++ ){
                        console.log(recipes[i].name);
                        $('#recipeList').append("<li><a href='/recipe=" + recipes[i].id + "'>" + recipes[i].name + "</a></li>");
                    }
                },
                error: function(error) {
                    console.log(error);
                }

            });
            e.preventDefault();
        });
    </script> -->
</head>
<body>
    % include('navbar.tpl')
    <div class="col-6">
        <span>{{recipe.name}}</span>
        <table id="ingredients" class="table">
            <tr>
                <th>ID</th>
                <th>Název</th>
                <th>Bílkovina</th>
                <th>Tuk</th>
                <th>Sacharidy</th>
                <th>Množství</th>
            </tr>
            % for ingredient in ingredients:
                <tr>
                    <td>{{ingredient.id}}</td>
                    <td>
                        <a href="/ingredient={{ingredient.id}}">{{ingredient.name}}</a>
                    </td>
                    <td>{{ingredient.protein}}</td>
                    <td>{{ingredient.fat}}</td>
                    <td>{{ingredient.sugar}}</td>
                    <td>{{ingredient.amount}}</td>
                </tr>
            % end     
        </table>

        <form id="removeRecipe" action="/recipe={{recipe.id}}/remove" method="post" accept-charset="utf-8">
            <input id="ajaxButton" type="submit" class="btn btn-danger" value="Smazat recept" />
        </form>
    </div>


</body>
</html>