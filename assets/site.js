(() => {
  const params = new URLSearchParams(window.location.search);
  const review = params.get('preview') === 'offer';

  if (review) {
    document.documentElement.classList.add('preview-offer');
    const notice = document.createElement('aside');
    notice.className = 'review-banner';
    notice.setAttribute('role', 'status');
    notice.textContent = document.documentElement.lang === 'fr'
      ? 'MODE RÉVISION — le contenu post-pitch est visible uniquement pour validation.'
      : 'REVIEW MODE — post-pitch content is visible only for content approval.';
    document.body.prepend(notice);
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
