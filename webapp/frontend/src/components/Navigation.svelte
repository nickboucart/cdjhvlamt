<script>
	import { Link } from "svelte-routing";

</script>

<ul class="navigation">
	<li><Link to="/">Home</Link></li>
	<li><Link to="/het-spel">Speel het spel</Link></li>
	<li><Link to="/about">Over Ons</Link></li>
</ul>


<style>
.navigation {
	display: flex;
	flex-flow: row wrap;
	justify-content: center;
	align-items: center;
	list-style: none;
	height: 100%;
	padding: 0px;
	margin: 0;
	
}
.navigation li {
	padding: 10px;
	margin: 0px;
	flex-grow: 1;
}

/* Medium screens */
@media all and (max-width: 800px) {
  .navigation {
    /* When on medium sized screens, we center it by evenly distributing empty space around items */
    justify-content: space-around;
  }
}

/* Small screens */
@media all and (max-width: 500px) {
  .navigation {
    /* On small screens, we are no longer using row direction but column */
    flex-direction: column;
  }
}
</style>