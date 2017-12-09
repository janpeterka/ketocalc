<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Dieta: {{diet.name}}</title>
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

    <div class="container row">
         <div class="col-8">
            <label for="recipes">Recepty</label>
            <ul name="recipes">
            % for recipe in recipes:
                    <li><a href="/recipe={{recipe.id}}">{{recipe.name}}</a></li>
            % end 
            </ul>
        </div>  
        <div class="col-4">
            <table id="ingredients" class="table">
                <tr>
                    <th>Cukr</th>
                    <th>Tuk</th>
                    <th>Bílkovina</th>
                </tr>
                <tr>
                    <td>{{diet.sugar}}</td>
                    <td>{{diet.fat}}</td>
                    <td>{{diet.protein}}</td>
                </tr>
            </table>
        </div>     
        
    </div> 

</body>
</html>