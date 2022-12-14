import { Api, ViteStaticSite } from "@serverless-stack/resources";

export function MyStack({ app, stack }) {
  const api = new Api(stack, "api", {
    defaults: {
      throttle: {
        burst: 5,
        rate: 10
      },
      function: {
        timeout: 3
      }
    },
    customDomain: {
      domainName:
        app.stage === "prod" ? "api.cdjhvlamt.be" : `api-${app.stage}.cdjhvlamt.be`,
    },
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

  const siteConfig = {
    path: "frontend",
    environment: {
      // Pass in the API endpoint to our app
      VITE_APP_API_URL: app.stage === 'prod' ? api.customDomainUrl : api.url,
    },
  }

  const customDomain = {
    domainName: "cdjhvlamt.be",
    domainAlias: "www.cdjhvlamt.be",
  };

  if (app.stage === 'prod') {
    siteConfig.customDomain = customDomain;
  }

  // Deploy our Svelte app
  const site = new ViteStaticSite(stack, "SvelteJSSite", siteConfig);

  // Show the URLs in the output
  stack.addOutputs({
    SiteUrl: app.stage === 'prod' ? site.customDomainUrl : site.url,
    ApiEndpoint: app.stage === 'prod' ? api.customDomainUrl : site.url,
  });


}
