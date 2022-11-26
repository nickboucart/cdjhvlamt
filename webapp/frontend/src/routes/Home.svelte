<script>


</script>

<div class="jumbotron">
<h1>CDJHVlamt <br /> Een interactief stadsspel voor de feestdagen!</h1>
<!-- <h2>Zoek de vlammetjes, scan de QR code en unlock de besturing het vlammetje</h2> -->
</div>

<div class="features">
<div class=feature>
	<h3>Zoek het vlammetje</h3>
	<p>Zoek op de kaart de blauwe cirkels. Wandel/fiets of hinkel naar die locatie en zoek de vlammende lichtjes.</p>
</div>
<div class=feature>
	<h3>Scan de QR code</h3>
	<p>Aan het vlammetjes vind je een poster, scan de QR code met je smartphone. Zo kom je op de pagina van het vlammetje terecht.</p>
</div>
<div class=feature>
	<h3>Unlock de besturing</h3>
	<p>Je kan nu de animatie van de ledjes aansturen. Druk op 1 van de knoppen en zie hoe de ledjes veranderen!</p>
</div>
</div>

<style>
.jumbotron {
	background: var(--cd-black);
	width: 80%;
	margin: auto;
	border-radius: 20px;
	color: var(--cd-yellow);
	padding: 10px 50px;
}

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
	flex-grow:1;
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

/* small and medium screens */
@media all and (max-width: 800px) { 
	.jumbotron {
		width: 100%;
		border-radius: 0;
	}

	.features {
		flex-direction: column;
	}
	.feature {
		width: 100%;
	}
}

</style>