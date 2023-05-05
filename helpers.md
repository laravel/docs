<a name="sleep"></a>
### Sleep

Laravel's `Sleep` class is a lightweight wrapper around PHP's native `sleep` and `usleep` functions. It brings testibility to these methods while also exposing a nicer API for working with time.

    use Illuminate\Support\Sleep;

    $waiting = true;

    while ($waiting) {
        Sleep::for(1)->second();

        $waiting = /* ... */;
    }

The class exposes a handful of methods that allow you to work with different units of time.

    // Pause exection for 90 seconds...
    Sleep::for(1.5)->minutes();

    // Pause exection for 2 seconds...
    Sleep::for(2)->seconds();

    // Pause exection for 500 milliseconds...
    Sleep::for(500)->milliseconds();

    // Pause exection for 5,000 microseconds...
    Sleep::for(5000)->microseconds();

    // Pause exection until a given time...
    Sleep::until(now()->addMinute());

    // Alias of PHP's native "sleep" function...
    Sleep::sleep(2);

    // Alias of PHP's native "usleep" function...
    Sleep::usleep(5000);

To make it easier to combine units of time, you may also chain calls to add additional time.

    Sleep::for(1)->second()->and(10)->milliseconds();

<a name="testing-sleep"></a>
#### Testing Sleep

When testing code that utilises the `Sleep` class, your test will also pause execution. Imagine you are testing the following code path:

    $waiting = /* ... */;
    $seconds = 1;

    while ($waiting) {
        Sleep::for($seconds++)->seconds();

        $waiting = /* ... */;
    }

Any test that executes the `while` loop seen above would take _at least_ one second, due to the execution pause. Luckily, the `Sleep` class allows us to "fake" the execution pause in our tests.

    public function testItWaitsUntilReady()
    {
        Sleep::fake();

        // ...
    }

Now when we run our test, the actual execution pause is by-passed leading to a substantially faster test.

It is also possible to make assertions against the expected execution pauses that should have occurred. Imagine we are testing that the code will pause execution 3 times, with each pause increasing by a single second.

    public function testItChecksIfReadyFourTimes()
    {
        Sleep::fake();

        // ...

        Sleep::assertSequence([
            Sleep::for(1)->second(),
            Sleep::for(2)->seconds(),
            Sleep::for(3)->seconds(),
        ]);
    }

There some additional assertions that may come in handy:

    use Carbon\CarbonInterval as Duration;
    use Illuminate\Support\Sleep;

    // Assert against the duration of the execution pause...
    Sleep::assertSlept(function (Duration $duration): bool {
        return /* ... */;
    }, times: 1);

    // Assert that Sleep was called 3 times...
    Sleep::assertSleptTimes(3);

    // Assert that Sleep was never called.
    Sleep::assertNeverSlept();

    // Assert that, even if Sleep was called, no sleeping occurred.
    // Useful if you are computing sleep durations that may be negative...
    Sleep::assertInsomniac();
