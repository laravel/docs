# 主控台測試

- [前言](#前言)
- [期望輸入/輸出](#%e6%9c%9f%e6%9c%9b%e8%bc%b8%e5%85%a5%2f%e8%bc%b8%e5%87%ba)

## 前言

除了簡化HTTP測試之外，Laravel還提供了一個簡單的API，用於測試使用者請求輸入主控台應用。

<span id="期望輸入/輸出"></span>

## 期望輸入/輸出

Laravel允許您使用 `expectsQuestion` 方法輕鬆地 "模擬" 使用者輸入控制台命令。 此外，您可以使用 `assertExitCode` 及 `expectsOutput` 方法指定主控台命令希望輸出的退出指令和文字。 請參考以下的主控台命令範例：

    Artisan::command('question', function () {
        $name = $this->ask('What is your name?');

        $language = $this->choice('Which language do you program in?', [
            'PHP',
            'Ruby',
            'Python',
        ]);

        $this->line('Your name is '.$name.' and you program in '.$language.'.');
    });

您可以利用 `expectsQuestion`、`expectsOutput` 及 `assertExitCode` 的測試方法來測試命令：

    /**
     * Test a console command.
     *
     * @return void
     */
    public function testConsoleCommand()
    {
        $this->artisan('question')
             ->expectsQuestion('What is your name?', 'Taylor Otwell')
             ->expectsQuestion('Which language do you program in?', 'PHP')
             ->expectsOutput('Your name is Taylor Otwell and you program in PHP.')
             ->assertExitCode(0);
    }


