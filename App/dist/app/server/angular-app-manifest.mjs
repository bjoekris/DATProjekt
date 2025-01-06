
export default {
  bootstrap: () => import('./main.server.mjs').then(m => m.default),
  inlineCriticalCss: true,
  baseHref: '/',
  locale: undefined,
  routes: [
  {
    "renderMode": 2,
    "redirectTo": "/login",
    "route": "/"
  },
  {
    "renderMode": 2,
    "route": "/login"
  },
  {
    "renderMode": 2,
    "route": "/register"
  },
  {
    "renderMode": 2,
    "route": "/invoice"
  }
],
  assets: {
    'index.csr.html': {size: 602, hash: '727a07eb986dbb2a1d8fa61e8c9eca14d226a2fedb9c18f8f2570e093fd6974b', text: () => import('./assets-chunks/index_csr_html.mjs').then(m => m.default)},
    'index.server.html': {size: 1115, hash: '35a1b9fe33cc9d27fc2c6d9d6c0b73e62a298c53cf74cb659df84d65747654dc', text: () => import('./assets-chunks/index_server_html.mjs').then(m => m.default)},
    'register/index.html': {size: 1830, hash: '22c4fc350af9eb699b77cde9cdb3c06f1f7a8e502c5a2cd8753a228f479a5346', text: () => import('./assets-chunks/register_index_html.mjs').then(m => m.default)},
    'login/index.html': {size: 1830, hash: '22c4fc350af9eb699b77cde9cdb3c06f1f7a8e502c5a2cd8753a228f479a5346', text: () => import('./assets-chunks/login_index_html.mjs').then(m => m.default)},
    'invoice/index.html': {size: 1830, hash: '22c4fc350af9eb699b77cde9cdb3c06f1f7a8e502c5a2cd8753a228f479a5346', text: () => import('./assets-chunks/invoice_index_html.mjs').then(m => m.default)},
    'styles-5INURTSO.css': {size: 0, hash: 'menYUTfbRu8', text: () => import('./assets-chunks/styles-5INURTSO_css.mjs').then(m => m.default)}
  },
};
