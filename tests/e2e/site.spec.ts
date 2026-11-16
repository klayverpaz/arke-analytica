import { test, expect } from '@playwright/test';

// pt/ e en/ são as páginas novas feitas à mão (15/11/2026); o build.py não as regenera.
const langs = [
  {
    code: 'pt', h1: 'Seu negócio é único. Seu software também deveria ser.', badge: null, privacy: 'privacidade',
    sections: ['autoridade', 'solucoes', 'projetos', 'desafios', 'diagnostico', 'metodologia', 'contratacao', 'perguntas', 'contato'],
    solutions: 3, cases: 5, steps: '.tl > li',
  },
  {
    code: 'en', h1: 'Your business is unique. Your software should be, too.', badge: null, privacy: 'privacy',
    sections: ['autoridade', 'solucoes', 'projetos', 'desafios', 'diagnostico', 'metodologia', 'contratacao', 'perguntas', 'contato'],
    solutions: 3, cases: 5, steps: '.tl > li',
  },
];

for (const l of langs) {
  test.describe(`home ${l.code}`, () => {
    test('renders every section and hides unproven blocks', async ({ page }) => {
      const errors: string[] = [];
      page.on('pageerror', (e) => errors.push(e.message));
      await page.goto(`/${l.code}/`);
      await expect(page.locator('h1')).toHaveText(l.h1);
      if (l.badge) await expect(page.locator('.badge')).toContainText(l.badge);
      for (const id of l.sections) {
        await expect(page.locator(`#${id}`)).toBeVisible();
      }
      await expect(page.locator('.stat')).toHaveCount(4);
      await expect(page.locator('#solucoes .card')).toHaveCount(l.solutions);
      await expect(page.locator('#projetos .case')).toHaveCount(l.cases);
      await expect(page.locator(l.steps)).toHaveCount(4);
      // sem depoimentos, fundadores, logos ou placeholders
      const text = await page.locator('body').innerText();
      expect(text).not.toMatch(/\[(MARCA|PROJETO|FUNDADOR|Nome)/);
      expect(text).not.toMatch(/NYU|VIDA Center/);
      expect(errors).toEqual([]);
    });

    test('images load and nothing overflows horizontally', async ({ page }) => {
      await page.goto(`/${l.code}/`);
      await page.evaluate(async () => {
        document.querySelectorAll('img').forEach((i) => i.setAttribute('loading', 'eager'));
        await Promise.all(Array.from(document.images).map((i) => i.decode().catch(() => null)));
      });
      const broken = await page.evaluate(() => Array.from(document.images).filter((i) => !i.naturalWidth).map((i) => i.src));
      expect(broken).toEqual([]);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      expect(overflow).toBeLessThanOrEqual(0);
    });

    test('language switch and privacy page', async ({ page }) => {
      await page.goto(`/${l.code}/`);
      const other = l.code === 'pt' ? 'en' : 'pt';
      const toggle = page.locator('.menu-toggle');
      if (await toggle.isVisible()) await toggle.click();
      await page.locator(`.lang a[data-lang="${other}"]`).click();
      await expect(page).toHaveURL(new RegExp(`/${other}/$`));
      await expect(page.locator('html')).toHaveAttribute('lang', other === 'pt' ? 'pt-BR' : 'en');
      await page.goto(`/${l.code}/${l.privacy}/`);
      await expect(page.locator('h1')).toBeVisible();
    });

    test('form validates, then opens WhatsApp with the message', async ({ page, context }) => {
      await context.route('https://wa.me/**', (r) => r.fulfill({ status: 200, body: 'ok' }));
      await context.route('https://api.whatsapp.com/**', (r) => r.fulfill({ status: 200, body: 'ok' }));
      await page.goto(`/${l.code}/`);
      await page.locator('#contact-form button[type=submit]').click();
      await expect(page.locator('.form-status')).toHaveClass(/is-error/);
      await page.fill('#f-name', 'Maria Teste');
      await page.fill('#f-email', 'maria@example.com');
      await page.fill('#f-challenge', 'Planilhas demais');
      await page.check('input[name=consent]');
      const [popup] = await Promise.all([
        context.waitForEvent('page'),
        page.locator('#contact-form button[type=submit]').click(),
      ]);
      const url = decodeURIComponent(popup.url());
      expect(url).toContain('wa.me/5511978119471');
      expect(url).toContain('Maria Teste');
      expect(url).toContain('Planilhas demais');
      await expect(page.locator('.form-status')).toHaveClass(/is-ok/);
    });
  });
}

const roadTitle: Record<string, string> = { pt: 'Inspeção de rodovias por vídeo', en: 'Road inspection from video' };
for (const code of ['pt', 'en']) test.describe(`home ${code}: página nova`, () => {
  test('vitrine do topo troca de projeto pelas barrinhas e leva ao carrossel', async ({ page }) => {
    await page.goto(`/${code}/`);
    await expect(page.locator('#sh-stage .scene')).toHaveCount(5);
    await page.locator('.sh-bars button').nth(4).click();
    await expect(page.locator('[data-sh-n]')).toHaveText('05');
    await expect(page.locator('[data-sh-title]')).toHaveText(roadTitle[code]);
    await page.locator('[data-sh-go]').click();
    await expect(page.locator('#projetos [data-current]')).toHaveText('05');
  });

  test('carrossel, perguntas e menu', async ({ page }) => {
    await page.goto(`/${code}/`);
    await page.locator('#projetos [data-next]').click();
    await expect(page.locator('#projetos [data-current]')).toHaveText('02');
    const faq = page.locator('.faq details');
    await faq.nth(1).locator('summary').click();
    await faq.nth(2).locator('summary').click();
    await expect(faq.nth(1)).not.toHaveAttribute('open', '');
    await expect(faq.nth(2)).toHaveAttribute('open', '');
    const toggle = page.locator('.menu-toggle');
    if (await toggle.isVisible()) {
      await toggle.click();
      await expect(page.locator('#menu-panel')).toBeVisible();
      await page.locator('#menu-panel a[href="#diagnostico"]').click();
      await expect(page.locator('#menu-panel')).toBeHidden();
    }
  });

  test('sem animação, tudo aparece no estado final', async ({ browser }) => {
    const ctx = await browser.newContext({ reducedMotion: 'reduce' });
    const page = await ctx.newPage();
    await page.goto(`/${code}/`);
    await expect(page.locator('.stats [data-to="30"]')).toHaveText('30');
    await expect(page.locator('#projetos .mo-road [data-set="3:1,5:2"]')).toHaveText('2');
    // Kanban do funil: o negócio em negociação foi fechado e a nova oportunidade entrou
    const kb = page.locator('.sc-kanban');
    await expect(kb.locator('[data-set="2:1,4:2"]')).toHaveText('2');
    await expect(kb.locator('[data-set="2:31,4:79"]')).toHaveText('79');
    const x = async (sel: string) => (await kb.locator(sel).boundingBox())!.x;
    expect(Math.abs((await x('.kF')) - (await x('.kG')))).toBeLessThan(1);
    expect(Math.abs((await x('.kD')) - (await x('.kb-col:nth-child(3)')))).toBeLessThan(8);
    await expect(kb.locator('.kH')).toHaveCSS('opacity', '1');
    await ctx.close();
  });
});

test('root redirects by saved language', async ({ page }) => {
  await page.goto('/en/');
  await page.goto('/');
  await expect(page).toHaveURL(/\/en\/$/);
});

test('screenshots', async ({ page }, info) => {
  for (const l of langs) {
    await page.goto(`/${l.code}/`);
    await page.addStyleTag({ content: '[data-reveal]{opacity:1!important;transform:none!important}' });
    await page.evaluate(async () => {
      document.querySelectorAll('img').forEach((i) => i.setAttribute('loading', 'eager'));
      await document.fonts.ready;
      await Promise.all(Array.from(document.images).map((i) => i.decode().catch(() => null)));
    });
    await page.waitForTimeout(500);
    await page.screenshot({ path: `test-results/shots/${info.project.name}-${l.code}.png`, fullPage: true });
  }
});
