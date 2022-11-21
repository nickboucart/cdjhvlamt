import { Api, ViteStaticSite } from "@serverless-stack/resources";

export function MyStack({ app, stack }) {
  const api = new Api(stack, "api", {
    cors: true,
    routes: {
      "POST /vlammekes/{id}": {
        function: {
          handler: "functions/vlammetjes.update",
          permissions: ['iot']
        }
      },
      "GET /vlammeke/{id}": {
        function: {
          handler: "functions/vlammetjes.get",
          permissions: ['iot']
        }
      },
      "GET /vlammekes": {
        function: {
          handler: "functions/vlammetjes.list",
          permissions: ['iot']
        }
      }
    }
  });


  // Deploy our Svelte app
  const site = new ViteStaticSite(stack, "SvelteJSSite", {
    path: "frontend",
    customDomain: {
      domainName:
        app.stage === "prod" ? "cdjhvlamt.be" : `${app.stage}.cdjhvlamt.be`,
      domainAlias: app.stage === "prod" ? "www.cdjhvlamt.be" : undefined,
    },
    environment: {
      // Pass in the API endpoint to our app
      VITE_APP_API_URL: api.url,
    },
  });

  // Show the URLs in the output
  stack.addOutputs({
    SiteUrl: site.url,
    ApiEndpoint: api.url,
  });


}
