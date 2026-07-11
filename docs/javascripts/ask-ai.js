(function () {
  function buildPrompt(ai) {
    var pageUrl = window.location.href;
    var pageTitle = document.title.replace(/ - Plainsight Playbook$/, "");
    var greeting = ai === "chatgpt" ? "Hi ChatGPT!" : "Hi Claude!";
    return (
      greeting +
      " Can you please read [" +
      pageTitle +
      "](" +
      pageUrl +
      ") and prepare to answer questions about it?"
    );
  }

  var chatgptLogo =
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="currentColor">' +
    '<path d="M22.282 9.821a5.985 5.985 0 0 0-.516-4.91 6.046 6.046 0 0 0-6.51-2.9A6.065 6.065 0 0 0 4.981 4.18a5.985 5.985 0 0 0-3.998 2.9 6.046 6.046 0 0 0 .743 7.097 5.98 5.98 0 0 0 .51 4.911 6.051 6.051 0 0 0 6.515 2.9A5.985 5.985 0 0 0 13.26 24a6.056 6.056 0 0 0 5.772-4.206 5.99 5.99 0 0 0 3.997-2.9 6.056 6.056 0 0 0-.747-7.073zM13.26 22.43a4.476 4.476 0 0 1-2.876-1.04l.141-.081 4.779-2.758a.795.795 0 0 0 .392-.681v-6.737l2.02 1.168a.071.071 0 0 1 .038.052v5.583a4.504 4.504 0 0 1-4.494 4.494zM3.6 18.304a4.47 4.47 0 0 1-.535-3.014l.142.085 4.783 2.759a.771.771 0 0 0 .78 0l5.843-3.369v2.332a.08.08 0 0 1-.033.062L9.74 19.95a4.5 4.5 0 0 1-6.14-1.646zM2.34 7.896a4.485 4.485 0 0 1 2.366-1.973V11.6a.766.766 0 0 0 .388.676l5.815 3.355-2.02 1.168a.076.076 0 0 1-.071 0l-4.83-2.786A4.504 4.504 0 0 1 2.34 7.872zm16.597 3.855l-5.833-3.387L15.119 7.2a.076.076 0 0 1 .071 0l4.83 2.791a4.494 4.494 0 0 1-.676 8.105v-5.678a.79.79 0 0 0-.407-.667zm2.01-3.023l-.141-.085-4.774-2.782a.776.776 0 0 0-.785 0L9.409 9.23V6.897a.066.066 0 0 1 .028-.061l4.83-2.787a4.5 4.5 0 0 1 6.68 4.66zm-12.64 4.135l-2.02-1.164a.08.08 0 0 1-.038-.057V6.075a4.5 4.5 0 0 1 7.375-3.453l-.142.08L8.704 5.46a.795.795 0 0 0-.393.681zm1.097-2.365l2.602-1.5 2.607 1.5v2.999l-2.597 1.5-2.607-1.5z"/>' +
    "</svg>";

  var claudeLogo =
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="currentColor">' +
    '<path d="M17.3041 3.541h-3.6718l6.696 16.918H24z"/>' +
    '<path d="M6.6959 3.541L0 20.459h3.7442l1.3693-3.5527h7.0052l1.3693 3.5528h3.7442L10.5363 3.5409zm-.3712 10.2232l2.2914-5.9456 2.2914 5.9456z"/>' +
    "</svg>";

  var options = [
    {
      name: "ChatGPT",
      icon: chatgptLogo,
      url: function () {
        return (
          "https://chatgpt.com/?prompt=" +
          encodeURIComponent(buildPrompt("chatgpt"))
        );
      },
    },
    {
      name: "Claude",
      icon: claudeLogo,
      url: function () {
        return (
          "https://claude.ai/new?q=" +
          encodeURIComponent(buildPrompt("claude"))
        );
      },
    },
  ];

  function injectButton() {
    // Remove any existing button (from previous navigation)
    var existing = document.querySelector(".ask-ai");
    if (existing) existing.remove();

    var content = document.querySelector(".md-content");
    if (!content) return;

    content.style.position = "relative";

    var container = document.createElement("div");
    container.className = "ask-ai";

    var button = document.createElement("button");
    button.className = "ask-ai__button";
    button.setAttribute("aria-label", "Ask AI about this page");
    button.innerHTML =
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09z"/>' +
      '<path d="M18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456z"/>' +
      '<path d="M16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423z"/>' +
      "</svg>" +
      "<span>Ask AI</span>";

    var dropdown = document.createElement("div");
    dropdown.className = "ask-ai__dropdown";

    options.forEach(function (opt) {
      var link = document.createElement("a");
      link.className = "ask-ai__option";
      link.href = "#";
      link.target = "_blank";
      link.rel = "noopener";
      link.innerHTML =
        '<span class="ask-ai__option-icon">' +
        opt.icon +
        "</span>" +
        '<span class="ask-ai__option-name">' +
        opt.name +
        "</span>" +
        '<svg class="ask-ai__external" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>';
      link.addEventListener("click", function (e) {
        e.preventDefault();
        window.open(opt.url(), "_blank", "noopener");
        dropdown.classList.remove("ask-ai__dropdown--open");
      });
      dropdown.appendChild(link);
    });

    container.appendChild(button);
    container.appendChild(dropdown);

    button.addEventListener("click", function (e) {
      e.stopPropagation();
      dropdown.classList.toggle("ask-ai__dropdown--open");
    });

    container.addEventListener("click", function (e) {
      e.stopPropagation();
    });

    content.appendChild(container);
  }

  // Close dropdown on any outside click
  document.addEventListener("click", function () {
    var dropdown = document.querySelector(".ask-ai__dropdown--open");
    if (dropdown) dropdown.classList.remove("ask-ai__dropdown--open");
  });

  // Initial load
  injectButton();

  // Re-inject on instant navigation (MkDocs Material SPA)
  if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
      injectButton();
    });
  } else {
    // Fallback: listen for location changes via MutationObserver on title
    var lastUrl = location.href;
    new MutationObserver(function () {
      if (location.href !== lastUrl) {
        lastUrl = location.href;
        injectButton();
      }
    }).observe(document.querySelector("title"), { childList: true });
  }
})();
