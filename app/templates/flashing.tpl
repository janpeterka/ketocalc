{% with messages = get_flashed_messages(with_categories=true) %}
  {# {% if messages %} #}
  <div class="flashes container alert alert-light" role="alert">
    <ul>
    {% for category, message in messages %}
      <li class='{{ category }}'>{{ message }}</li>
    {% endfor %}
    </ul>
  </div>
  {# {% endif %} #}
{% endwith %}