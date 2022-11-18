<script>
import { onMount } from 'svelte';
import {  Link } from "svelte-routing";
import { getData } from "../helpers/APIHelpers";

let vlammetjes = [];

onMount(async () => {
	vlammetjes = await getData('/vlammekes');
});

</script>

<div>
	<div>
		<ul>
		 {#each vlammetjes as { naam, vlamnaam }, i }
		 <li> <Link to={'/vlammetjes/' + 'cdjhvlamt-71373'}>Vlam van {naam}</Link></li>
		 {/each}
		</ul>
		 <!-- <VlamMap /> -->
	 </div>

</div>


