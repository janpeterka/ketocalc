{% extends "base.html.j2" %}
{% block title %}
    Nápověda
{% endblock %}

{% block style %}{% endblock %}

{% block content %}
    <div>
    	<h1>FAQ</h1>
    	<ul>
    		<li>
    			<p class="faq-question">Nefunguje mi ketokalkulačka</p>
    			<p class="faq-answer">Nahlašte problém na <a href="{{ url_for('SupportView:feedback') }}}">této záložce</a>. Než se problém vyřeší, používejte <a href="https://ketocalc.herokuapp.com/">stabilní verzi</a></p>
    		</li>
    	</ul>
    	
    </div>
	<div name="newrecipe">
		<h1> Nový recept </h1>
		Typy surovin:
		<ul>
			<li class="tr-mainIngredient">Hlavní surovina <i class="fa fa-hospital-symbol"></i></li>
				<ul>
					<li>Hlavní surovina může být maximálně jedna</li>
					<li>Množství hlavní suroviny bude možné upravovat na stránce výpočtu</li>
				</ul>
			<li class="tr-fixedIngredient">Fixní surovina <i class="fa fa-thumbtack"></i></li>
				<ul>
					<li>Fixních surovin může být libovolné množství</li>
					<li>Množství fixních surovin zůstává pořád stejné</li>
				</ul>
			<li>Počítaná surovina</li>
				<ul>
					<li>Počítaných surovin spolu s hlavní surovinou může být 3-4</li>
					<li>Množství se přepočítává podle množství hlavní suroviny</li>
				</ul>
		</ul>
		Surovinu je možné odebrat kliknutím na ikonu <i class="fa fa-times fa-2x"></i>


	</div>	
{% endblock %}
