/* The displayed formulas are exported from canonical LaTeX, not retyped.
 * These are the portable rendering equivalents of the parent manuscript macros.
 * phasedot keeps the parent's heavy bullet; CSS/TeX scaling is presentation only. */
window.MathJax = {
  loader: {load: []},
  tex: {
    tags: 'none',
    macros: {
      mc: ['\\mathcal{#1}', 1], mbf: ['\\mathbf{#1}', 1],
      bs: ['\\boldsymbol{#1}', 1], p: ['\\frac{\\partial #1}{\\partial #2}', 2],
      phasedot: ['\\overset{\\scriptscriptstyle\\bullet}{#1}', 1],
      dev: '\\operatorname{dev}', dv: '\\,{\\rm d}v',
      dVblank: '\\,{\\rm d}V', dVxi: '\\,{\\rm d}V_\\xi', dt: '\\,{\\rm d}t',
      matD: ['\\frac{{\\rm D}#1}{{\\rm D}#2}', 2]
    }
  },
  svg: {fontCache: 'local'},
  options: {enableMenu: false, ignoreHtmlClass: 'code|latex|commands', processHtmlClass: 'math'},
  startup: {ready: function () {
    MathJax.startup.defaultReady();
    MathJax.startup.promise.then(function () {
      document.documentElement.dataset.mathReady = 'true';
      document.querySelectorAll('.math').forEach(function (element) {
        if (element.scrollWidth > element.clientWidth + 1) {
          element.tabIndex = 0;
          element.setAttribute('aria-label', 'Equation; scroll horizontally to read the full display');
          const hint = document.createElement('p');
          hint.className = 'math-hint';
          hint.textContent = 'Scroll horizontally to read the full equation →';
          element.after(hint);
        }
      });
    });
  }}
};
