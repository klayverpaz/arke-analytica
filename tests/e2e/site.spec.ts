import { test, expect } from '@playwright/test';

const langs = [
  { code: 'pt', h1: 'Seu negócio é único. Seu software também deveria ser.', badge: 'até 1 semana', privacy: 'privacidade' },
  { code: 'en', h1: 'Your business is unique. Your software should be, too.', badge: '1 week', privacy: 'privacy' },
];

for (const l of langs) {
  test.describe(`home ${l.code}`, () => {
    test('renders every section and hides unproven blocks', async ({ page }) => {
      const errors: string[] = [];
      page.on('pageerror', (e) => errors.push(e.message));
      await page.goto(`/${l.code}/`);
      await expect(page.locator('h1')).toHaveText(l.h1);
      await expect(page.locator('.badge')).toContainText(l.badge);
      for (const id of ['autoridade', 'solucoes', 'projetos', 'segmentos', 'desafios', 'metodologia', 'contratacao', 'contato']) {
        await expect(page.locator(`#${id}`)).toBeVisible();
      }
      await expect(page.locator('.stat')).toHaveCount(4);
      await expect(page.locator('#solucoes .card')).toHaveCount(6);
      await expect(page.locator('.case')).toHaveCount(4);
      await expect(page.locator('.step')).toHaveCount(6);
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
      expect(url).toContain('wa.me/558599500076');
      expect(url).toContain('Maria Teste');
      expect(url).toContain('Planilhas demais');
      await expect(page.locator('.form-status')).toHaveClass(/is-ok/);
    });
  });
}

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
