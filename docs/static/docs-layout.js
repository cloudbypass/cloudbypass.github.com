(function () {
  'use strict';
  var legacy = {"zh-cn": ["关于穿云api版本", "穿云v1", "穿云v2", "穿云v2s", "如何区分常见验证？", "突破-js质询，穿云v2自动挑战", "突破-turnstile-部件", "突破-datadome-挑战", "获取帮助", "突破-js质询穿云v2自动挑战"], "us-en": ["about-scrapingbypass-api-versions", "scrapingbypass-v1", "scrapingbypass-v2", "scrapingbypass-v2s", "how-to-distinguish-common-verifications", "bypass-js-challenge-scrapingbypass-v2-auto-challenge", "bypass-turnstile-component", "bypass-datadome-challenge", "get-help"]};
  var pages = ["README", "_coverpage", "_navbar", "_sidebar", "challenges", "collector", "compatibility", "credit_balance", "credit_consume", "fp_browser", "golang_sdk", "nginx_proxy", "nodejs_sdk", "proxy_tools", "python_sdk", "quickstart", "request_parameters", "response_data", "trial", "vibe_coding", "websocks"];
  function redirectLegacy() {
    var match = location.hash.match(/^#\/(zh-cn|us-en)\/quickstart\?id=([^&]+)/);
    if (!match) return;
    var id;
    try { id = decodeURIComponent(match[2]); } catch (e) { return; }
    if (legacy[match[1]].indexOf(id) === -1) return;
    var first = legacy[match[1]][0];
    if (id === '突破-js质询穿云v2自动挑战') id = '突破-js质询，穿云v2自动挑战';
    location.replace('#/' + match[1] + '/challenges' + (id === first ? '' : '?id=' + encodeURIComponent(id)));
  }
  document.addEventListener('click', function (event) {
    var link = event.target.closest('[data-language-switch]');
    if (!link) return;
    var match = location.hash.match(/^#\/(zh-cn|us-en)\/([^?]*)/);
    if (!match) return;
    var page = match[2].replace(/\.md$/, '');
    if (pages.indexOf(page) === -1) page = '';
    link.href = '#/' + (match[1] === 'zh-cn' ? 'us-en' : 'zh-cn') + '/' + page;
  }, true);
  function updatePageLayout() {
    var path = location.hash.split('?')[0];
    document.body.classList.toggle('language-selection', !path || path === '#' || path === '#/');
  }
  updatePageLayout();
  window.addEventListener('hashchange', updatePageLayout);
  redirectLegacy();
  window.addEventListener('hashchange', redirectLegacy);
  window.$docsify.plugins = (window.$docsify.plugins || []).concat(function (hook, vm) {
    hook.doneEach(function () {
      var cn = vm.route.path.indexOf('/zh-cn') === 0;
      document.documentElement.lang = cn ? 'zh-CN' : 'en';
      var other = cn ? 'us-en' : 'zh-cn';
      var page = vm.route.path.split('/')[2] || '';
      page = page.replace(/\.md$/, '');
      if (pages.indexOf(page) === -1) page = '';
      document.querySelectorAll('[data-language-switch]').forEach(function (link) {
        link.href = '#/' + other + '/' + page;
      });
      var old = document.querySelector('.page-toc');
      if (old) old.remove();
      var headings = document.querySelectorAll('.markdown-section h2 a.anchor');
      if (headings.length < 2) return;
      var nav = document.createElement('nav');
      nav.className = 'page-toc';
      nav.setAttribute('aria-label', cn ? '本页目录' : 'On this page');
      var label = document.createElement('strong');
      label.textContent = cn ? '本页目录' : 'On this page';
      nav.appendChild(label);
      headings.forEach(function (heading) {
        var link = document.createElement('a');
        link.href = heading.href;
        link.textContent = heading.textContent;
        nav.appendChild(link);
      });
      document.body.appendChild(nav);
    });
  });
})();
