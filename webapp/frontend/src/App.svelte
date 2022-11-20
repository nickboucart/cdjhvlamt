<script>
  import { Router, Link, Route } from "svelte-routing";
  import Home from "./routes/Home.svelte";
  import Vlammetjes from "./routes/Vlammetjes.svelte";
  import Vlam from "./routes/Vlam.svelte";
  import OverOns from "./routes/OverOns.svelte";
  import Footer from "./components/Footer.svelte";
  import Privacy from "./routes/Privacy.svelte";

  // import VlamMap from "./components/VlamMap.svelte";
  
  export let url = "";

  </script>
  
  
  <Router url="{url}">
    <nav>
      <Link to="/">Home</Link>
      <Link to="/vlammetjes">De Vlammetjes</Link>
      <Link to="/about">Over Ons</Link>
    </nav>
    <div>
      <Route path="vlammetjes/:id" component="{Vlam}" />
      <Route path="vlammetjes" component="{Vlammetjes}" />
      <Route path="about" component="{OverOns}" />
      <Route path="privacy" component="{Privacy}" />
      <Route path="/"><Home /></Route>
    </div>
    <Footer />
  </Router>