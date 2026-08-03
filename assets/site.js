(() => {
  const params = new URLSearchParams(window.location.search);
  const review = params.get('preview') === 'offer';

  if (review) {
    document.documentElement.classList.add('preview-offer');
  }

  const utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  document.querySelectorAll('[data-checkout]').forEach((link) => {
    const destination = new URL(link.href);
    utmKeys.forEach((key) => {
      if (params.has(key)) destination.searchParams.set(key, params.get(key));
    });
    link.href = destination.toString();
  });
})();
