# Maple Lingua

Школа французского и английского для переезда в Канаду: обучение с нуля и подготовка к TEF Canada, TCF Canada, IELTS General и CELPIP. Онлайн и очно в Торонто.

> Название «Maple Lingua» может поменяться: домен maplelingua.com уже занят. Логотип держится на двухцветном кленовом листе, поэтому при смене названия меняется только надпись.

## Что где лежит

| Папка | Что внутри |
|---|---|
| `site/` | Лендинг. `index.html` — готовая страница для хостинга, `landing.html` — исходник для превью в Claude |
| `brand/` | Брендбук (`brandbook.html`), его картинки в `assets/`, шаблоны поста, сторис и сертификата в `templates/` (исходники в `templates/source/`) |
| `logos/` | Логотипы в SVG (текст переведён в кривые) и PNG 2000 px с прозрачным фоном. В `avatar/` — аватарки для Telegram 1024×1024 |
| `design-canvas/` | Исходные варианты логотипа с холста (6 концептов) |
| `tools/` | Скрипты, которыми собраны логотипы, аватарки и шаблоны |

### Логотипы

| Файл | Вариант |
|---|---|
| `maple-lingua-2-dvuyazychnyj-list` | **Основной.** Сине-красный лист и надпись MAPLE LINGUA |
| `maple-lingua-3-list-nad-i` | Надпись с листом над «i», с подписью и без |
| `maple-lingua-4-pechat` | Печать для сертификатов и мерча |
| `maple-lingua-5-fr-en` | Облачка Fr и En |

## Бренд коротко

- **Синий `#1F4E9C` — французский, красный `#C8332B` — английский.** Текст и тёмный фон — `#1B2A41`.
- **Шрифт** — Manrope (Google Fonts, бесплатный, есть кириллица).
- **Голос** — «проводник»: конкретно, спокойно, честно, на «вы». Подробности в брендбуке.

## Перед запуском сайта

1. **Форма заявки.** Создайте форму на [formspree.io](https://formspree.io) и вставьте её адрес в `site/index.html` в строку `const FORM_ENDPOINT = "";`. Пока строка пустая, заявки не отправляются, и форма предлагает написать в Telegram.
2. **Фото преподавателя.** Замените заглушку «Здесь будет фото Эльвиры».
3. **Аналитика.** Подключите Google Tag Manager / GA4 или Яндекс Метрику. Сайт уже отправляет события: клики по кнопкам (`cta_*`), `form_start`, `form_error`, `lead_submit`. Для Метрики задайте `window.YM_ID`.
4. **Превью ссылки.** Раскомментируйте `og:image` в `<head>` и укажите полный адрес картинки.
5. **Хостинг.** `site/index.html` — один самодостаточный файл: подойдут GitHub Pages, Netlify, Cloudflare Pages.

## Пересборка логотипов и шаблонов

Скрипты в `tools/` написаны на Python (`fonttools`, `uharfbuzz`) и Node (`playwright`). Им нужны файлы шрифта Manrope (`m500.ttf`, `m700.ttf`, `m800.ttf`) из Google Fonts в отдельной папке:

```bash
pip install fonttools uharfbuzz
python3 tools/build_logos.py путь/к/шрифтам logos          # SVG логотипов
node tools/render.js logos путь/для/превью                  # PNG 2000 px
python3 tools/build_templates.py logos путь/для/html        # HTML шаблонов
node tools/render_tpl.js путь/для/html brand/templates      # PNG и PDF шаблонов
```
