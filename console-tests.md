# Console Tests

- [Introduction](#introduction)
- [Expecting Input / Output](#expecting-input-and-output)

<a name="introduction"></a>
## Introduction

In addition to simplifying HTTP testing, Laravel provides a simple API for testing console applications that ask for user input.

<a name="expecting-input-and-output"></a>
## Expecting Input / Output

Laravel allows you to easily "mock" user input for your console commands using the `expectsQuestion` method. In addition, you may specify the exit code and text that you expect to be output by the console command using the `assertExitCode` and `expectsOutput` methods. For example, consider the following console command:

    Artisan::command('question', function () {
        $name = $this->ask('What is your name?');

        $language = $this->choice('Which language do you program in?', [
            'PHP',
            'Ruby',
            'Python',
        ]);

        $this->line('Your name is '.$name.' and you program in '.$language.'.');
    });

You may test this command with the following test which utilizes the `expectsQuestion`, `expectsOutput`, and `assertExitCode` methods:

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

When writing a command which expects a confirmation in the form of a "yes" or "no" answer, you may utilize the `expectsConfirmation` method:

    $this->artisan('module:import')
        ->expectsConfirmation('Do you really wish to run this command?', 'no')
        ->assertExitCode(1);
