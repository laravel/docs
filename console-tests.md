# 終端測試

- [介紹](#introduction)
- [成功 / 失敗期望值](#success-failure-expectations)
- [輸入 / 輸出期望值](#input-output-expectations)

<a name="introduction"></a>
## 介紹

此外簡化 HTTP 測試，Laravel　提供一個簡單的　API　來測試你的應用程式 [自定義終端指令](/docs/{{version}}/artisan)。

<a name="success-failure-expectations"></a>
## 成功 / 失敗期望值

首先，來探索如何對 Artisan 指令對出碼做斷言。為了完成這個，我們將使用 `artisan` 方法從我們的測試引動一個 Artisan　指令， 然後，我們將使用 `assertExitCode` 方法來斷言該指令以給定的退出碼完成 :

    /**
     * 測試一個終端指另。
     *
     * @return void
     */
    public function test_console_command()
    {
        $this->artisan('inspire')->assertExitCode(0);
    }

你可能使用 `assertNotExitCode` 方法來斷言該指令沒用給定的退出碼退出:

    $this->artisan('inspire')->assertNotExitCode(1);

當然，所有終端機指令通常退出跟著一個狀態碼 `0` 當他們是成功和非零當他們是失敗的。因此，為了方便，你可能採用  `assertSuccessful` 和 `assertFailed` 斷言來斷言一個給定指令退出是否有成退出碼:

    $this->artisan('inspire')->assertSuccessful();

    $this->artisan('inspire')->assertFailed();

<a name="成功 / 失敗期望值"></a>
## 成功 / 失敗期望值

Laravel 允許你簡單地 "mock" 使用者輸入給你的終端指令使用 `expectsQuestion` 方法。 此外，你可能指定退出碼和文本你期被終端指令使用 `assertExitCode` 和 `expectsOutput` 方法輸出。舉例，思考下列終端指令:

    Artisan::command('question', function () {
        $name = $this->ask('What is your name?');

        $language = $this->choice('Which language do you prefer?', [
            'PHP',
            'Ruby',
            'Python',
        ]);

        $this->line('Your name is '.$name.' and you prefer '.$language.'.');
    });

你可能測試這個指令利用下列 `expectsQuestion`， `expectsOutput`， `doesntExpectOutput`， 和  `assertExitCode` 方法來測試:

    /**
     * 測試一個終端指另。
     *
     * @return void
     */
    public function test_console_command()
    {
        $this->artisan('question')
             ->expectsQuestion('What is your name?', 'Taylor Otwell')
             ->expectsQuestion('Which language do you prefer?', 'PHP')
             ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.')
             ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.')
             ->assertExitCode(0);
    }

<a name="confirmation-expectations"></a>
#### 確認期望值

當寫一個期望確認 "yes" 或 "no" 形式答案的指令,你可能利用 `expectsConfirmation` 方法:

    $this->artisan('module:import')
        ->expectsConfirmation('Do you really wish to run this command?', 'no')
        ->assertExitCode(1);

<a name="table-expectations"></a>
#### 資料表期望值

如果你的指令陳列一個資運使用 Artisan's `table` 方法的資料表，他整個資料表的輸出期望值可能是繁瑣寫。取而代之，你可能使用 `expectsTable` 方法。這個方法接受資料表的標頭做為第一個引數和資料表的資料最為第二個引數:

    $this->artisan('users:all')
        ->expectsTable([
            'ID',
            'Email',
        ], [
            [1, 'taylor@example.com'],
            [2, 'abigail@example.com'],
        ]);
