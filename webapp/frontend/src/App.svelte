<script>
  import { Router, Route } from "svelte-routing";
  import { QueryClient, QueryClientProvider } from "@sveltestack/svelte-query";

  import Home from "./routes/Home.svelte";
  import Vlam from "./routes/Vlam.svelte";
  import Spel from "./routes/Spel.svelte";
  import OverOns from "./routes/OverOns.svelte";
  import Footer from "./components/Footer.svelte";
  import Privacy from "./routes/Privacy.svelte";
  import Gevonden from "./routes/Gevonden.svelte";
  import VlamQRCode from "./routes/VlamQRCode.svelte";
  import Navigation from "./components/Navigation.svelte";
  import ScratchSpellen from "./routes/ScratchSpellen.svelte";

  export let url = "";
  const queryClient = new QueryClient();
</script>

<QueryClientProvider client={queryClient}>
  <Router {url}>
    <div class="header">
      <Navigation />
    </div>
    <div class="content">
      <Route path="/het-spel" component={Spel} />
      <Route path="/gevonden/:id" component={Gevonden} />
      <Route path="/vlammetjes/:id/qrcode" component={VlamQRCode} />
      <Route path="/vlammetjes/:id" component={Vlam} />
      <Route path="/scratch-spelletjes" component={ScratchSpellen} />
      <Route path="/about" component={OverOns} />
      <Route path="/privacy" component={Privacy} />
      <Route path="/"><Home /></Route>
    </div>
    <div class="footer">
      <Footer />
    </div>
  </Router>
</QueryClientProvider>

<style>
  .header {
    background: var(--cd-blue);
  }

  .content {
    flex-grow: 1;
  }

  .footer {
    min-height: 50px;
    background: var(--cd-blue);
  }
</style>
