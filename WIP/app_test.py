from bottle import route, request, run, get


@route('/form')
def construct_form():
    return '''

<!DOCTYPE html>
<html>
<head>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
    <script type="text/javascript">
        $(document).ready(function() {
            $('form').submit(function(e) {
                $.ajax({
                    type: 'POST',
                    url: '/ajax',
                    data: $(this).serialize(),
                    success: function(response) {
                        $('#ajaxP').html(response);
                    }
                });
                e.preventDefault();
            });
        });
    </script>
</head>
<body>
    <form method="POST" action="/ajax">
        <input id="ajaxTextbox" name="text" type"text" />
        <input id="ajaxButton" type="button" value="Submit" />
    </form>
    <p id="ajaxP">Nothing to see here.</p>
</body>
</html>

    '''


@route('/ajax', method='POST')
def ajaxtest():
    theText = request.forms.text
    if theText:
        return theText
    return "You didn't type anything."


run(host='localhost', port='8080')
