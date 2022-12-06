<script>
	import {Link} from "svelte-routing";
</script>

<div class="jumbotron split">
	<div>
		<h1>CoderDojo Halle Vlamt!</h1>
		<h2>Een interactief stadsspel voor de feestdagen!</h2>
	</div>
	<div>
		<img
			src="/images/vlammetje.gif"
			alt="een brandend ledvlammetje aan de gevel"
		/>
	</div>
</div>

<div class="features">
	<div class="feature">
		<h3><span class="circle">1</span> Zoek het vlammetje</h3>
		<p>
			Zoek op de kaart de blauwe cirkels. Wandel/fiets of hinkel naar die
			locatie en zoek de vlammende lichtjes.
		</p>
	</div>
	<div class="feature">
		<h3><span class="circle">2</span> Scan de QR code</h3>
		<p>
			Aan het vlammetjes vind je een poster, scan de QR code met je smartphone.
			Zo kom je op de pagina van het vlammetje terecht.
		</p>
	</div>
	<div class="feature">
		<h3><span class="circle">3</span> Unlock de besturing</h3>
		<p>
			Je kan nu de animatie van de ledjes aansturen. Druk op 1 van de knoppen en
			zie hoe de ledjes veranderen!
		</p>
	</div>
</div>

<div class="team">
	<p>
		Dit interactieve stadspel werd gemaakt door de coaches en de ninja's van
		CoderDojo Halle.
	</p>
	<p>
		<img
		src="/images/cdjh-team-1.jpeg"
		alt="het coderdojo halle team aan de soldeertafel"
	/>
	<img
	src="/images/cdjh-team-2.jpeg"
	alt="het coderdojo halle team tijdens een show en tell"
/>
<img
src="/images/cdjh-team-3.jpeg"
alt="het coderdojo halle team aan de soldeertafel"
/>
	</p>
	<p>
		Bij CoderDojo kunnen meisjes en jongens van 7 t/m 18 jaar leren
		programmeren. Dit wordt helemaal gratis verzorgd door vrijwilligers! <br />
		In Halle komen we 1x per maand samen, in het Vondel. <br /> Interesse? Kijk
		snel op de website van
		<a
			href="https://www.coderdojobelgium.be/nl"
			target="_blank"
			rel="noreferrer">CoderDojo Belgium!</a
		>
	</p>
	<p>Op onze <Link to="/scratch-spelletjes">spelletjespagina</Link> vind je alvast enkele online games gemaakt door onze ninja's.</p>

</div>

<style>
	h1 {
		text-transform: capitalize;
	}
	p {
		line-height: 150%;
	}

	.features {
		display: flex;
		flex-direction: row nowrap;
		padding-top: 20px;
		text-align: justify;
		padding-left: 20px;
		padding-right: 20px;
	}

	.feature {
		flex: 1;
		padding-left: 20px;
		padding-right: 20px;
		border: 2px solid var(--cd-blue);
		border-radius: 20px;
		margin-right: 10px;
		text-align: justify;
	}
	.feature:last-of-type {
		margin-right: 0;
	}

	.feature h3 {
		text-align: center;
	}

	.feature p {
		font-size: 110%;
	}

	.team p {
		font-size: 120%;
	}

	span.circle {
		background: var(--cd-yellow);
		border-radius: 50%;
		-moz-border-radius: 50%;
		-webkit-border-radius: 50%;
		color: white;
		display: inline-block;
		font-weight: bold;
		line-height: 40px;
		margin-right: 5px;
		text-align: center;
		width: 40px;
	}

	.split {
		display: flex;
		flex-direction: row nowrap;
		align-items: center;
	}

	.split div {
		flex-grow: 1;
	}
	
	img {
		border-radius: 50%;
	}

	.team img {
		width: 200px;
		height: 200px;
	}

	/* small and medium screens */
	@media all and (max-width: 800px) {
		.features {
			flex-direction: column;
		}
		.feature {
			width: 100%;
		}
	}
</style>
