(() => {
  'use strict';
  document.querySelectorAll('[data-product-3d]').forEach((root) => {
    const launch = root.querySelector('[data-product-3d-launch]');
    const stage = root.querySelector('[data-product-3d-stage]');
    const status = root.querySelector('[data-product-3d-status]');
    let started = false;
    const emit = (name, detail = {}) => document.dispatchEvent(new CustomEvent(`yuchen:${name}`, {
      detail: { ctaLocation: 'product_3d', modelId: root.dataset.modelId || '', ...detail }
    }));
    launch?.addEventListener('click', async () => {
      if (started) return;
      started = true;
      launch.disabled = true;
      launch.textContent = 'Loading 3D…';
      stage.hidden = false;
      emit('3d-open');
      try {
        const viewer = await import('./product-3d-viewer.js');
        await viewer.mountProduct3D(root, emit);
        launch.remove();
        emit('3d-ready');
      } catch (error) {
        stage.hidden = true;
        launch.disabled = false;
        launch.textContent = 'Try 3D view again';
        const fallback = root.querySelector('[data-product-3d-fallback]');
        if (fallback) fallback.hidden = false;
        if (status) status.textContent = 'The interactive view could not load. The product photos and component notes remain available.';
        emit('3d-error', { errorBucket: error?.name || 'load_error' });
      }
    });
  });
})();
