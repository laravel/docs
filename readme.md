# Українська документація Laravel

Повний український переклад офіційної документації Laravel - **102 сторінки,
понад 92 000 рядків**, синхронізовані з оригіналом.

Читати онлайн: **[laravelukraine.com/docs](https://laravelukraine.com/docs)**

Оригінал: [laravel.com/docs](https://laravel.com/docs) · [laravel/docs](https://github.com/laravel/docs)

> **In English:** a complete Ukrainian translation of the official Laravel
> documentation, kept in sync with upstream. Every page records the upstream
> commit it was translated from, so drift is measurable rather than guessed at.
> Read it at [laravelukraine.com/docs](https://laravelukraine.com/docs);
> contributions are welcome - see [Як допомогти](#як-допомогти).

## Про переклад

Репозиторій є форком [laravel/docs](https://github.com/laravel/docs) з дзеркальними
іменами гілок: переклад для Laravel 13 живе в гілці `13.x`, як і в оригіналі. Імена
файлів і якорі заголовків збігаються з англійськими - завдяки цьому адреси сторінок
ідентичні оригінальним:

```
laravel.com/docs/13.x/installation
laravelukraine.com/docs/13.x/installation
```

Кожен перекладений файл починається з YAML-хедера, що фіксує коміт оригіналу, з якого
зроблено переклад:

```
---
git: 0d61029ee4473fc32ef843ea6051b2db54647a34
---
```

Це дозволяє бачити, які сторінки відстали від оригіналу:

```
diff <(git show upstream/13.x:strings.md) strings.md
```

## Синхронізація з оригіналом

Гілка `upstream-13.x` - дзеркало [laravel/docs](https://github.com/laravel/docs)
всередині цього репозиторію, потрібне для обчислення різниці, коли віддалений
`upstream` не налаштований. Щоб підтягнути зміни оригіналу, її оновлюють і
звіряють перекладені файли командою вище.

Щодня це робиться автоматично - [workflow](.github/workflows/sync-upstream.yml)
порівнює переклад з оригіналом і розводить зміни на два шляхи. Дрібні правки
перекладаються та йдуть у Pull Request на рев'ю; великі зміни й нові сторінки
потрапляють в issue, бо новий розділ потребує людини.

Скрипти під цим лежать у [`scripts/`](scripts) і працюють самостійно:

| Скрипт | Що робить |
| --- | --- |
| `upstream_status.py` | рахує відставання за `git:` хедерами сторінок |
| `translate_diff.py` | перекладає лише ті секції, яких торкнувся diff |
| `validate_translation.py` | звіряє структуру: рядки, якорі, блоки коду, терміни |

Валідатор запускається до запису файлу. Викинутий якір ламає бічну панель і всі
глибокі посилання на сторінку, а в diff виглядає як звичайна зміна формулювання -
тому це перевіряється машинно, а не оком.

## Як допомогти

Помітили помилку, неточність або незграбну фразу - відкривайте
[issue](https://github.com/laravelukraine/docs/issues) або Pull Request у гілку `13.x`.

Перед тим як перекладати, загляньте в [GLOSSARY.md](GLOSSARY.md) - там узгоджений
словник термінів і правила оформлення. Єдина термінологія важливіша за красу окремої
фрази: коли `middleware` в одному розділі «проміжне ПЗ», а в іншому «посередник»,
читати стає важче.

Коротко, що **не** перекладається: вміст блоків коду, якорі `<a name="...">`, адреси
посилань, плейсхолдер `{{version}}`, імена класів, методів і команд.

## Ліцензія

Оригінальна документація Laravel поширюється за ліцензією MIT,
Copyright (c) Taylor Otwell - див. [license.md](license.md).

Переклад є похідною роботою і поширюється за тією ж ліцензією.

Laravel є торговельною маркою Laravel Holdings Inc. Цей переклад - незалежна
ініціатива спільноти, не пов'язана з Laravel Holdings Inc.
