---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---

# Рядки

- [Вступ](#introduction)
- [Доступні методи](#available-methods)

<a name="introduction"></a>
## Вступ

Laravel має цілу низку функцій для роботи з рядковими значеннями. Багато з них використовує сам фреймворк, але ви вільні застосовувати їх і у власних застосунках, якщо вважаєте зручними.

<a name="available-methods"></a>
## Доступні методи

<a name="strings-method-list"></a>
### Рядки

<div class="collection-method-list" markdown="1">

[\__](#method-__)
[class_basename](#method-class-basename)
[e](#method-e)
[preg_replace_array](#method-preg-replace-array)
[Str::after](#method-str-after)
[Str::afterLast](#method-str-after-last)
[Str::apa](#method-str-apa)
[Str::ascii](#method-str-ascii)
[Str::before](#method-str-before)
[Str::beforeLast](#method-str-before-last)
[Str::between](#method-str-between)
[Str::betweenFirst](#method-str-between-first)
[Str::camel](#method-camel-case)
[Str::charAt](#method-char-at)
[Str::chopStart](#method-str-chop-start)
[Str::chopEnd](#method-str-chop-end)
[Str::contains](#method-str-contains)
[Str::containsAll](#method-str-contains-all)
[Str::counted](#method-str-counted)
[Str::doesntContain](#method-str-doesnt-contain)
[Str::doesntEndWith](#method-str-doesnt-end-with)
[Str::doesntStartWith](#method-str-doesnt-start-with)
[Str::deduplicate](#method-deduplicate)
[Str::endsWith](#method-ends-with)
[Str::excerpt](#method-excerpt)
[Str::finish](#method-str-finish)
[Str::fromBase64](#method-str-from-base64)
[Str::headline](#method-str-headline)
[Str::initials](#method-str-initials)
[Str::inlineMarkdown](#method-str-inline-markdown)
[Str::is](#method-str-is)
[Str::isAscii](#method-str-is-ascii)
[Str::isJson](#method-str-is-json)
[Str::isUlid](#method-str-is-ulid)
[Str::isUrl](#method-str-is-url)
[Str::isUuid](#method-str-is-uuid)
[Str::kebab](#method-kebab-case)
[Str::lcfirst](#method-str-lcfirst)
[Str::length](#method-str-length)
[Str::limit](#method-str-limit)
[Str::lower](#method-str-lower)
[Str::markdown](#method-str-markdown)
[Str::mask](#method-str-mask)
[Str::match](#method-str-match)
[Str::matchAll](#method-str-match-all)
[Str::isMatch](#method-str-is-match)
[Str::orderedUuid](#method-str-ordered-uuid)
[Str::padBoth](#method-str-padboth)
[Str::padLeft](#method-str-padleft)
[Str::padRight](#method-str-padright)
[Str::password](#method-str-password)
[Str::plural](#method-str-plural)
[Str::pluralStudly](#method-str-plural-studly)
[Str::position](#method-str-position)
[Str::random](#method-str-random)
[Str::remove](#method-str-remove)
[Str::repeat](#method-str-repeat)
[Str::replace](#method-str-replace)
[Str::replaceArray](#method-str-replace-array)
[Str::replaceFirst](#method-str-replace-first)
[Str::replaceLast](#method-str-replace-last)
[Str::replaceMatches](#method-str-replace-matches)
[Str::replaceStart](#method-str-replace-start)
[Str::replaceEnd](#method-str-replace-end)
[Str::reverse](#method-str-reverse)
[Str::singular](#method-str-singular)
[Str::slug](#method-str-slug)
[Str::snake](#method-snake-case)
[Str::squish](#method-str-squish)
[Str::start](#method-str-start)
[Str::startsWith](#method-starts-with)
[Str::studly](#method-studly-case)
[Str::substr](#method-str-substr)
[Str::substrCount](#method-str-substrcount)
[Str::substrReplace](#method-str-substrreplace)
[Str::swap](#method-str-swap)
[Str::take](#method-take)
[Str::title](#method-title-case)
[Str::toBase64](#method-str-to-base64)
[Str::transliterate](#method-str-transliterate)
[Str::trim](#method-str-trim)
[Str::ltrim](#method-str-ltrim)
[Str::rtrim](#method-str-rtrim)
[Str::ucfirst](#method-str-ucfirst)
[Str::ucsplit](#method-str-ucsplit)
[Str::ucwords](#method-str-ucwords)
[Str::upper](#method-str-upper)
[Str::ulid](#method-str-ulid)
[Str::unwrap](#method-str-unwrap)
[Str::uuid](#method-str-uuid)
[Str::uuid7](#method-str-uuid7)
[Str::wordCount](#method-str-word-count)
[Str::wordWrap](#method-str-word-wrap)
[Str::words](#method-str-words)
[Str::wrap](#method-str-wrap)
[str](#method-str)
[trans](#method-trans)
[trans_choice](#method-trans-choice)

</div>

<a name="fluent-strings-method-list"></a>
### Плавні рядки

<div class="collection-method-list" markdown="1">

[after](#method-fluent-str-after)
[afterLast](#method-fluent-str-after-last)
[apa](#method-fluent-str-apa)
[append](#method-fluent-str-append)
[ascii](#method-fluent-str-ascii)
[basename](#method-fluent-str-basename)
[before](#method-fluent-str-before)
[beforeLast](#method-fluent-str-before-last)
[between](#method-fluent-str-between)
[betweenFirst](#method-fluent-str-between-first)
[camel](#method-fluent-str-camel)
[charAt](#method-fluent-str-char-at)
[classBasename](#method-fluent-str-class-basename)
[chopStart](#method-fluent-str-chop-start)
[chopEnd](#method-fluent-str-chop-end)
[contains](#method-fluent-str-contains)
[containsAll](#method-fluent-str-contains-all)
[counted](#method-fluent-str-counted)
[decrypt](#method-fluent-str-decrypt)
[deduplicate](#method-fluent-str-deduplicate)
[dirname](#method-fluent-str-dirname)
[doesntContain](#method-fluent-str-doesnt-contain)
[doesntEndWith](#method-fluent-str-doesnt-end-with)
[doesntStartWith](#method-fluent-str-doesnt-start-with)
[encrypt](#method-fluent-str-encrypt)
[endsWith](#method-fluent-str-ends-with)
[exactly](#method-fluent-str-exactly)
[excerpt](#method-fluent-str-excerpt)
[explode](#method-fluent-str-explode)
[finish](#method-fluent-str-finish)
[fromBase64](#method-fluent-str-from-base64)
[hash](#method-fluent-str-hash)
[headline](#method-fluent-str-headline)
[initials](#method-fluent-str-initials)
[inlineMarkdown](#method-fluent-str-inline-markdown)
[is](#method-fluent-str-is)
[isAscii](#method-fluent-str-is-ascii)
[isEmpty](#method-fluent-str-is-empty)
[isNotEmpty](#method-fluent-str-is-not-empty)
[isJson](#method-fluent-str-is-json)
[isUlid](#method-fluent-str-is-ulid)
[isUrl](#method-fluent-str-is-url)
[isUuid](#method-fluent-str-is-uuid)
[kebab](#method-fluent-str-kebab)
[lcfirst](#method-fluent-str-lcfirst)
[length](#method-fluent-str-length)
[limit](#method-fluent-str-limit)
[lower](#method-fluent-str-lower)
[markdown](#method-fluent-str-markdown)
[mask](#method-fluent-str-mask)
[match](#method-fluent-str-match)
[matchAll](#method-fluent-str-match-all)
[isMatch](#method-fluent-str-is-match)
[newLine](#method-fluent-str-new-line)
[padBoth](#method-fluent-str-padboth)
[padLeft](#method-fluent-str-padleft)
[padRight](#method-fluent-str-padright)
[pipe](#method-fluent-str-pipe)
[plural](#method-fluent-str-plural)
[position](#method-fluent-str-position)
[prepend](#method-fluent-str-prepend)
[remove](#method-fluent-str-remove)
[repeat](#method-fluent-str-repeat)
[replace](#method-fluent-str-replace)
[replaceArray](#method-fluent-str-replace-array)
[replaceFirst](#method-fluent-str-replace-first)
[replaceLast](#method-fluent-str-replace-last)
[replaceMatches](#method-fluent-str-replace-matches)
[replaceStart](#method-fluent-str-replace-start)
[replaceEnd](#method-fluent-str-replace-end)
[scan](#method-fluent-str-scan)
[singular](#method-fluent-str-singular)
[slug](#method-fluent-str-slug)
[snake](#method-fluent-str-snake)
[split](#method-fluent-str-split)
[squish](#method-fluent-str-squish)
[start](#method-fluent-str-start)
[startsWith](#method-fluent-str-starts-with)
[stripTags](#method-fluent-str-strip-tags)
[studly](#method-fluent-str-studly)
[substr](#method-fluent-str-substr)
[substrReplace](#method-fluent-str-substrreplace)
[swap](#method-fluent-str-swap)
[take](#method-fluent-str-take)
[tap](#method-fluent-str-tap)
[test](#method-fluent-str-test)
[title](#method-fluent-str-title)
[toBase64](#method-fluent-str-to-base64)
[toHtmlString](#method-fluent-str-to-html-string)
[toUri](#method-fluent-str-to-uri)
[transliterate](#method-fluent-str-transliterate)
[trim](#method-fluent-str-trim)
[ltrim](#method-fluent-str-ltrim)
[rtrim](#method-fluent-str-rtrim)
[ucfirst](#method-fluent-str-ucfirst)
[ucsplit](#method-fluent-str-ucsplit)
[ucwords](#method-fluent-str-ucwords)
[unwrap](#method-fluent-str-unwrap)
[upper](#method-fluent-str-upper)
[when](#method-fluent-str-when)
[whenContains](#method-fluent-str-when-contains)
[whenContainsAll](#method-fluent-str-when-contains-all)
[whenDoesntEndWith](#method-fluent-str-when-doesnt-end-with)
[whenDoesntStartWith](#method-fluent-str-when-doesnt-start-with)
[whenEmpty](#method-fluent-str-when-empty)
[whenNotEmpty](#method-fluent-str-when-not-empty)
[whenStartsWith](#method-fluent-str-when-starts-with)
[whenEndsWith](#method-fluent-str-when-ends-with)
[whenExactly](#method-fluent-str-when-exactly)
[whenNotExactly](#method-fluent-str-when-not-exactly)
[whenIs](#method-fluent-str-when-is)
[whenIsAscii](#method-fluent-str-when-is-ascii)
[whenIsUlid](#method-fluent-str-when-is-ulid)
[whenIsUuid](#method-fluent-str-when-is-uuid)
[whenTest](#method-fluent-str-when-test)
[wordCount](#method-fluent-str-word-count)
[words](#method-fluent-str-words)
[wrap](#method-fluent-str-wrap)

</div>

<a name="strings"></a>
## Рядки

<a name="method-__"></a>
#### `__()` {.collection-method}

Функція `__` перекладає заданий рядок або ключ перекладу за допомогою ваших [мовних файлів](/docs/{{version}}/localization):

```php
echo __('Welcome to our application');

echo __('messages.welcome');
```

Якщо вказаного рядка чи ключа перекладу не існує, функція `__` повернає передане значення. Тож у прикладі вище функція `__` повернула б `messages.welcome`, якби такого ключа перекладу не було.

<a name="method-class-basename"></a>
#### `class_basename()` {.collection-method}

Функція `class_basename` повертає назву заданого класу без його простору імен:

```php
$class = class_basename('Foo\Bar\Baz');

// Baz
```

<a name="method-e"></a>
#### `e()` {.collection-method}

Функція `e` виконує PHP-функцію `htmlspecialchars`, у якій опція `double_encode` за замовчуванням дорівнює `true`:

```php
echo e('<html>foo</html>');

// &lt;html&gt;foo&lt;/html&gt;
```

<a name="method-preg-replace-array"></a>
#### `preg_replace_array()` {.collection-method}

Функція `preg_replace_array` послідовно замінює в рядку заданий шаблон значеннями з масиву:

```php
$string = 'The event will take place between :start and :end';

$replaced = preg_replace_array('/:[a-z_]+/', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-after"></a>
#### `Str::after()` {.collection-method}

Метод `Str::after` повертає все, що йде в рядку після заданого значення. Якщо значення в рядку немає, буде повернуто цілий рядок:

```php
use Illuminate\Support\Str;

$slice = Str::after('This is my name', 'This is');

// ' my name'
```

<a name="method-str-after-last"></a>
#### `Str::afterLast()` {.collection-method}

Метод `Str::afterLast` повертає все, що йде в рядку після останнього входження заданого значення. Якщо значення в рядку немає, буде повернуто цілий рядок:

```php
use Illuminate\Support\Str;

$slice = Str::afterLast('App\Http\Controllers\Controller', '\\');

// 'Controller'
```

<a name="method-str-apa"></a>
#### `Str::apa()` {.collection-method}

Метод `Str::apa` перетворює заданий рядок на заголовний регістр за [настановами APA](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case):

```php
use Illuminate\Support\Str;

$title = Str::apa('Creating A Project');

// 'Creating a Project'
```

<a name="method-str-ascii"></a>
#### `Str::ascii()` {.collection-method}

Метод `Str::ascii` спробує транслітерувати рядок у значення ASCII:

```php
use Illuminate\Support\Str;

$slice = Str::ascii('û');

// 'u'
```

<a name="method-str-before"></a>
#### `Str::before()` {.collection-method}

Метод `Str::before` повертає все, що йде в рядку до заданого значення:

```php
use Illuminate\Support\Str;

$slice = Str::before('This is my name', 'my name');

// 'This is '
```

<a name="method-str-before-last"></a>
#### `Str::beforeLast()` {.collection-method}

Метод `Str::beforeLast` повертає все, що йде в рядку до останнього входження заданого значення:

```php
use Illuminate\Support\Str;

$slice = Str::beforeLast('This is my name', 'is');

// 'This '
```

<a name="method-str-between"></a>
#### `Str::between()` {.collection-method}

Метод `Str::between` повертає частину рядка між двома значеннями:

```php
use Illuminate\Support\Str;

$slice = Str::between('This is my name', 'This', 'name');

// ' is my '
```

<a name="method-str-between-first"></a>
#### `Str::betweenFirst()` {.collection-method}

Метод `Str::betweenFirst` повертає найменшу можливу частину рядка між двома значеннями:

```php
use Illuminate\Support\Str;

$slice = Str::betweenFirst('[a] bc [d]', '[', ']');

// 'a'
```

<a name="method-camel-case"></a>
#### `Str::camel()` {.collection-method}

Метод `Str::camel` перетворює заданий рядок на `camelCase`:

```php
use Illuminate\Support\Str;

$converted = Str::camel('foo_bar');

// 'fooBar'
```

<a name="method-char-at"></a>
#### `Str::charAt()` {.collection-method}

Метод `Str::charAt` повертає символ за вказаним індексом. Якщо індекс поза межами рядка, повертається `false`:

```php
use Illuminate\Support\Str;

$character = Str::charAt('This is my name.', 6);

// 's'
```

<a name="method-str-chop-start"></a>
#### `Str::chopStart()` {.collection-method}

Метод `Str::chopStart` видаляє перше входження заданого значення лише тоді, коли воно стоїть на початку рядка:

```php
use Illuminate\Support\Str;

$url = Str::chopStart('https://laravel.com', 'https://');

// 'laravel.com'
```

Другим аргументом можна також передати масив. Якщо рядок починається з будь-якого зі значень масиву, це значення буде з нього видалено:

```php
use Illuminate\Support\Str;

$url = Str::chopStart('http://laravel.com', ['https://', 'http://']);

// 'laravel.com'
```

<a name="method-str-chop-end"></a>
#### `Str::chopEnd()` {.collection-method}

Метод `Str::chopEnd` видаляє останнє входження заданого значення лише тоді, коли воно стоїть у кінці рядка:

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('app/Models/Photograph.php', '.php');

// 'app/Models/Photograph'
```

Другим аргументом можна також передати масив. Якщо рядок закінчується будь-яким зі значень масиву, це значення буде з нього видалено:

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('laravel.com/index.php', ['/index.html', '/index.php']);

// 'laravel.com'
```

<a name="method-str-contains"></a>
#### `Str::contains()` {.collection-method}

Метод `Str::contains` визначає, чи містить заданий рядок задане значення. За замовчуванням метод чутливий до регістру:

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'my');

// true
```

Ви можете також передати масив значень, щоб перевірити, чи містить рядок будь-яке зі значень масиву:

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', ['my', 'foo']);

// true
```

Вимкнути чутливість до регістру можна, задавши аргументу `ignoreCase` значення `true`:

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'MY', ignoreCase: true);

// true
```

<a name="method-str-contains-all"></a>
#### `Str::containsAll()` {.collection-method}

Метод `Str::containsAll` визначає, чи містить заданий рядок усі значення із заданого масиву:

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['my', 'name']);

// true
```

Вимкнути чутливість до регістру можна, задавши аргументу `ignoreCase` значення `true`:

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['MY', 'NAME'], ignoreCase: true);

// true
```

<a name="method-str-doesnt-contain"></a>
#### `Str::doesntContain()` {.collection-method}

Метод `Str::doesntContain` визначає, чи не містить заданий рядок задане значення. За замовчуванням метод чутливий до регістру:

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'my');

// true
```

Ви можете також передати масив значень, щоб перевірити, чи не містить рядок жодного зі значень масиву:

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', ['my', 'framework']);

// true
```

Вимкнути чутливість до регістру можна, задавши аргументу `ignoreCase` значення `true`:

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'MY', ignoreCase: true);

// true
```

<a name="method-deduplicate"></a>
#### `Str::deduplicate()` {.collection-method}

Метод `Str::deduplicate` замінює послідовні входження символу в заданому рядку одним таким символом. За замовчуванням метод дедуплікує пробіли:

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The   Laravel   Framework');

// The Laravel Framework
```

Ви можете вказати інший символ для дедуплікації, передавши його другим аргументом методу:

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The---Laravel---Framework', '-');

// The-Laravel-Framework
```

<a name="method-str-doesnt-end-with"></a>
#### `Str::doesntEndWith()` {.collection-method}

Метод `Str::doesntEndWith` визначає, чи не закінчується заданий рядок заданим значенням:

```php
use Illuminate\Support\Str;

$result = Str::doesntEndWith('This is my name', 'dog');

// true
```

Ви можете також передати масив значень, щоб перевірити, чи не закінчується рядок жодним зі значень масиву:

```php
use Illuminate\Support\Str;

$result = Str::doesntEndWith('This is my name', ['this', 'foo']);

// true

$result = Str::doesntEndWith('This is my name', ['name', 'foo']);

// false
```

<a name="method-str-doesnt-start-with"></a>
#### `Str::doesntStartWith()` {.collection-method}

Метод `Str::doesntStartWith` визначає, чи не починається заданий рядок заданим значенням:

```php
use Illuminate\Support\Str;

$result = Str::doesntStartWith('This is my name', 'That');

// true
```

Якщо передати масив можливих значень, метод `doesntStartWith` повернає `true`, коли рядок не починається жодним із заданих значень:

```php
$result = Str::doesntStartWith('This is my name', ['What', 'That', 'There']);

// true
```

<a name="method-ends-with"></a>
#### `Str::endsWith()` {.collection-method}

Метод `Str::endsWith` визначає, чи закінчується заданий рядок заданим значенням:

```php
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', 'name');

// true
```

Ви можете також передати масив значень, щоб перевірити, чи закінчується рядок будь-яким зі значень масиву:

```php
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', ['name', 'foo']);

// true

$result = Str::endsWith('This is my name', ['this', 'foo']);

// false
```

<a name="method-excerpt"></a>
#### `Str::excerpt()` {.collection-method}

Метод `Str::excerpt` дістає із заданого рядка уривок навколо першого входження заданої фрази:

```php
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'my', [
    'radius' => 3
]);

// '...is my na...'
```

Опція `radius`, що за замовчуванням дорівнює `100`, задає кількість символів, які мають з'явитися з кожного боку обрізаного рядка.

Крім того, опцією `omission` можна задати рядок, який буде додано на початку та в кінці обрізаного рядка:

```php
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'name', [
    'radius' => 3,
    'omission' => '(...) '
]);

// '(...) my name'
```

<a name="method-str-finish"></a>
#### `Str::finish()` {.collection-method}

Метод `Str::finish` додає до рядка одне входження заданого значення, якщо рядок ще не закінчується цим значенням:

```php
use Illuminate\Support\Str;

$adjusted = Str::finish('this/string', '/');

// this/string/

$adjusted = Str::finish('this/string/', '/');

// this/string/
```

<a name="method-str-from-base64"></a>
#### `Str::fromBase64()` {.collection-method}

Метод `Str::fromBase64` декодує заданий рядок Base64:

```php
use Illuminate\Support\Str;

$decoded = Str::fromBase64('TGFyYXZlbA==');

// Laravel
```

<a name="method-str-headline"></a>
#### `Str::headline()` {.collection-method}

Метод `Str::headline` перетворює рядки, розділені регістром, дефісами чи підкресленнями, на рядок, розділений пробілами, де перша літера кожного слова велика:

```php
use Illuminate\Support\Str;

$headline = Str::headline('steve_jobs');

// Steve Jobs

$headline = Str::headline('EmailNotificationSent');

// Email Notification Sent
```

<a name="method-str-initials"></a>
#### `Str::initials()` {.collection-method}

Метод `Str::initials` повертає ініціали заданого рядка, за бажанням переводячи їх у верхній регістр:

```php
use Illuminate\Support\Str;

$initials = Str::initials('taylor otwell');

// to

$initials = Str::initials('taylor otwell', capitalize: true);

// TO
```

<a name="method-str-inline-markdown"></a>
#### `Str::inlineMarkdown()` {.collection-method}

Метод `Str::inlineMarkdown` перетворює Markdown у стилі GitHub на інлайновий HTML за допомогою [CommonMark](https://commonmark.thephpleague.com/). Проте, на відміну від методу `markdown`, він не обгортає весь згенерований HTML у блоковий елемент:

```php
use Illuminate\Support\Str;

$html = Str::inlineMarkdown('**Laravel**');

// <strong>Laravel</strong>
```

#### Безпека Markdown

За замовчуванням Markdown підтримує сирий HTML, а це відкриває вразливість до міжсайтового скриптингу (XSS), якщо подавати туди сирий користувацький ввід. Як радить [документація з безпеки CommonMark](https://commonmark.thephpleague.com/security/), ви можете скористатися опцією `html_input`, щоб екранувати чи вирізати сирий HTML, і опцією `allow_unsafe_links`, щоб указати, чи дозволяти небезпечні посилання. Якщо вам потрібно дозволити частину сирого HTML, проженіть скомпільований Markdown через HTML Purifier:

```php
use Illuminate\Support\Str;

Str::inlineMarkdown('Inject: <script>alert("Hello XSS!");</script>', [
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// Inject: alert(&quot;Hello XSS!&quot;);
```

<a name="method-str-is"></a>
#### `Str::is()` {.collection-method}

Метод `Str::is` визначає, чи відповідає заданий рядок заданому шаблону. Зірочки можна використовувати як символи підстановки:

```php
use Illuminate\Support\Str;

$matches = Str::is('foo*', 'foobar');

// true

$matches = Str::is('baz*', 'foobar');

// false
```

Вимкнути чутливість до регістру можна, задавши аргументу `ignoreCase` значення `true`:

```php
use Illuminate\Support\Str;

$matches = Str::is('*.jpg', 'photo.JPG', ignoreCase: true);

// true
```

<a name="method-str-is-ascii"></a>
#### `Str::isAscii()` {.collection-method}

Метод `Str::isAscii` визначає, чи є заданий рядок 7-бітним ASCII:

```php
use Illuminate\Support\Str;

$isAscii = Str::isAscii('Taylor');

// true

$isAscii = Str::isAscii('ü');

// false
```

<a name="method-str-is-json"></a>
#### `Str::isJson()` {.collection-method}

Метод `Str::isJson` визначає, чи є заданий рядок коректним JSON:

```php
use Illuminate\Support\Str;

$result = Str::isJson('[1,2,3]');

// true

$result = Str::isJson('{"first": "John", "last": "Doe"}');

// true

$result = Str::isJson('{first: "John", last: "Doe"}');

// false
```

<a name="method-str-is-url"></a>
#### `Str::isUrl()` {.collection-method}

Метод `Str::isUrl` визначає, чи є заданий рядок коректним URL:

```php
use Illuminate\Support\Str;

$isUrl = Str::isUrl('http://example.com');

// true

$isUrl = Str::isUrl('laravel');

// false
```

Метод `isUrl` вважає коректними чимало протоколів. Втім, ви можете вказати, які протоколи вважати коректними, передавши їх методу `isUrl`:

```php
$isUrl = Str::isUrl('http://example.com', ['http', 'https']);
```

<a name="method-str-is-ulid"></a>
#### `Str::isUlid()` {.collection-method}

Метод `Str::isUlid` визначає, чи є заданий рядок коректним ULID:

```php
use Illuminate\Support\Str;

$isUlid = Str::isUlid('01gd6r360bp37zj17nxb55yv40');

// true

$isUlid = Str::isUlid('laravel');

// false
```

<a name="method-str-is-uuid"></a>
#### `Str::isUuid()` {.collection-method}

Метод `Str::isUuid` визначає, чи є заданий рядок коректним UUID:

```php
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de');

// true

$isUuid = Str::isUuid('laravel');

// false
```

Ви можете також перевірити, чи відповідає заданий UUID специфікації певної версії (1, 3, 4, 5, 6, 7 або 8):

```php
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de', version: 4);

// true

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de', version: 1);

// false
```

<a name="method-kebab-case"></a>
#### `Str::kebab()` {.collection-method}

Метод `Str::kebab` перетворює заданий рядок на `kebab-case`:

```php
use Illuminate\Support\Str;

$converted = Str::kebab('fooBar');

// foo-bar
```

<a name="method-str-lcfirst"></a>
#### `Str::lcfirst()` {.collection-method}

Метод `Str::lcfirst` повертає заданий рядок, у якому перший символ переведено в нижній регістр:

```php
use Illuminate\Support\Str;

$string = Str::lcfirst('Foo Bar');

// foo Bar
```

<a name="method-str-length"></a>
#### `Str::length()` {.collection-method}

Метод `Str::length` повертає довжину заданого рядка:

```php
use Illuminate\Support\Str;

$length = Str::length('Laravel');

// 7
```

<a name="method-str-limit"></a>
#### `Str::limit()` {.collection-method}

Метод `Str::limit` обрізає заданий рядок до вказаної довжини:

```php
use Illuminate\Support\Str;

$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20);

// The quick brown fox...
```

Третім аргументом методу можна змінити рядок, який буде дописано в кінці обрізаного рядка:

```php
$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20, ' (...)');

// The quick brown fox (...)
```

Якщо ви хочете зберегти цілі слова під час обрізання, скористайтеся аргументом `preserveWords`. Коли він `true`, рядок буде обрізано до найближчої межі цілого слова:

```php
$truncated = Str::limit('The quick brown fox', 12, preserveWords: true);

// The quick...
```

<a name="method-str-lower"></a>
#### `Str::lower()` {.collection-method}

Метод `Str::lower` переводить заданий рядок у нижній регістр:

```php
use Illuminate\Support\Str;

$converted = Str::lower('LARAVEL');

// laravel
```

<a name="method-str-markdown"></a>
#### `Str::markdown()` {.collection-method}

Метод `Str::markdown` перетворює Markdown у стилі GitHub на HTML за допомогою [CommonMark](https://commonmark.thephpleague.com/):

```php
use Illuminate\Support\Str;

$html = Str::markdown('# Laravel');

// <h1>Laravel</h1>

$html = Str::markdown('# Taylor <b>Otwell</b>', [
    'html_input' => 'strip',
]);

// <h1>Taylor Otwell</h1>
```

#### Безпека Markdown

За замовчуванням Markdown підтримує сирий HTML, а це відкриває вразливість до міжсайтового скриптингу (XSS), якщо подавати туди сирий користувацький ввід. Як радить [документація з безпеки CommonMark](https://commonmark.thephpleague.com/security/), ви можете скористатися опцією `html_input`, щоб екранувати чи вирізати сирий HTML, і опцією `allow_unsafe_links`, щоб указати, чи дозволяти небезпечні посилання. Якщо вам потрібно дозволити частину сирого HTML, проженіть скомпільований Markdown через HTML Purifier:

```php
use Illuminate\Support\Str;

Str::markdown('Inject: <script>alert("Hello XSS!");</script>', [
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// <p>Inject: alert(&quot;Hello XSS!&quot;);</p>
```

<a name="method-str-mask"></a>
#### `Str::mask()` {.collection-method}

Метод `Str::mask` маскує частину рядка повторюваним символом; ним можна приховувати фрагменти рядків - наприклад, адреси електронної пошти чи номери телефонів:

```php
use Illuminate\Support\Str;

$string = Str::mask('taylor@example.com', '*', 3);

// tay***************
```

За потреби третім аргументом методу `mask` можна передати від'ємне число - тоді маскування почнеться на заданій відстані від кінця рядка:

```php
$string = Str::mask('taylor@example.com', '*', -15, 3);

// tay***@example.com
```

<a name="method-str-match"></a>
#### `Str::match()` {.collection-method}

Метод `Str::match` повертає частину рядка, що відповідає заданому шаблону регулярного виразу:

```php
use Illuminate\Support\Str;

$result = Str::match('/bar/', 'foo bar');

// 'bar'

$result = Str::match('/foo (.*)/', 'foo bar');

// 'bar'
```

<a name="method-str-match-all"></a>
#### `Str::matchAll()` {.collection-method}

Метод `Str::matchAll` повертає колекцію з частинами рядка, що відповідають заданому шаблону регулярного виразу:

```php
use Illuminate\Support\Str;

$result = Str::matchAll('/bar/', 'bar foo bar');

// collect(['bar', 'bar'])
```

Якщо ви вкажете у виразі групу захоплення, Laravel повернає колекцію збігів першої такої групи:

```php
use Illuminate\Support\Str;

$result = Str::matchAll('/f(\w*)/', 'bar fun bar fly');

// collect(['un', 'ly']);
```

Якщо збігів не знайдено, буде повернуто порожню колекцію.

<a name="method-str-is-match"></a>
#### `Str::isMatch()` {.collection-method}

Метод `Str::isMatch` повертає `true`, якщо рядок відповідає заданому регулярному виразу:

```php
use Illuminate\Support\Str;

$result = Str::isMatch('/foo (.*)/', 'foo bar');

// true

$result = Str::isMatch('/foo (.*)/', 'laravel');

// false
```

<a name="method-str-ordered-uuid"></a>
#### `Str::orderedUuid()` {.collection-method}

Метод `Str::orderedUuid` генерує UUID, у якому першою йде часова позначка, - такий UUID ефективно зберігати в проіндексованому стовпці бази даних. Кожен згенерований цим методом UUID сортуватиметься після UUID, згенерованих ним раніше:

```php
use Illuminate\Support\Str;

return (string) Str::orderedUuid();
```

<a name="method-str-padboth"></a>
#### `Str::padBoth()` {.collection-method}

Метод `Str::padBoth` обгортає PHP-функцію `str_pad` і доповнює рядок з обох боків іншим рядком, доки той не досягне потрібної довжини:

```php
use Illuminate\Support\Str;

$padded = Str::padBoth('James', 10, '_');

// '__James___'

$padded = Str::padBoth('James', 10);

// '  James   '
```

<a name="method-str-padleft"></a>
#### `Str::padLeft()` {.collection-method}

Метод `Str::padLeft` обгортає PHP-функцію `str_pad` і доповнює рядок зліва іншим рядком, доки той не досягне потрібної довжини:

```php
use Illuminate\Support\Str;

$padded = Str::padLeft('James', 10, '-=');

// '-=-=-James'

$padded = Str::padLeft('James', 10);

// '     James'
```

<a name="method-str-padright"></a>
#### `Str::padRight()` {.collection-method}

Метод `Str::padRight` обгортає PHP-функцію `str_pad` і доповнює рядок справа іншим рядком, доки той не досягне потрібної довжини:

```php
use Illuminate\Support\Str;

$padded = Str::padRight('James', 10, '-');

// 'James-----'

$padded = Str::padRight('James', 10);

// 'James     '
```

<a name="method-str-password"></a>
#### `Str::password()` {.collection-method}

Методом `Str::password` можна згенерувати надійний випадковий пароль заданої довжини. Пароль складатиметься з літер, цифр, символів і пробілів. За замовчуванням довжина пароля - 32 символи:

```php
use Illuminate\Support\Str;

$password = Str::password();

// 'EbJo2vE-AS:U,$%_gkrV4n,q~1xy/-_4'

$password = Str::password(12);

// 'qwuar>#V|i]N'
```

<a name="method-str-counted"></a>
#### `Str::counted()` {.collection-method}

Метод `Str::counted` перетворює слово в однині на однину чи множину залежно від заданої кількості й додає перед результатом відформатовану кількість:

```php
use Illuminate\Support\Str;

$label = Str::counted('order', 1);

// 1 order

$label = Str::counted('order', 1000);

// 1,000 orders
```

<a name="method-str-plural"></a>
#### `Str::plural()` {.collection-method}

Метод `Str::plural` перетворює слово в однині на форму множини. Ця функція підтримує [будь-яку з мов, які підтримує плюралізатор Laravel](/docs/{{version}}/localization#pluralization-language):

```php
use Illuminate\Support\Str;

$plural = Str::plural('car');

// cars

$plural = Str::plural('child');

// children
```

Другим аргументом функції можна передати ціле число, щоб отримати форму однини або множини:

```php
use Illuminate\Support\Str;

$plural = Str::plural('child', 2);

// children

$singular = Str::plural('child', 1);

// child
```

Аргументом `prependCount` можна додати перед формою множини відформатоване значення `$count`:

```php
use Illuminate\Support\Str;

$label = Str::plural('car', 1000, prependCount: true);

// 1,000 cars
```

<a name="method-str-plural-studly"></a>
#### `Str::pluralStudly()` {.collection-method}

Метод `Str::pluralStudly` перетворює слово в однині, записане в studly caps, на форму множини. Ця функція підтримує [будь-яку з мов, які підтримує плюралізатор Laravel](/docs/{{version}}/localization#pluralization-language):

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman');

// VerifiedHumans

$plural = Str::pluralStudly('UserFeedback');

// UserFeedback
```

Другим аргументом функції можна передати ціле число, щоб отримати форму однини або множини:

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman', 2);

// VerifiedHumans

$singular = Str::pluralStudly('VerifiedHuman', 1);

// VerifiedHuman
```

<a name="method-str-position"></a>
#### `Str::position()` {.collection-method}

Метод `Str::position` повертає позицію першого входження підрядка в рядок. Якщо підрядка в заданому рядку немає, повертається `false`:

```php
use Illuminate\Support\Str;

$position = Str::position('Hello, World!', 'Hello');

// 0

$position = Str::position('Hello, World!', 'W');

// 7
```

<a name="method-str-random"></a>
#### `Str::random()` {.collection-method}

Метод `Str::random` генерує випадковий рядок указаної довжини. Ця функція використовує PHP-функцію `random_bytes`:

```php
use Illuminate\Support\Str;

$random = Str::random(40);
```

Під час тестування буває корисно «підмінити» значення, яке повертає метод `Str::random`. Для цього скористайтеся методом `createRandomStringsUsing`:

```php
Str::createRandomStringsUsing(function () {
    return 'fake-random-string';
});
```

Щоб метод `random` знову генерував випадкові рядки як звичайно, викличте метод `createRandomStringsNormally`:

```php
Str::createRandomStringsNormally();
```

<a name="method-str-remove"></a>
#### `Str::remove()` {.collection-method}

Метод `Str::remove` видаляє з рядка задане значення або масив значень:

```php
use Illuminate\Support\Str;

$string = 'Peter Piper picked a peck of pickled peppers.';

$removed = Str::remove('e', $string);

// Ptr Pipr pickd a pck of pickld ppprs.
```

Ви можете також передати третім аргументом `false`, щоб метод `remove` не звертав уваги на регістр.

<a name="method-str-repeat"></a>
#### `Str::repeat()` {.collection-method}

Метод `Str::repeat` повторює заданий рядок:

```php
use Illuminate\Support\Str;

$string = 'a';

$repeat = Str::repeat($string, 5);

// aaaaa
```

<a name="method-str-replace"></a>
#### `Str::replace()` {.collection-method}

Метод `Str::replace` замінює в рядку заданий рядок:

```php
use Illuminate\Support\Str;

$string = 'Laravel 11.x';

$replaced = Str::replace('11.x', '12.x', $string);

// Laravel 12.x
```

Метод `replace` приймає також аргумент `caseSensitive`. За замовчуванням метод `replace` чутливий до регістру:

```php
$replaced = Str::replace(
    'php',
    'Laravel',
    'PHP Framework for Web Artisans',
    caseSensitive: false
);

// Laravel Framework for Web Artisans
```

<a name="method-str-replace-array"></a>
#### `Str::replaceArray()` {.collection-method}

Метод `Str::replaceArray` послідовно замінює задане значення в рядку значеннями з масиву:

```php
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::replaceArray('?', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-replace-first"></a>
#### `Str::replaceFirst()` {.collection-method}

Метод `Str::replaceFirst` замінює перше входження заданого значення в рядку:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog');

// a quick brown fox jumps over the lazy dog
```

<a name="method-str-replace-last"></a>
#### `Str::replaceLast()` {.collection-method}

Метод `Str::replaceLast` замінює останнє входження заданого значення в рядку:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog');

// the quick brown fox jumps over a lazy dog
```

<a name="method-str-replace-matches"></a>
#### `Str::replaceMatches()` {.collection-method}

Метод `Str::replaceMatches` замінює всі частини рядка, що відповідають шаблону, заданим рядком заміни:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceMatches(
    pattern: '/[^A-Za-z0-9]++/',
    replace: '',
    subject: '(+1) 501-555-1000'
)

// '15015551000'
```

Метод `replaceMatches` приймає також замикання, яке буде викликано для кожної частини рядка, що відповідає заданому шаблону: у ньому ви виконуєте логіку заміни й повертаєте замінене значення:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceMatches('/\d/', function (array $matches) {
    return '['.$matches[0].']';
}, '123');

// '[1][2][3]'
```

<a name="method-str-replace-start"></a>
#### `Str::replaceStart()` {.collection-method}

Метод `Str::replaceStart` замінює перше входження заданого значення лише тоді, коли воно стоїть на початку рядка:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceStart('Hello', 'Laravel', 'Hello World');

// Laravel World

$replaced = Str::replaceStart('World', 'Laravel', 'Hello World');

// Hello World
```

<a name="method-str-replace-end"></a>
#### `Str::replaceEnd()` {.collection-method}

Метод `Str::replaceEnd` замінює останнє входження заданого значення лише тоді, коли воно стоїть у кінці рядка:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceEnd('World', 'Laravel', 'Hello World');

// Hello Laravel

$replaced = Str::replaceEnd('Hello', 'Laravel', 'Hello World');

// Hello World
```

<a name="method-str-reverse"></a>
#### `Str::reverse()` {.collection-method}

Метод `Str::reverse` перевертає заданий рядок:

```php
use Illuminate\Support\Str;

$reversed = Str::reverse('Hello World');

// dlroW olleH
```

<a name="method-str-singular"></a>
#### `Str::singular()` {.collection-method}

Метод `Str::singular` перетворює рядок на форму однини. Ця функція підтримує [будь-яку з мов, які підтримує плюралізатор Laravel](/docs/{{version}}/localization#pluralization-language):

```php
use Illuminate\Support\Str;

$singular = Str::singular('cars');

// car

$singular = Str::singular('children');

// child
```

<a name="method-str-slug"></a>
#### `Str::slug()` {.collection-method}

Метод `Str::slug` генерує із заданого рядка дружній до URL «slug»:

```php
use Illuminate\Support\Str;

$slug = Str::slug('Laravel 5 Framework', '-');

// laravel-5-framework
```

<a name="method-snake-case"></a>
#### `Str::snake()` {.collection-method}

Метод `Str::snake` перетворює заданий рядок на `snake_case`:

```php
use Illuminate\Support\Str;

$converted = Str::snake('fooBar');

// foo_bar

$converted = Str::snake('fooBar', '-');

// foo-bar
```

<a name="method-str-squish"></a>
#### `Str::squish()` {.collection-method}

Метод `Str::squish` прибирає з рядка всі надлишкові пробіли, зокрема й між словами:

```php
use Illuminate\Support\Str;

$string = Str::squish('    laravel    framework    ');

// laravel framework
```

<a name="method-str-start"></a>
#### `Str::start()` {.collection-method}

Метод `Str::start` додає до рядка одне входження заданого значення, якщо рядок ще не починається цим значенням:

```php
use Illuminate\Support\Str;

$adjusted = Str::start('this/string', '/');

// /this/string

$adjusted = Str::start('/this/string', '/');

// /this/string
```

<a name="method-starts-with"></a>
#### `Str::startsWith()` {.collection-method}

Метод `Str::startsWith` визначає, чи починається заданий рядок заданим значенням:

```php
use Illuminate\Support\Str;

$result = Str::startsWith('This is my name', 'This');

// true
```

Якщо передати масив можливих значень, метод `startsWith` повернає `true`, коли рядок починається будь-яким із заданих значень:

```php
$result = Str::startsWith('This is my name', ['This', 'That', 'There']);

// true
```

<a name="method-studly-case"></a>
#### `Str::studly()` {.collection-method}

Метод `Str::studly` перетворює заданий рядок на `StudlyCase`:

```php
use Illuminate\Support\Str;

$converted = Str::studly('foo_bar');

// FooBar
```

<a name="method-str-substr"></a>
#### `Str::substr()` {.collection-method}

Метод `Str::substr` повертає частину рядка, задану параметрами початку та довжини:

```php
use Illuminate\Support\Str;

$converted = Str::substr('The Laravel Framework', 4, 7);

// Laravel
```

<a name="method-str-substrcount"></a>
#### `Str::substrCount()` {.collection-method}

Метод `Str::substrCount` повертає кількість входжень заданого значення в заданому рядку:

```php
use Illuminate\Support\Str;

$count = Str::substrCount('If you like ice cream, you will like snow cones.', 'like');

// 2
```

<a name="method-str-substrreplace"></a>
#### `Str::substrReplace()` {.collection-method}

Метод `Str::substrReplace` замінює текст у частині рядка, починаючи з позиції, заданої третім аргументом, і замінюючи стільку символів, скільки задано четвертим аргументом. Якщо передати четвертим аргументом `0`, рядок буде вставлено у вказану позицію, не замінюючи жодного наявного символу:

```php
use Illuminate\Support\Str;

$result = Str::substrReplace('1300', ':', 2);
// 13:

$result = Str::substrReplace('1300', ':', 2, 0);
// 13:00
```

<a name="method-str-swap"></a>
#### `Str::swap()` {.collection-method}

Метод `Str::swap` замінює в заданому рядку кілька значень за допомогою PHP-функції `strtr`:

```php
use Illuminate\Support\Str;

$string = Str::swap([
    'Tacos' => 'Burritos',
    'great' => 'fantastic',
], 'Tacos are great!');

// Burritos are fantastic!
```

<a name="method-take"></a>
#### `Str::take()` {.collection-method}

Метод `Str::take` повертає вказану кількість символів із початку рядка:

```php
use Illuminate\Support\Str;

$taken = Str::take('Build something amazing!', 5);

// Build
```

<a name="method-title-case"></a>
#### `Str::title()` {.collection-method}

Метод `Str::title` перетворює заданий рядок на `Title Case`:

```php
use Illuminate\Support\Str;

$converted = Str::title('a nice title uses the correct case');

// A Nice Title Uses The Correct Case
```

<a name="method-str-to-base64"></a>
#### `Str::toBase64()` {.collection-method}

Метод `Str::toBase64` перетворює заданий рядок на Base64:

```php
use Illuminate\Support\Str;

$base64 = Str::toBase64('Laravel');

// TGFyYXZlbA==
```

<a name="method-str-transliterate"></a>
#### `Str::transliterate()` {.collection-method}

Метод `Str::transliterate` спробує перетворити заданий рядок на найближче представлення в ASCII:

```php
use Illuminate\Support\Str;

$email = Str::transliterate('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ');

// 'test@laravel.com'
```

<a name="method-str-trim"></a>
#### `Str::trim()` {.collection-method}

Метод `Str::trim` прибирає пробіли (чи інші символи) з початку та кінця заданого рядка. На відміну від нативної PHP-функції `trim`, метод `Str::trim` прибирає ще й пробільні символи Unicode:

```php
use Illuminate\Support\Str;

$string = Str::trim(' foo bar ');

// 'foo bar'
```

<a name="method-str-ltrim"></a>
#### `Str::ltrim()` {.collection-method}

Метод `Str::ltrim` прибирає пробіли (чи інші символи) з початку заданого рядка. На відміну від нативної PHP-функції `ltrim`, метод `Str::ltrim` прибирає ще й пробільні символи Unicode:

```php
use Illuminate\Support\Str;

$string = Str::ltrim('  foo bar  ');

// 'foo bar  '
```

<a name="method-str-rtrim"></a>
#### `Str::rtrim()` {.collection-method}

Метод `Str::rtrim` прибирає пробіли (чи інші символи) з кінця заданого рядка. На відміну від нативної PHP-функції `rtrim`, метод `Str::rtrim` прибирає ще й пробільні символи Unicode:

```php
use Illuminate\Support\Str;

$string = Str::rtrim('  foo bar  ');

// '  foo bar'
```

<a name="method-str-ucfirst"></a>
#### `Str::ucfirst()` {.collection-method}

Метод `Str::ucfirst` повертає заданий рядок, у якому перший символ переведено у верхній регістр:

```php
use Illuminate\Support\Str;

$string = Str::ucfirst('foo bar');

// Foo bar
```

<a name="method-str-ucsplit"></a>
#### `Str::ucsplit()` {.collection-method}

Метод `Str::ucsplit` розбиває заданий рядок на масив за великими літерами:

```php
use Illuminate\Support\Str;

$segments = Str::ucsplit('FooBar');

// [0 => 'Foo', 1 => 'Bar']
```

<a name="method-str-ucwords"></a>
#### `Str::ucwords()` {.collection-method}

Метод `Str::ucwords` переводить перший символ кожного слова в заданому рядку у верхній регістр:

```php
use Illuminate\Support\Str;

$string = Str::ucwords('laravel framework');

// Laravel Framework
```

<a name="method-str-upper"></a>
#### `Str::upper()` {.collection-method}

Метод `Str::upper` переводить заданий рядок у верхній регістр:

```php
use Illuminate\Support\Str;

$string = Str::upper('laravel');

// LARAVEL
```

<a name="method-str-ulid"></a>
#### `Str::ulid()` {.collection-method}

Метод `Str::ulid` генерує ULID - компактний унікальний ідентифікатор, упорядкований за часом:

```php
use Illuminate\Support\Str;

return (string) Str::ulid();

// 01gd6r360bp37zj17nxb55yv40
```

Якщо ви хочете отримати екземпляр дати `Illuminate\Support\Carbon`, що відповідає даті й часу створення заданого ULID, скористайтеся методом `createFromId` з інтеграції Carbon у Laravel:

```php
use Illuminate\Support\Carbon;
use Illuminate\Support\Str;

$date = Carbon::createFromId((string) Str::ulid());
```

Під час тестування буває корисно «підмінити» значення, яке повертає метод `Str::ulid`. Для цього скористайтеся методом `createUlidsUsing`:

```php
use Symfony\Component\Uid\Ulid;

Str::createUlidsUsing(function () {
    return new Ulid('01HRDBNHHCKNW2AK4Z29SN82T9');
});
```

Щоб метод `ulid` знову генерував ULID як звичайно, викличте метод `createUlidsNormally`:

```php
Str::createUlidsNormally();
```

<a name="method-str-unwrap"></a>
#### `Str::unwrap()` {.collection-method}

Метод `Str::unwrap` прибирає вказані рядки з початку та кінця заданого рядка:

```php
use Illuminate\Support\Str;

Str::unwrap('-Laravel-', '-');

// Laravel

Str::unwrap('{framework: "Laravel"}', '{', '}');

// framework: "Laravel"
```

<a name="method-str-uuid"></a>
#### `Str::uuid()` {.collection-method}

Метод `Str::uuid` генерує UUID (версії 4):

```php
use Illuminate\Support\Str;

return (string) Str::uuid();
```

Під час тестування буває корисно «підмінити» значення, яке повертає метод `Str::uuid`. Для цього скористайтеся методом `createUuidsUsing`:

```php
use Ramsey\Uuid\Uuid;

Str::createUuidsUsing(function () {
    return Uuid::fromString('eadbfeac-5258-45c2-bab7-ccb9b5ef74f9');
});
```

Щоб метод `uuid` знову генерував UUID як звичайно, викличте метод `createUuidsNormally`:

```php
Str::createUuidsNormally();
```

<a name="method-str-uuid7"></a>
#### `Str::uuid7()` {.collection-method}

Метод `Str::uuid7` генерує UUID (версії 7):

```php
use Illuminate\Support\Str;

return (string) Str::uuid7();
```

Необов'язковим параметром можна передати `DateTimeInterface`, який буде використано для генерації впорядкованого UUID:

```php
return (string) Str::uuid7(time: now());
```

<a name="method-str-word-count"></a>
#### `Str::wordCount()` {.collection-method}

Метод `Str::wordCount` повертає кількість слів у рядку:

```php
use Illuminate\Support\Str;

Str::wordCount('Hello, world!'); // 2
```

<a name="method-str-word-wrap"></a>
#### `Str::wordWrap()` {.collection-method}

Метод `Str::wordWrap` переносить рядок по заданій кількості символів:

```php
use Illuminate\Support\Str;

$text = "The quick brown fox jumped over the lazy dog."

Str::wordWrap($text, characters: 20, break: "<br />\n");

/*
The quick brown fox<br />
jumped over the lazy<br />
dog.
*/
```

<a name="method-str-words"></a>
#### `Str::words()` {.collection-method}

Метод `Str::words` обмежує кількість слів у рядку. Третім аргументом методу можна передати додатковий рядок, який буде дописано в кінці обрізаного рядка:

```php
use Illuminate\Support\Str;

return Str::words('Perfectly balanced, as all things should be.', 3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-str-wrap"></a>
#### `Str::wrap()` {.collection-method}

Метод `Str::wrap` обгортає заданий рядок додатковим рядком або парою рядків:

```php
use Illuminate\Support\Str;

Str::wrap('Laravel', '"');

// "Laravel"

Str::wrap('is', before: 'This ', after: ' Laravel!');

// This is Laravel!
```

<a name="method-str"></a>
#### `str()` {.collection-method}

Функція `str` повертає новий екземпляр `Illuminate\Support\Stringable` для заданого рядка. Ця функція рівнозначна методу `Str::of`:

```php
$string = str('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

Якщо функції `str` не передати аргументу, вона повертає екземпляр `Illuminate\Support\Str`:

```php
$snake = str()->snake('FooBar');

// 'foo_bar'
```

<a name="method-trans"></a>
#### `trans()` {.collection-method}

Функція `trans` перекладає заданий ключ перекладу за допомогою ваших [мовних файлів](/docs/{{version}}/localization):

```php
echo trans('messages.welcome');
```

Якщо вказаного ключа перекладу не існує, функція `trans` повернає переданий ключ. Тож у прикладі вище функція `trans` повернула б `messages.welcome`, якби такого ключа перекладу не було.

<a name="method-trans-choice"></a>
#### `trans_choice()` {.collection-method}

Функція `trans_choice` перекладає заданий ключ перекладу з урахуванням числової форми:

```php
echo trans_choice('messages.notifications', $unreadCount);
```

Якщо вказаного ключа перекладу не існує, функція `trans_choice` повернає переданий ключ. Тож у прикладі вище функція `trans_choice` повернула б `messages.notifications`, якби такого ключа перекладу не було.

<a name="fluent-strings"></a>
## Плавні рядки

Плавні рядки дають плавніший, об'єктно-орієнтований інтерфейс для роботи з рядковими значеннями: ви можете зчіплювати кілька операцій над рядком ланцюжком, і синтаксис читається краще, ніж у традиційних операціях із рядками.

<a name="method-fluent-str-after"></a>
#### `after` {.collection-method}

Метод `after` повертає все, що йде в рядку після заданого значення. Якщо значення в рядку немає, буде повернуто цілий рядок:

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->after('This is');

// ' my name'
```

<a name="method-fluent-str-after-last"></a>
#### `afterLast` {.collection-method}

Метод `afterLast` повертає все, що йде в рядку після останнього входження заданого значення. Якщо значення в рядку немає, буде повернуто цілий рядок:

```php
use Illuminate\Support\Str;

$slice = Str::of('App\Http\Controllers\Controller')->afterLast('\\');

// 'Controller'
```

<a name="method-fluent-str-apa"></a>
#### `apa` {.collection-method}

Метод `apa` перетворює заданий рядок на заголовний регістр за [настановами APA](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case):

```php
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->apa();

// A Nice Title Uses the Correct Case
```

<a name="method-fluent-str-append"></a>
#### `append` {.collection-method}

Метод `append` дописує задані значення в кінець рядка:

```php
use Illuminate\Support\Str;

$string = Str::of('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

<a name="method-fluent-str-ascii"></a>
#### `ascii` {.collection-method}

Метод `ascii` спробує транслітерувати рядок у значення ASCII:

```php
use Illuminate\Support\Str;

$string = Str::of('ü')->ascii();

// 'u'
```

<a name="method-fluent-str-basename"></a>
#### `basename` {.collection-method}

Метод `basename` повертає останній компонент назви із заданого рядка:

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->basename();

// 'baz'
```

За потреби ви можете передати «розширення», яке буде прибрано з останнього компонента:

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz.jpg')->basename('.jpg');

// 'baz'
```

<a name="method-fluent-str-before"></a>
#### `before` {.collection-method}

Метод `before` повертає все, що йде в рядку до заданого значення:

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->before('my name');

// 'This is '
```

<a name="method-fluent-str-before-last"></a>
#### `beforeLast` {.collection-method}

Метод `beforeLast` повертає все, що йде в рядку до останнього входження заданого значення:

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->beforeLast('is');

// 'This '
```

<a name="method-fluent-str-between"></a>
#### `between` {.collection-method}

Метод `between` повертає частину рядка між двома значеннями:

```php
use Illuminate\Support\Str;

$converted = Str::of('This is my name')->between('This', 'name');

// ' is my '
```

<a name="method-fluent-str-between-first"></a>
#### `betweenFirst` {.collection-method}

Метод `betweenFirst` повертає найменшу можливу частину рядка між двома значеннями:

```php
use Illuminate\Support\Str;

$converted = Str::of('[a] bc [d]')->betweenFirst('[', ']');

// 'a'
```

<a name="method-fluent-str-camel"></a>
#### `camel` {.collection-method}

Метод `camel` перетворює заданий рядок на `camelCase`:

```php
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->camel();

// 'fooBar'
```

<a name="method-fluent-str-char-at"></a>
#### `charAt` {.collection-method}

Метод `charAt` повертає символ за вказаним індексом. Якщо індекс поза межами рядка, повертається `false`:

```php
use Illuminate\Support\Str;

$character = Str::of('This is my name.')->charAt(6);

// 's'
```

<a name="method-fluent-str-class-basename"></a>
#### `classBasename` {.collection-method}

Метод `classBasename` повертає назву заданого класу без його простору імен:

```php
use Illuminate\Support\Str;

$class = Str::of('Foo\Bar\Baz')->classBasename();

// 'Baz'
```

<a name="method-fluent-str-chop-start"></a>
#### `chopStart` {.collection-method}

Метод `chopStart` видаляє перше входження заданого значення лише тоді, коли воно стоїть на початку рядка:

```php
use Illuminate\Support\Str;

$url = Str::of('https://laravel.com')->chopStart('https://');

// 'laravel.com'
```

Ви можете також передати масив. Якщо рядок починається з будь-якого зі значень масиву, це значення буде з нього видалено:

```php
use Illuminate\Support\Str;

$url = Str::of('http://laravel.com')->chopStart(['https://', 'http://']);

// 'laravel.com'
```

<a name="method-fluent-str-chop-end"></a>
#### `chopEnd` {.collection-method}

Метод `chopEnd` видаляє останнє входження заданого значення лише тоді, коли воно стоїть у кінці рядка:

```php
use Illuminate\Support\Str;

$url = Str::of('https://laravel.com')->chopEnd('.com');

// 'https://laravel'
```

Ви можете також передати масив. Якщо рядок закінчується будь-яким зі значень масиву, це значення буде з нього видалено:

```php
use Illuminate\Support\Str;

$url = Str::of('http://laravel.com')->chopEnd(['.com', '.io']);

// 'http://laravel'
```

<a name="method-fluent-str-contains"></a>
#### `contains` {.collection-method}

Метод `contains` визначає, чи містить заданий рядок задане значення. За замовчуванням метод чутливий до регістру:

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('my');

// true
```

Ви можете також передати масив значень, щоб перевірити, чи містить рядок будь-яке зі значень масиву:

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains(['my', 'foo']);

// true
```

Вимкнути чутливість до регістру можна, задавши аргументу `ignoreCase` значення `true`:

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('MY', ignoreCase: true);

// true
```

<a name="method-fluent-str-contains-all"></a>
#### `containsAll` {.collection-method}

Метод `containsAll` визначає, чи містить заданий рядок усі значення із заданого масиву:

```php
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['my', 'name']);

// true
```

Вимкнути чутливість до регістру можна, задавши аргументу `ignoreCase` значення `true`:

```php
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['MY', 'NAME'], ignoreCase: true);

// true
```

<a name="method-fluent-str-decrypt"></a>
#### `decrypt` {.collection-method}

Метод `decrypt` [розшифровує](/docs/{{version}}/encryption) зашифрований рядок:

```php
use Illuminate\Support\Str;

$decrypted = $encrypted->decrypt();

// 'secret'
```

Обернений до `decrypt` - метод [encrypt](#method-fluent-str-encrypt).

<a name="method-fluent-str-deduplicate"></a>
#### `deduplicate` {.collection-method}

Метод `deduplicate` замінює послідовні входження символу в заданому рядку одним таким символом. За замовчуванням метод дедуплікує пробіли:

```php
use Illuminate\Support\Str;

$result = Str::of('The   Laravel   Framework')->deduplicate();

// The Laravel Framework
```

Ви можете вказати інший символ для дедуплікації, передавши його другим аргументом методу:

```php
use Illuminate\Support\Str;

$result = Str::of('The---Laravel---Framework')->deduplicate('-');

// The-Laravel-Framework
```

<a name="method-fluent-str-dirname"></a>
#### `dirname` {.collection-method}

Метод `dirname` повертає частину заданого рядка з батьківським каталогом:

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname();

// '/foo/bar'
```

За потреби ви можете вказати, скільки рівнів каталогів обрізати з рядка:

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname(2);

// '/foo'
```

<a name="method-fluent-str-doesnt-contain"></a>
#### `doesntContain()` {.collection-method}

Метод `doesntContain` визначає, чи не містить заданий рядок задане значення. Цей метод обернений до [contains](#method-fluent-str-contains). За замовчуванням він чутливий до регістру:

```php
use Illuminate\Support\Str;

$doesntContain = Str::of('This is name')->doesntContain('my');

// true
```

Ви можете також передати масив значень, щоб перевірити, чи не містить рядок жодного зі значень масиву:

```php
use Illuminate\Support\Str;

$doesntContain = Str::of('This is name')->doesntContain(['my', 'framework']);

// true
```

Вимкнути чутливість до регістру можна, задавши аргументу `ignoreCase` значення `true`:

```php
use Illuminate\Support\Str;

$doesntContain = Str::of('This is my name')->doesntContain('MY', ignoreCase: true);

// false
```

<a name="method-fluent-str-doesnt-end-with"></a>
#### `doesntEndWith` {.collection-method}

Метод `doesntEndWith` визначає, чи не закінчується заданий рядок заданим значенням:

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntEndWith('dog');

// true
```

Ви можете також передати масив значень, щоб перевірити, чи не закінчується рядок жодним зі значень масиву:

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntEndWith(['this', 'foo']);

// true

$result = Str::of('This is my name')->doesntEndWith(['name', 'foo']);

// false
```

<a name="method-fluent-str-doesnt-start-with"></a>
#### `doesntStartWith` {.collection-method}

Метод `doesntStartWith` визначає, чи не починається заданий рядок заданим значенням:

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntStartWith('That');

// true
```

Ви можете також передати масив значень, щоб перевірити, чи не починається рядок жодним зі значень масиву:

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->doesntStartWith(['What', 'That', 'There']);

// true
```

<a name="method-fluent-str-encrypt"></a>
#### `encrypt` {.collection-method}

Метод `encrypt` [шифрує](/docs/{{version}}/encryption) рядок:

```php
use Illuminate\Support\Str;

$encrypted = Str::of('secret')->encrypt();
```

Обернений до `encrypt` - метод [decrypt](#method-fluent-str-decrypt).

<a name="method-fluent-str-ends-with"></a>
#### `endsWith` {.collection-method}

Метод `endsWith` визначає, чи закінчується заданий рядок заданим значенням:

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith('name');

// true
```

Ви можете також передати масив значень, щоб перевірити, чи закінчується рядок будь-яким зі значень масиву:

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith(['name', 'foo']);

// true

$result = Str::of('This is my name')->endsWith(['this', 'foo']);

// false
```

<a name="method-fluent-str-exactly"></a>
#### `exactly` {.collection-method}

Метод `exactly` визначає, чи точно збігається заданий рядок з іншим рядком:

```php
use Illuminate\Support\Str;

$result = Str::of('Laravel')->exactly('Laravel');

// true
```

<a name="method-fluent-str-excerpt"></a>
#### `excerpt` {.collection-method}

Метод `excerpt` дістає з рядка уривок навколо першого входження заданої фрази:

```php
use Illuminate\Support\Str;

$excerpt = Str::of('This is my name')->excerpt('my', [
    'radius' => 3
]);

// '...is my na...'
```

Опція `radius`, що за замовчуванням дорівнює `100`, задає кількість символів, які мають з'явитися з кожного боку обрізаного рядка.

Крім того, опцією `omission` можна змінити рядок, який буде додано на початку та в кінці обрізаного рядка:

```php
use Illuminate\Support\Str;

$excerpt = Str::of('This is my name')->excerpt('name', [
    'radius' => 3,
    'omission' => '(...) '
]);

// '(...) my name'
```

<a name="method-fluent-str-explode"></a>
#### `explode` {.collection-method}

Метод `explode` розбиває рядок за заданим розділювачем і повертає колекцію з кожною частиною розбитого рядка:

```php
use Illuminate\Support\Str;

$collection = Str::of('foo bar baz')->explode(' ');

// collect(['foo', 'bar', 'baz'])
```

<a name="method-fluent-str-finish"></a>
#### `finish` {.collection-method}

Метод `finish` додає до рядка одне входження заданого значення, якщо рядок ще не закінчується цим значенням:

```php
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->finish('/');

// this/string/

$adjusted = Str::of('this/string/')->finish('/');

// this/string/
```

<a name="method-fluent-str-from-base64"></a>
#### `fromBase64` {.collection-method}

Метод `fromBase64` декодує заданий рядок Base64:

```php
use Illuminate\Support\Str;

$decoded = Str::of('TGFyYXZlbA==')->fromBase64();

// Laravel
```

<a name="method-fluent-str-hash"></a>
#### `hash` {.collection-method}

Метод `hash` хешує рядок заданим [алгоритмом](https://www.php.net/manual/en/function.hash-algos.php):

```php
use Illuminate\Support\Str;

$hashed = Str::of('secret')->hash(algorithm: 'sha256');

// '2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b'
```

<a name="method-fluent-str-headline"></a>
#### `headline` {.collection-method}

Метод `headline` перетворює рядки, розділені регістром, дефісами чи підкресленнями, на рядок, розділений пробілами, де перша літера кожного слова велика:

```php
use Illuminate\Support\Str;

$headline = Str::of('taylor_otwell')->headline();

// Taylor Otwell

$headline = Str::of('EmailNotificationSent')->headline();

// Email Notification Sent
```

<a name="method-fluent-str-initials"></a>
#### `initials` {.collection-method}

Метод `initials` перетворює рядок на його ініціали:

```php
use Illuminate\Support\Str;

$initials = Str::of('Taylor Otwell')->initials()->upper();

// TO
```

<a name="method-fluent-str-inline-markdown"></a>
#### `inlineMarkdown` {.collection-method}

Метод `inlineMarkdown` перетворює Markdown у стилі GitHub на інлайновий HTML за допомогою [CommonMark](https://commonmark.thephpleague.com/). Проте, на відміну від методу `markdown`, він не обгортає весь згенерований HTML у блоковий елемент:

```php
use Illuminate\Support\Str;

$html = Str::of('**Laravel**')->inlineMarkdown();

// <strong>Laravel</strong>
```

#### Безпека Markdown

За замовчуванням Markdown підтримує сирий HTML, а це відкриває вразливість до міжсайтового скриптингу (XSS), якщо подавати туди сирий користувацький ввід. Як радить [документація з безпеки CommonMark](https://commonmark.thephpleague.com/security/), ви можете скористатися опцією `html_input`, щоб екранувати чи вирізати сирий HTML, і опцією `allow_unsafe_links`, щоб указати, чи дозволяти небезпечні посилання. Якщо вам потрібно дозволити частину сирого HTML, проженіть скомпільований Markdown через HTML Purifier:

```php
use Illuminate\Support\Str;

Str::of('Inject: <script>alert("Hello XSS!");</script>')->inlineMarkdown([
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// Inject: alert(&quot;Hello XSS!&quot;);
```

<a name="method-fluent-str-is"></a>
#### `is` {.collection-method}

Метод `is` визначає, чи відповідає заданий рядок заданому шаблону. Зірочки можна використовувати як символи підстановки

```php
use Illuminate\Support\Str;

$matches = Str::of('foobar')->is('foo*');

// true

$matches = Str::of('foobar')->is('baz*');

// false
```

<a name="method-fluent-str-is-ascii"></a>
#### `isAscii` {.collection-method}

Метод `isAscii` визначає, чи є заданий рядок рядком ASCII:

```php
use Illuminate\Support\Str;

$result = Str::of('Taylor')->isAscii();

// true

$result = Str::of('ü')->isAscii();

// false
```

<a name="method-fluent-str-is-empty"></a>
#### `isEmpty` {.collection-method}

Метод `isEmpty` визначає, чи є заданий рядок порожнім:

```php
use Illuminate\Support\Str;

$result = Str::of('  ')->trim()->isEmpty();

// true

$result = Str::of('Laravel')->trim()->isEmpty();

// false
```

<a name="method-fluent-str-is-not-empty"></a>
#### `isNotEmpty` {.collection-method}

Метод `isNotEmpty` визначає, чи не є заданий рядок порожнім:

```php
use Illuminate\Support\Str;

$result = Str::of('  ')->trim()->isNotEmpty();

// false

$result = Str::of('Laravel')->trim()->isNotEmpty();

// true
```

<a name="method-fluent-str-is-json"></a>
#### `isJson` {.collection-method}

Метод `isJson` визначає, чи є заданий рядок коректним JSON:

```php
use Illuminate\Support\Str;

$result = Str::of('[1,2,3]')->isJson();

// true

$result = Str::of('{"first": "John", "last": "Doe"}')->isJson();

// true

$result = Str::of('{first: "John", last: "Doe"}')->isJson();

// false
```

<a name="method-fluent-str-is-ulid"></a>
#### `isUlid` {.collection-method}

Метод `isUlid` визначає, чи є заданий рядок ULID:

```php
use Illuminate\Support\Str;

$result = Str::of('01gd6r360bp37zj17nxb55yv40')->isUlid();

// true

$result = Str::of('Taylor')->isUlid();

// false
```

<a name="method-fluent-str-is-url"></a>
#### `isUrl` {.collection-method}

Метод `isUrl` визначає, чи є заданий рядок URL:

```php
use Illuminate\Support\Str;

$result = Str::of('http://example.com')->isUrl();

// true

$result = Str::of('Taylor')->isUrl();

// false
```

Метод `isUrl` вважає коректними чимало протоколів. Втім, ви можете вказати, які протоколи вважати коректними, передавши їх методу `isUrl`:

```php
$result = Str::of('http://example.com')->isUrl(['http', 'https']);
```

<a name="method-fluent-str-is-uuid"></a>
#### `isUuid` {.collection-method}

Метод `isUuid` визначає, чи є заданий рядок UUID:

```php
use Illuminate\Support\Str;

$result = Str::of('5ace9ab9-e9cf-4ec6-a19d-5881212a452c')->isUuid();

// true

$result = Str::of('Taylor')->isUuid();

// false
```

Ви можете також перевірити, чи відповідає заданий UUID специфікації певної версії (1, 3, 4, 5, 6, 7 або 8):

```php
use Illuminate\Support\Str;

$isUuid = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->isUuid(version: 4);

// true

$isUuid = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->isUuid(version: 1);

// false
```

<a name="method-fluent-str-kebab"></a>
#### `kebab` {.collection-method}

Метод `kebab` перетворює заданий рядок на `kebab-case`:

```php
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->kebab();

// foo-bar
```

<a name="method-fluent-str-lcfirst"></a>
#### `lcfirst` {.collection-method}

Метод `lcfirst` повертає заданий рядок, у якому перший символ переведено в нижній регістр:

```php
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->lcfirst();

// foo Bar
```

<a name="method-fluent-str-length"></a>
#### `length` {.collection-method}

Метод `length` повертає довжину заданого рядка:

```php
use Illuminate\Support\Str;

$length = Str::of('Laravel')->length();

// 7
```

<a name="method-fluent-str-limit"></a>
#### `limit` {.collection-method}

Метод `limit` обрізає заданий рядок до вказаної довжини:

```php
use Illuminate\Support\Str;

$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20);

// The quick brown fox...
```

Другим аргументом можна змінити рядок, який буде дописано в кінці обрізаного рядка:

```php
$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20, ' (...)');

// The quick brown fox (...)
```

Якщо ви хочете зберегти цілі слова під час обрізання, скористайтеся аргументом `preserveWords`. Коли він `true`, рядок буде обрізано до найближчої межі цілого слова:

```php
$truncated = Str::of('The quick brown fox')->limit(12, preserveWords: true);

// The quick...
```

<a name="method-fluent-str-lower"></a>
#### `lower` {.collection-method}

Метод `lower` переводить заданий рядок у нижній регістр:

```php
use Illuminate\Support\Str;

$result = Str::of('LARAVEL')->lower();

// 'laravel'
```

<a name="method-fluent-str-markdown"></a>
#### `markdown` {.collection-method}

Метод `markdown` перетворює Markdown у стилі GitHub на HTML:

```php
use Illuminate\Support\Str;

$html = Str::of('# Laravel')->markdown();

// <h1>Laravel</h1>

$html = Str::of('# Taylor <b>Otwell</b>')->markdown([
    'html_input' => 'strip',
]);

// <h1>Taylor Otwell</h1>
```

#### Безпека Markdown

За замовчуванням Markdown підтримує сирий HTML, а це відкриває вразливість до міжсайтового скриптингу (XSS), якщо подавати туди сирий користувацький ввід. Як радить [документація з безпеки CommonMark](https://commonmark.thephpleague.com/security/), ви можете скористатися опцією `html_input`, щоб екранувати чи вирізати сирий HTML, і опцією `allow_unsafe_links`, щоб указати, чи дозволяти небезпечні посилання. Якщо вам потрібно дозволити частину сирого HTML, проженіть скомпільований Markdown через HTML Purifier:

```php
use Illuminate\Support\Str;

Str::of('Inject: <script>alert("Hello XSS!");</script>')->markdown([
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// <p>Inject: alert(&quot;Hello XSS!&quot;);</p>
```

<a name="method-fluent-str-mask"></a>
#### `mask` {.collection-method}

Метод `mask` маскує частину рядка повторюваним символом; ним можна приховувати фрагменти рядків - наприклад, адреси електронної пошти чи номери телефонів:

```php
use Illuminate\Support\Str;

$string = Str::of('taylor@example.com')->mask('*', 3);

// tay***************
```

За потреби третім або четвертим аргументом методу `mask` можна передати від'ємні числа - тоді маскування почнеться на заданій відстані від кінця рядка:

```php
$string = Str::of('taylor@example.com')->mask('*', -15, 3);

// tay***@example.com

$string = Str::of('taylor@example.com')->mask('*', 4, -4);

// tayl**********.com
```

<a name="method-fluent-str-match"></a>
#### `match` {.collection-method}

Метод `match` повертає частину рядка, що відповідає заданому шаблону регулярного виразу:

```php
use Illuminate\Support\Str;

$result = Str::of('foo bar')->match('/bar/');

// 'bar'

$result = Str::of('foo bar')->match('/foo (.*)/');

// 'bar'
```

<a name="method-fluent-str-match-all"></a>
#### `matchAll` {.collection-method}

Метод `matchAll` повертає колекцію з частинами рядка, що відповідають заданому шаблону регулярного виразу:

```php
use Illuminate\Support\Str;

$result = Str::of('bar foo bar')->matchAll('/bar/');

// collect(['bar', 'bar'])
```

Якщо ви вкажете у виразі групу захоплення, Laravel повернає колекцію збігів першої такої групи:

```php
use Illuminate\Support\Str;

$result = Str::of('bar fun bar fly')->matchAll('/f(\w*)/');

// collect(['un', 'ly']);
```

Якщо збігів не знайдено, буде повернуто порожню колекцію.

<a name="method-fluent-str-is-match"></a>
#### `isMatch` {.collection-method}

Метод `isMatch` повертає `true`, якщо рядок відповідає заданому регулярному виразу:

```php
use Illuminate\Support\Str;

$result = Str::of('foo bar')->isMatch('/foo (.*)/');

// true

$result = Str::of('laravel')->isMatch('/foo (.*)/');

// false
```

<a name="method-fluent-str-new-line"></a>
#### `newLine` {.collection-method}

Метод `newLine` дописує до рядка символ «кінець рядка»:

```php
use Illuminate\Support\Str;

$padded = Str::of('Laravel')->newLine()->append('Framework');

// 'Laravel
//  Framework'
```

<a name="method-fluent-str-padboth"></a>
#### `padBoth` {.collection-method}

Метод `padBoth` обгортає PHP-функцію `str_pad` і доповнює рядок з обох боків іншим рядком, доки той не досягне потрібної довжини:

```php
use Illuminate\Support\Str;

$padded = Str::of('James')->padBoth(10, '_');

// '__James___'

$padded = Str::of('James')->padBoth(10);

// '  James   '
```

<a name="method-fluent-str-padleft"></a>
#### `padLeft` {.collection-method}

Метод `padLeft` обгортає PHP-функцію `str_pad` і доповнює рядок зліва іншим рядком, доки той не досягне потрібної довжини:

```php
use Illuminate\Support\Str;

$padded = Str::of('James')->padLeft(10, '-=');

// '-=-=-James'

$padded = Str::of('James')->padLeft(10);

// '     James'
```

<a name="method-fluent-str-padright"></a>
#### `padRight` {.collection-method}

Метод `padRight` обгортає PHP-функцію `str_pad` і доповнює рядок справа іншим рядком, доки той не досягне потрібної довжини:

```php
use Illuminate\Support\Str;

$padded = Str::of('James')->padRight(10, '-');

// 'James-----'

$padded = Str::of('James')->padRight(10);

// 'James     '
```

<a name="method-fluent-str-pipe"></a>
#### `pipe` {.collection-method}

Метод `pipe` дозволяє перетворити рядок, передавши його поточне значення заданому виклику:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$hash = Str::of('Laravel')->pipe('md5')->prepend('Checksum: ');

// 'Checksum: a5c95b86291ea299fcbe64458ed12702'

$closure = Str::of('foo')->pipe(function (Stringable $str) {
    return 'bar';
});

// 'bar'
```

<a name="method-fluent-str-counted"></a>
#### `counted` {.collection-method}

Метод `counted` перетворює слово в однині на однину чи множину залежно від заданої кількості й додає перед результатом відформатовану кількість:

```php
use Illuminate\Support\Str;

$label = Str::of('order')->counted(1);

// 1 order

$label = Str::of('order')->counted(1000);

// 1,000 orders
```

<a name="method-fluent-str-plural"></a>
#### `plural` {.collection-method}

Метод `plural` перетворює слово в однині на форму множини. Ця функція підтримує [будь-яку з мов, які підтримує плюралізатор Laravel](/docs/{{version}}/localization#pluralization-language):

```php
use Illuminate\Support\Str;

$plural = Str::of('car')->plural();

// cars

$plural = Str::of('child')->plural();

// children
```

Функції можна передати аргумент - ціле число, щоб отримати форму однини або множини:

```php
use Illuminate\Support\Str;

$plural = Str::of('child')->plural(2);

// children

$plural = Str::of('child')->plural(1);

// child
```

Аргументом `prependCount` можна додати перед формою множини відформатоване значення `$count`:

```php
use Illuminate\Support\Str;

$label = Str::of('car')->plural(1000, prependCount: true);

// 1,000 cars
```

<a name="method-fluent-str-position"></a>
#### `position` {.collection-method}

Метод `position` повертає позицію першого входження підрядка в рядок. Якщо підрядка в рядку немає, повертається `false`:

```php
use Illuminate\Support\Str;

$position = Str::of('Hello, World!')->position('Hello');

// 0

$position = Str::of('Hello, World!')->position('W');

// 7
```

<a name="method-fluent-str-prepend"></a>
#### `prepend` {.collection-method}

Метод `prepend` додає задані значення на початок рядка:

```php
use Illuminate\Support\Str;

$string = Str::of('Framework')->prepend('Laravel ');

// Laravel Framework
```

<a name="method-fluent-str-remove"></a>
#### `remove` {.collection-method}

Метод `remove` видаляє з рядка задане значення або масив значень:

```php
use Illuminate\Support\Str;

$string = Str::of('Arkansas is quite beautiful!')->remove('quite ');

// Arkansas is beautiful!
```

Ви можете також передати другим параметром `false`, щоб метод не звертав уваги на регістр.

<a name="method-fluent-str-repeat"></a>
#### `repeat` {.collection-method}

Метод `repeat` повторює заданий рядок:

```php
use Illuminate\Support\Str;

$repeated = Str::of('a')->repeat(5);

// aaaaa
```

<a name="method-fluent-str-replace"></a>
#### `replace` {.collection-method}

Метод `replace` замінює в рядку заданий рядок:

```php
use Illuminate\Support\Str;

$replaced = Str::of('Laravel 6.x')->replace('6.x', '7.x');

// Laravel 7.x
```

Метод `replace` приймає також аргумент `caseSensitive`. За замовчуванням метод `replace` чутливий до регістру:

```php
$replaced = Str::of('macOS 13.x')->replace(
    'macOS', 'iOS', caseSensitive: false
);
```

<a name="method-fluent-str-replace-array"></a>
#### `replaceArray` {.collection-method}

Метод `replaceArray` послідовно замінює задане значення в рядку значеннями з масиву:

```php
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::of($string)->replaceArray('?', ['8:30', '9:00']);

// The event will take place between 8:30 and 9:00
```

<a name="method-fluent-str-replace-first"></a>
#### `replaceFirst` {.collection-method}

Метод `replaceFirst` замінює перше входження заданого значення в рядку:

```php
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceFirst('the', 'a');

// a quick brown fox jumps over the lazy dog
```

<a name="method-fluent-str-replace-last"></a>
#### `replaceLast` {.collection-method}

Метод `replaceLast` замінює останнє входження заданого значення в рядку:

```php
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceLast('the', 'a');

// the quick brown fox jumps over a lazy dog
```

<a name="method-fluent-str-replace-matches"></a>
#### `replaceMatches` {.collection-method}

Метод `replaceMatches` замінює всі частини рядка, що відповідають шаблону, заданим рядком заміни:

```php
use Illuminate\Support\Str;

$replaced = Str::of('(+1) 501-555-1000')->replaceMatches('/[^A-Za-z0-9]++/', '')

// '15015551000'
```

Метод `replaceMatches` приймає також замикання, яке буде викликано для кожної частини рядка, що відповідає заданому шаблону: у ньому ви виконуєте логіку заміни й повертаєте замінене значення:

```php
use Illuminate\Support\Str;

$replaced = Str::of('123')->replaceMatches('/\d/', function (array $matches) {
    return '['.$matches[0].']';
});

// '[1][2][3]'
```

<a name="method-fluent-str-replace-start"></a>
#### `replaceStart` {.collection-method}

Метод `replaceStart` замінює перше входження заданого значення лише тоді, коли воно стоїть на початку рядка:

```php
use Illuminate\Support\Str;

$replaced = Str::of('Hello World')->replaceStart('Hello', 'Laravel');

// Laravel World

$replaced = Str::of('Hello World')->replaceStart('World', 'Laravel');

// Hello World
```

<a name="method-fluent-str-replace-end"></a>
#### `replaceEnd` {.collection-method}

Метод `replaceEnd` замінює останнє входження заданого значення лише тоді, коли воно стоїть у кінці рядка:

```php
use Illuminate\Support\Str;

$replaced = Str::of('Hello World')->replaceEnd('World', 'Laravel');

// Hello Laravel

$replaced = Str::of('Hello World')->replaceEnd('Hello', 'Laravel');

// Hello World
```

<a name="method-fluent-str-scan"></a>
#### `scan` {.collection-method}

Метод `scan` розбирає вхідний рядок у колекцію за форматом, що його підтримує [PHP-функція `sscanf`](https://www.php.net/manual/en/function.sscanf.php):

```php
use Illuminate\Support\Str;

$collection = Str::of('filename.jpg')->scan('%[^.].%s');

// collect(['filename', 'jpg'])
```

<a name="method-fluent-str-singular"></a>
#### `singular` {.collection-method}

Метод `singular` перетворює рядок на форму однини. Ця функція підтримує [будь-яку з мов, які підтримує плюралізатор Laravel](/docs/{{version}}/localization#pluralization-language):

```php
use Illuminate\Support\Str;

$singular = Str::of('cars')->singular();

// car

$singular = Str::of('children')->singular();

// child
```

<a name="method-fluent-str-slug"></a>
#### `slug` {.collection-method}

Метод `slug` генерує із заданого рядка дружній до URL «slug»:

```php
use Illuminate\Support\Str;

$slug = Str::of('Laravel Framework')->slug('-');

// laravel-framework
```

<a name="method-fluent-str-snake"></a>
#### `snake` {.collection-method}

Метод `snake` перетворює заданий рядок на `snake_case`:

```php
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->snake();

// foo_bar
```

<a name="method-fluent-str-split"></a>
#### `split` {.collection-method}

Метод `split` розбиває рядок у колекцію за регулярним виразом:

```php
use Illuminate\Support\Str;

$segments = Str::of('one, two, three')->split('/[\s,]+/');

// collect(["one", "two", "three"])
```

<a name="method-fluent-str-squish"></a>
#### `squish` {.collection-method}

Метод `squish` прибирає з рядка всі надлишкові пробіли, зокрема й між словами:

```php
use Illuminate\Support\Str;

$string = Str::of('    laravel    framework    ')->squish();

// laravel framework
```

<a name="method-fluent-str-start"></a>
#### `start` {.collection-method}

Метод `start` додає до рядка одне входження заданого значення, якщо рядок ще не починається цим значенням:

```php
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->start('/');

// /this/string

$adjusted = Str::of('/this/string')->start('/');

// /this/string
```

<a name="method-fluent-str-starts-with"></a>
#### `startsWith` {.collection-method}

Метод `startsWith` визначає, чи починається заданий рядок заданим значенням:

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->startsWith('This');

// true
```

Ви можете також передати масив значень, щоб перевірити, чи починається рядок будь-яким зі значень масиву:

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->startsWith(['This', 'That']);

// true
```

<a name="method-fluent-str-strip-tags"></a>
#### `stripTags` {.collection-method}

Метод `stripTags` прибирає з рядка всі теги HTML і PHP:

```php
use Illuminate\Support\Str;

$result = Str::of('<a href="https://laravel.com">Taylor <b>Otwell</b></a>')->stripTags();

// Taylor Otwell

$result = Str::of('<a href="https://laravel.com">Taylor <b>Otwell</b></a>')->stripTags('<b>');

// Taylor <b>Otwell</b>
```

<a name="method-fluent-str-studly"></a>
#### `studly` {.collection-method}

Метод `studly` перетворює заданий рядок на `StudlyCase`:

```php
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->studly();

// FooBar
```

<a name="method-fluent-str-substr"></a>
#### `substr` {.collection-method}

Метод `substr` повертає частину рядка, задану параметрами початку та довжини:

```php
use Illuminate\Support\Str;

$string = Str::of('Laravel Framework')->substr(8);

// Framework

$string = Str::of('Laravel Framework')->substr(8, 5);

// Frame
```

<a name="method-fluent-str-substrreplace"></a>
#### `substrReplace` {.collection-method}

Метод `substrReplace` замінює текст у частині рядка, починаючи з позиції, заданої другим аргументом, і замінюючи стільку символів, скільки задано третім аргументом. Якщо передати третім аргументом `0`, рядок буде вставлено у вказану позицію, не замінюючи жодного наявного символу:

```php
use Illuminate\Support\Str;

$string = Str::of('1300')->substrReplace(':', 2);

// 13:

$string = Str::of('The Framework')->substrReplace(' Laravel', 3, 0);

// The Laravel Framework
```

<a name="method-fluent-str-swap"></a>
#### `swap` {.collection-method}

Метод `swap` замінює в рядку кілька значень за допомогою PHP-функції `strtr`:

```php
use Illuminate\Support\Str;

$string = Str::of('Tacos are great!')
    ->swap([
        'Tacos' => 'Burritos',
        'great' => 'fantastic',
    ]);

// Burritos are fantastic!
```

<a name="method-fluent-str-take"></a>
#### `take` {.collection-method}

Метод `take` повертає вказану кількість символів із початку рядка:

```php
use Illuminate\Support\Str;

$taken = Str::of('Build something amazing!')->take(5);

// Build
```

<a name="method-fluent-str-tap"></a>
#### `tap` {.collection-method}

Метод `tap` передає рядок заданому замиканню, щоб ви могли оглянути рядок і щось із ним зробити, не змінюючи самого рядка. Метод `tap` повертає початковий рядок незалежно від того, що повернуло замикання:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('Laravel')
    ->append(' Framework')
    ->tap(function (Stringable $string) {
        dump('String after append: '.$string);
    })
    ->upper();

// LARAVEL FRAMEWORK
```

<a name="method-fluent-str-test"></a>
#### `test` {.collection-method}

Метод `test` визначає, чи відповідає рядок заданому шаблону регулярного виразу:

```php
use Illuminate\Support\Str;

$result = Str::of('Laravel Framework')->test('/Laravel/');

// true
```

<a name="method-fluent-str-title"></a>
#### `title` {.collection-method}

Метод `title` перетворює заданий рядок на `Title Case`:

```php
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->title();

// A Nice Title Uses The Correct Case
```

<a name="method-fluent-str-to-base64"></a>
#### `toBase64` {.collection-method}

Метод `toBase64` перетворює заданий рядок на Base64:

```php
use Illuminate\Support\Str;

$base64 = Str::of('Laravel')->toBase64();

// TGFyYXZlbA==
```

<a name="method-fluent-str-to-html-string"></a>
#### `toHtmlString` {.collection-method}

Метод `toHtmlString` перетворює заданий рядок на екземпляр `Illuminate\Support\HtmlString`, який не буде екрановано під час рендеру в Blade-шаблонах:

```php
use Illuminate\Support\Str;

$htmlString = Str::of('Nuno Maduro')->toHtmlString();
```

<a name="method-fluent-str-to-uri"></a>
#### `toUri` {.collection-method}

Метод `toUri` перетворює заданий рядок на екземпляр [Illuminate\Support\Uri](/docs/{{version}}/helpers#uri):

```php
use Illuminate\Support\Str;

$uri = Str::of('https://example.com')->toUri();
```

<a name="method-fluent-str-transliterate"></a>
#### `transliterate` {.collection-method}

Метод `transliterate` спробує перетворити заданий рядок на найближче представлення в ASCII:

```php
use Illuminate\Support\Str;

$email = Str::of('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ')->transliterate()

// 'test@laravel.com'
```

<a name="method-fluent-str-trim"></a>
#### `trim` {.collection-method}

Метод `trim` обрізає заданий рядок. На відміну від нативної PHP-функції `trim`, метод `trim` у Laravel прибирає ще й пробільні символи Unicode:

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->trim();

// 'Laravel'

$string = Str::of('/Laravel/')->trim('/');

// 'Laravel'
```

<a name="method-fluent-str-ltrim"></a>
#### `ltrim` {.collection-method}

Метод `ltrim` обрізає рядок зліва. На відміну від нативної PHP-функції `ltrim`, метод `ltrim` у Laravel прибирає ще й пробільні символи Unicode:

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->ltrim();

// 'Laravel  '

$string = Str::of('/Laravel/')->ltrim('/');

// 'Laravel/'
```

<a name="method-fluent-str-rtrim"></a>
#### `rtrim` {.collection-method}

Метод `rtrim` обрізає заданий рядок справа. На відміну від нативної PHP-функції `rtrim`, метод `rtrim` у Laravel прибирає ще й пробільні символи Unicode:

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->rtrim();

// '  Laravel'

$string = Str::of('/Laravel/')->rtrim('/');

// '/Laravel'
```

<a name="method-fluent-str-ucfirst"></a>
#### `ucfirst` {.collection-method}

Метод `ucfirst` повертає заданий рядок, у якому перший символ переведено у верхній регістр:

```php
use Illuminate\Support\Str;

$string = Str::of('foo bar')->ucfirst();

// Foo bar
```

<a name="method-fluent-str-ucsplit"></a>
#### `ucsplit` {.collection-method}

Метод `ucsplit` розбиває заданий рядок у колекцію за великими літерами:

```php
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->ucsplit();

// collect(['Foo ', 'Bar'])
```

<a name="method-fluent-str-ucwords"></a>
#### `ucwords` {.collection-method}

Метод `ucwords` переводить перший символ кожного слова в заданому рядку у верхній регістр:

```php
use Illuminate\Support\Str;

$string = Str::of('laravel framework')->ucwords();

// Laravel Framework
```

<a name="method-fluent-str-unwrap"></a>
#### `unwrap` {.collection-method}

Метод `unwrap` прибирає вказані рядки з початку та кінця заданого рядка:

```php
use Illuminate\Support\Str;

Str::of('-Laravel-')->unwrap('-');

// Laravel

Str::of('{framework: "Laravel"}')->unwrap('{', '}');

// framework: "Laravel"
```

<a name="method-fluent-str-upper"></a>
#### `upper` {.collection-method}

Метод `upper` переводить заданий рядок у верхній регістр:

```php
use Illuminate\Support\Str;

$adjusted = Str::of('laravel')->upper();

// LARAVEL
```

<a name="method-fluent-str-when"></a>
#### `when` {.collection-method}

Метод `when` викликає задане замикання, якщо задана умова - `true`. Замикання отримає екземпляр плавного рядка:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('Taylor')
    ->when(true, function (Stringable $string) {
        return $string->append(' Otwell');
    });

// 'Taylor Otwell'
```

За потреби третім параметром методу `when` можна передати ще одне замикання. Воно виконається, якщо параметр умови дасть `false`.

<a name="method-fluent-str-when-contains"></a>
#### `whenContains` {.collection-method}

Метод `whenContains` викликає задане замикання, якщо рядок містить задане значення. Замикання отримає екземпляр плавного рядка:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('tony stark')
    ->whenContains('tony', function (Stringable $string) {
        return $string->title();
    });

// 'Tony Stark'
```

За потреби третім параметром можна передати ще одне замикання. Воно буде викликане, якщо рядок не містить заданого значення.

Ви можете також передати масив значень, щоб перевірити, чи містить рядок будь-яке зі значень масиву:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('tony stark')
    ->whenContains(['tony', 'hulk'], function (Stringable $string) {
        return $string->title();
    });

// Tony Stark
```

<a name="method-fluent-str-when-contains-all"></a>
#### `whenContainsAll` {.collection-method}

Метод `whenContainsAll` викликає задане замикання, якщо рядок містить усі задані підрядки. Замикання отримає екземпляр плавного рядка:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('tony stark')
    ->whenContainsAll(['tony', 'stark'], function (Stringable $string) {
        return $string->title();
    });

// 'Tony Stark'
```

За потреби третім параметром можна передати ще одне замикання. Воно буде викликане, якщо параметр умови дасть `false`.

<a name="method-fluent-str-when-doesnt-end-with"></a>
#### `whenDoesntEndWith` {.collection-method}

Метод `whenDoesntEndWith` викликає задане замикання, якщо рядок не закінчується заданим підрядком. Замикання отримає екземпляр плавного рядка:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('disney world')->whenDoesntEndWith('land', function (Stringable $string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-doesnt-start-with"></a>
#### `whenDoesntStartWith` {.collection-method}

Метод `whenDoesntStartWith` викликає задане замикання, якщо рядок не починається заданим підрядком. Замикання отримає екземпляр плавного рядка:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('disney world')->whenDoesntStartWith('sea', function (Stringable $string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-empty"></a>
#### `whenEmpty` {.collection-method}

Метод `whenEmpty` викликає задане замикання, якщо рядок порожній. Якщо замикання повертає значення, метод `whenEmpty` теж повернає це значення. Якщо замикання не повертає значення, буде повернуто екземпляр плавного рядка:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('  ')->trim()->whenEmpty(function (Stringable $string) {
    return $string->prepend('Laravel');
});

// 'Laravel'
```

<a name="method-fluent-str-when-not-empty"></a>
#### `whenNotEmpty` {.collection-method}

Метод `whenNotEmpty` викликає задане замикання, якщо рядок не порожній. Якщо замикання повертає значення, метод `whenNotEmpty` теж повернає це значення. Якщо замикання не повертає значення, буде повернуто екземпляр плавного рядка:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('Framework')->whenNotEmpty(function (Stringable $string) {
    return $string->prepend('Laravel ');
});

// 'Laravel Framework'
```

<a name="method-fluent-str-when-starts-with"></a>
#### `whenStartsWith` {.collection-method}

Метод `whenStartsWith` викликає задане замикання, якщо рядок починається заданим підрядком. Замикання отримає екземпляр плавного рядка:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('disney world')->whenStartsWith('disney', function (Stringable $string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-ends-with"></a>
#### `whenEndsWith` {.collection-method}

Метод `whenEndsWith` викликає задане замикання, якщо рядок закінчується заданим підрядком. Замикання отримає екземпляр плавного рядка:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('disney world')->whenEndsWith('world', function (Stringable $string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-exactly"></a>
#### `whenExactly` {.collection-method}

Метод `whenExactly` викликає задане замикання, якщо рядок точно збігається із заданим рядком. Замикання отримає екземпляр плавного рядка:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('laravel')->whenExactly('laravel', function (Stringable $string) {
    return $string->title();
});

// 'Laravel'
```

<a name="method-fluent-str-when-not-exactly"></a>
#### `whenNotExactly` {.collection-method}

Метод `whenNotExactly` викликає задане замикання, якщо рядок не збігається точно із заданим рядком. Замикання отримає екземпляр плавного рядка:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('framework')->whenNotExactly('laravel', function (Stringable $string) {
    return $string->title();
});

// 'Framework'
```

<a name="method-fluent-str-when-is"></a>
#### `whenIs` {.collection-method}

Метод `whenIs` викликає задане замикання, якщо рядок відповідає заданому шаблону. Зірочки можна використовувати як символи підстановки. Замикання отримає екземпляр плавного рядка:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('foo/bar')->whenIs('foo/*', function (Stringable $string) {
    return $string->append('/baz');
});

// 'foo/bar/baz'
```

<a name="method-fluent-str-when-is-ascii"></a>
#### `whenIsAscii` {.collection-method}

Метод `whenIsAscii` викликає задане замикання, якщо рядок є 7-бітним ASCII. Замикання отримає екземпляр плавного рядка:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('laravel')->whenIsAscii(function (Stringable $string) {
    return $string->title();
});

// 'Laravel'
```

<a name="method-fluent-str-when-is-ulid"></a>
#### `whenIsUlid` {.collection-method}

Метод `whenIsUlid` викликає задане замикання, якщо рядок є коректним ULID. Замикання отримає екземпляр плавного рядка:

```php
use Illuminate\Support\Str;

$string = Str::of('01gd6r360bp37zj17nxb55yv40')->whenIsUlid(function (Stringable $string) {
    return $string->substr(0, 8);
});

// '01gd6r36'
```

<a name="method-fluent-str-when-is-uuid"></a>
#### `whenIsUuid` {.collection-method}

Метод `whenIsUuid` викликає задане замикання, якщо рядок є коректним UUID. Замикання отримає екземпляр плавного рядка:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->whenIsUuid(function (Stringable $string) {
    return $string->substr(0, 8);
});

// 'a0a2a2d2'
```

<a name="method-fluent-str-when-test"></a>
#### `whenTest` {.collection-method}

Метод `whenTest` викликає задане замикання, якщо рядок відповідає заданому регулярному виразу. Замикання отримає екземпляр плавного рядка:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('laravel framework')->whenTest('/laravel/', function (Stringable $string) {
    return $string->title();
});

// 'Laravel Framework'
```

<a name="method-fluent-str-word-count"></a>
#### `wordCount` {.collection-method}

Метод `wordCount` повертає кількість слів у рядку:

```php
use Illuminate\Support\Str;

Str::of('Hello, world!')->wordCount(); // 2
```

<a name="method-fluent-str-words"></a>
#### `words` {.collection-method}

Метод `words` обмежує кількість слів у рядку. За потреби ви можете вказати додатковий рядок, який буде дописано до обрізаного рядка:

```php
use Illuminate\Support\Str;

$string = Str::of('Perfectly balanced, as all things should be.')->words(3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-fluent-str-wrap"></a>
#### `wrap` {.collection-method}

Метод `wrap` обгортає заданий рядок додатковим рядком або парою рядків:

```php
use Illuminate\Support\Str;

Str::of('Laravel')->wrap('"');

// "Laravel"

Str::is('is')->wrap(before: 'This ', after: ' Laravel!');

// This is Laravel!
```
