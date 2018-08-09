{% extends "base.tpl" %}
{% block title %}
    Feedback - Dejte nám vědět!
{% endblock %}

{% block style %}
    
{% endblock %}

{% block script %}
	
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
    <div class="container">
            <form class="form-control form-group col-6" method="POST" action="/feedback" enctype = "multipart/form-data">
                <label for="type">Vyberte typ reakce</label>
                <select name="type" class="form-control">
                    <option value="bug">Chyba v programu</option>
                    <option value="ux">Problém s používáním uživatelského rozhraní</option>
                    <option value="suggestion">Doporučení na zlepšení aplikace</option>
                </select>
                
                <label for="message">Popište<span style="color: black">*</span></label>
                <input type="text" name="message" class="form-control" required oninvalid="this.setCustomValidity('Popište situaci')"
                    oninput="setCustomValidity('')"  /> 
                
                <label for="sender">Váš email (pro případ nutnosti upřesnění)</label>
                <input type="text" name="sender" class="form-control" />
                
                <label for="file">Screenshot s problémem</label>
                <input type="file" name="file" class="form-control screenshot_file" value="Nahrajte screenshot">
                
                <input type="submit" class="btn btn-primary form-control" value="Poslat reakci" />
            </form>
    </div>
{% endblock %}

