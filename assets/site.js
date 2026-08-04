(() => {
  const params = new URLSearchParams(window.location.search);
  const review = params.get('preview') === 'offer';

  if (review) {
    document.documentElement.classList.add('preview-offer');
  }

  const targetPlayerId = 'vid-6a70aeed9fc79f7cf8cb1795';
  let revealScheduled = false;

  const schedulePostPitchReveal = (candidate) => {
    const player = candidate || document.querySelector(`#${targetPlayerId}`);
    const configId = (player && player.config && player.config.id) || (player && player.id);
    const normalizedId = typeof configId === 'string'
      ? `vid-${configId.replace(/^vid-/, '')}`
      : '';

    if (normalizedId !== targetPlayerId || revealScheduled || typeof player.displayHiddenElements !== 'function') return false;

    revealScheduled = true;
    player.displayHiddenElements(1254, ['.esconder'], { persist: true });
    return true;
  };

  document.addEventListener('player:ready', (event) => {
    const detail = event.detail || {};
    schedulePostPitchReveal(detail.player);
  });

  // The VTurb embed is asynchronous and can become ready before this final script runs.
  // Retry briefly so the reveal is always registered, including on cached/fast loads.
  const revealRetry = window.setInterval(() => {
    if (schedulePostPitchReveal()) window.clearInterval(revealRetry);
  }, 100);
  window.setTimeout(() => window.clearInterval(revealRetry), 15000);

  const utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  document.querySelectorAll('[data-checkout]').forEach((link) => {
    const destination = new URL(link.href);
    utmKeys.forEach((key) => {
      if (params.has(key)) destination.searchParams.set(key, params.get(key));
    });
    link.href = destination.toString();
  });
})();
