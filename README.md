# Site da Arke Analytica

Site estático publicado no GitHub Pages: https://klayverpaz.github.io/arke-analytica/

- **`pt/index.html` é feita à mão** (página nova de 15/11/2026, com cenas animadas em HTML e
  estilos e scripts no próprio arquivo). O `build.py` não sobrescreve páginas com o marcador
  `arke: pagina-feita-a-mao`. O protótipo e as decisões estão no vault, em
  `20-ventures/23-arke-analytica/site-novo/` (LEIAME.md).
- Textos, números e projetos da versão em inglês ficam em `content/en.json` (e `content/pt.json`,
  que não alimenta mais a página em português).
- `python3 build.py` gera `index.html`, `pt/`, `en/`, `sitemap.xml` e `robots.txt`. Não edite esses arquivos à mão.
- Estilos em `assets/css/site.css` (tokens do design system no topo) e comportamento em `assets/js/site.js`.
- Números de WhatsApp e e-mail ficam no topo de `build.py`.
- Testes: `npm install`, `npx playwright install chromium` e `npm test` (desktop e mobile, PT e EN).

O formulário não tem backend: o envio abre o WhatsApp com a mensagem preenchida.
