// Fill these in once the accounts exist. Nothing else needs editing.
window.FJ = {
  // Klaviyo: Settings > Account > API keys > "Public API key / Site ID" (6 characters), and the list id from Lists & segments
  klaviyoCompanyId: "",
  klaviyoListId: "",
  // used only until Klaviyo is set: signups are emailed here via FormSubmit
  fallbackEmail: "iudiciumfinale@gmail.com",
  // Stripe Payment Links, one per product + size. Tracksuit: one link per hoodie-size/joggers-size pair, key "M/L" etc.
  stripe: {
    "hoodie": { S: "", M: "", L: "", XL: "" },
    "joggers": { S: "", M: "", L: "", XL: "" },
    "polo-black": { S: "", M: "", L: "", XL: "" },
    "polo-white": { S: "", M: "", L: "", XL: "" },
    "tracksuit": {}
  }
};
