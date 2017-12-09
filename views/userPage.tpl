<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>Vítejte {{username}}</title>
    % include('bootstrap.tpl')
    % include('styleBody.tpl')

    <script type="text/javascript">
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
                                // $('#recipeList').append("<tr><td>" + recipes[i].id + "</td><td>" + recipes[i].name + "</td><td>" + recipes[i].sugar+ "</td><td>" + recipes[i].fat + "</td><td>" + recipes[i].protein + "</td></tr>");
                            }
                        },
                        error: function(error) {
                            console.log(error);
                        }

                    });
                    e.preventDefault();
            });
    </script>
</head>
<body>
    % include('navbar.tpl')

    <div class="col-sm-6">
        Seznam receptů:
        <ul id="recipeList">
        %for recipe in recipes:
            <li><a href="/recipe={{recipe.id}}">{{recipe.name}}</a></li>
        %end
        </ul>
    </div>

    <div class="form-inline col-sm-4">
        <form id="selectDietForm" method="POST" action="/selectDietAJAX">
            <select name="selectDiet" class="form-control">
                %for diet in diets:
                    <option value="{{diet.id}}">{{diet.name}}</option>
                %end
            </select>
            <input id="ajaxButton" type="submit" class="btn btn-primary" value="Změnit dietu" />
        </form>
    </div>

</body>
</html>