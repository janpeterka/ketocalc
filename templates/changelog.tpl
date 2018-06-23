{% extends "base.tpl" %}
{% block title %}
    Changelog
{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
		<div class="changelog">
			<h3>Beta</h3>
			<h6>v2</h6>
			<ul>
				<i>
					<li>v2.3.1 (ve vývoji)
						<ul>
							<li><strong>přepočítávání receptu do jiné diety</strong></li>
							<li>nápověda</li>
						</ul>
					</li>
				</i>

				<li>v2.3 <i>8.6.2018</i>
					<ul>
						<li>Fixní suroviny - počítání s více surovinami</li>
						<li>Úprava uživatele - jméno, heslo <i>(23.6.2018)</i></li>
					</ul>
				</li>

				<li>v2.2.1 <i>24.4.2018</i>
					<ul>
						<li>archivování diety</li>
						<li>lepší hlavní surovina (s podbarvením)</li>
					</ul>
				</li>

				<li>v2.2
					<ul>
						<li>tisk receptu</li>
						<li>úprava suroviny, receptu, diety</li>
						<li>feedback formulář</li>
						<li>přidání kalorií k surovinám</li>
						<li>výpis všech receptů k tisku</li>
						<li>lepší přidávání nových receptů</li>
					</ul>
				</li>
				<li>v2.1
					<ul>
						<li>možnost nastavení množství 4. suroviny </li>
						<li>ubrání chybně přidané suroviny (Nový recept)</li>
						<li>nastavení velkého a malého jídla</li>
					</ul>
				</li>
				<li>v2.0
					<ul>
						<li>výpočet pro 4 suroviny</li>
						<li>vylepšený formulář přidání receptu</li>
					</ul>
				</li>
			</ul>

			<h3>Alpha</h3>
			<h6>v1</h6>
			<ul>
				<li>v1.0
					<ul>
						<li>changelog</li>
						<li>podpora diakritiky</li>
						<li>mazání receptů, surovin, diet</li>
					</ul>
				</li>
				<li>v1.1
					<ul>
						<li>seznamy všech osobních receptů, surovin, diet</li>
						<li>drobné úpravy designu</li>
					</ul>
				</li>
				<li>v1.2
					<ul>
						<li>výpočet pro 2 suroviny</li>
						<li>výpočet pro 3 suroviny</li>
						<li>nahlášení nereálného receptu</li>
					</ul>
				</li>
			</ul>

			

			

			<i>v3 (ve vývoji)
				<ul>
					<li>výpočet pro 5 surovin</li>
				</ul>
			</i>
		</div>
{% endblock %}