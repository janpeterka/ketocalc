{% with messages = get_flashed_messages() %}
  {% if messages %}
  <div class="flashes container alert alert-light" role="alert">
    <ul>
    {% for message in messages %}
      <li style="list-style-type: none; text-align: center; color: #101010">{{ message }}</li>
    {% endfor %}
    </ul>
  </div>
  {% endif %}
{% endwith %}