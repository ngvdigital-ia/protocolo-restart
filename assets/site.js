(() => {
  const params = new URLSearchParams(window.location.search);
  const review = params.get('preview') === 'offer';

  if (review) {
    document.documentElement.classList.add('preview-offer');
  }

  const targetPlayerId = 'vid-6a70aeed9fc79f7cf8cb1795';
  let revealScheduled = false;

  document.addEventListener('player:ready', (event) => {
    const player = event.detail;
    const configId = player && player.config && player.config.id;
    const normalizedId = typeof configId === 'string'
      ? `vid-${configId.replace(/^vid-/, '')}`
      : '';

    if (normalizedId !== targetPlayerId || revealScheduled || typeof player.displayHiddenElements !== 'function') return;

    revealScheduled = true;
    player.displayHiddenElements(1254, ['.esconder'], { persist: true });
  });

  const utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  document.querySelectorAll('[data-checkout]').forEach((link) => {
    const destination = new URL(link.href);
    utmKeys.forEach((key) => {
      if (params.has(key)) destination.searchParams.set(key, params.get(key));
    });
    link.href = destination.toString();
  });
})();
