<script>
</script>

<div class="jumbotron">
	<h1>
		CoderDojo Halle Vlamt <br /> Een interactief stadsspel voor de feestdagen!
	</h1>
	<!-- <h2>Zoek de vlammetjes, scan de QR code en unlock de besturing het vlammetje</h2> -->
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

<style>


	h1 {
		text-transform: capitalize;
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
		flex-grow: 1;
		padding-left: 20px;
		padding-right: 20px;
		border: 2px solid var(--cd-blue);
		border-radius: 20px;
		margin-right: 10px;
	}
	.feature:last-of-type {
		margin-right: 0;
	}

	.feature h3 {
		text-align: center;
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
