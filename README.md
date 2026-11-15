# Site da Arke Analytica

Site estático publicado no GitHub Pages: https://klayverpaz.github.io/arke-analytica/

- **`pt/index.html` e `en/index.html` são feitas à mão** (página nova de 15/11/2026, com cenas
  animadas em HTML e estilos e scripts no próprio arquivo). O `build.py` não sobrescreve páginas
  com o marcador `arke: pagina-feita-a-mao`; ele ainda gera a raiz, as páginas de privacidade, o
  sitemap e o robots. O protótipo e as decisões estão no vault, em
  `20-ventures/23-arke-analytica/site-novo/` (LEIAME.md). Mudou texto em PT? Mude também no EN.
- `content/pt.json` e `content/en.json` não alimentam mais as páginas iniciais.
- `python3 build.py` gera `index.html` (raiz), as páginas de privacidade, `sitemap.xml` e `robots.txt`. Não edite esses arquivos à mão.
- As páginas iniciais trazem os próprios estilos e scripts. `assets/css/site.css` e `assets/js/site.js` servem às páginas de privacidade.
- Números de WhatsApp e e-mail ficam no topo de `build.py`.
- Testes: `npm install`, `npx playwright install chromium` e `npm test` (desktop e mobile, PT e EN).

O formulário não tem backend: o envio abre o WhatsApp com a mensagem preenchida.
