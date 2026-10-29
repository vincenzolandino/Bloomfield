(() => {
  'use strict';
  // Essential content and navigation work without JavaScript.
  // Focus the destination after a skip-link activation.
  const skip = document.querySelector('.skip-link');
  const main = document.getElementById('main');
  if (!skip || !main) return;
  skip.addEventListener('click', () => {
    main.tabIndex = -1;
    main.focus({ preventScroll: true });
  });
})();
