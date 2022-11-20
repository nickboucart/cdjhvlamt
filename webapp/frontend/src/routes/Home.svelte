<script>
	import { onMount } from "svelte";
	import { Link } from "svelte-routing";
	import VlamMap from "../components/VlamMap.svelte";
	import { getData } from "../helpers/APIHelpers";

	let vlammetjes = [];

	// onMount(async () => {
	// 	vlammetjes = await getData('/vlammekes');
	// });

	async function getVlammetjes() {
		vlammetjes = await getData("/vlammekes");
		return vlammetjes;
	}
</script>

<div>
	<div>
		{#await getVlammetjes()}
			<p>data laden...</p>
		{:then vlammetjes}
			<ul>
				{#each vlammetjes as { thingName, attributes }, i}
					<li>
						<Link to={"/vlammetjes/" + thingName}
							>Vlam van {attributes.eigenaar}</Link
						>
					</li>
				{/each}
				<VlamMap vlammetjes={vlammetjes} />
			</ul>
		{/await}
	</div>
</div>
