# Site da Arke Analytica

Site estático publicado no GitHub Pages: https://klayverpaz.github.io/arke-analytica/

- Textos, números e projetos ficam em `content/pt.json` e `content/en.json`.
- `python3 build.py` gera `index.html`, `pt/`, `en/`, `sitemap.xml` e `robots.txt`. Não edite esses arquivos à mão.
- Estilos em `assets/css/site.css` (tokens do design system no topo) e comportamento em `assets/js/site.js`.
- Números de WhatsApp e e-mail ficam no topo de `build.py`.
- Testes: `npm install`, `npx playwright install chromium` e `npm test` (desktop e mobile, PT e EN).

O formulário não tem backend: o envio abre o WhatsApp com a mensagem preenchida.
