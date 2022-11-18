<script>
	import { postData } from "../helpers/APIHelpers";
	console.log($$props);

async function onClick(animatie) {
	const vlamNaam = $$props.id;
	await postData('/vlammekes/' + vlamNaam,  {"animatie": animatie});
	};



</script>

<div>
	<h1>Individuele Vlam</h1>
	<h2>Toon de details van {$$props.id}</h2>
<p>Stuur het vlammetje aan:
	<button on:click={() => onClick("fire")}>vlam animatie</button>
	<button on:click={() => onClick("conjunction")}>andere animatie</button>

</p>
</div>
