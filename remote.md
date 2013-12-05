# The Remote Component

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Usage](#usage)
- [Tasks](#tasks)
- [Files](#files)
- [Use Cases](#use-cases)

<a name="introduction"></a>
## Introduction

The Remote Component makes it easy to manage the various installs of your application on remote servers. Furthermore, it can execute terminal commands on any remote server, whether or not it has a Laravel application installed. As reviewed in the [Use Cases](#use-cases) section, it can also contribute to your deployment workflow when combined with [Artisan Commands](/docs/commands).

<a name="configuration"></a>
## Configuration

You may configure multiple remote connections in `/app/config/remote.php`, as well as the default connection to be used when accessing the `SSH` facade. You can also group your connections for quick and easy access to multiple connections in one single execution.

<a name="usage"></a>
## Usage

After configuring your remote connections, you can connect to the server by using the `SSH` facade:

    $client = SSH::into('production'); // where 'production' is the connection name
    
Once you have haccess to the connection, you can execute a command by using the `run()` method:

    $client->run('cd /var/www');
    
You can also execute multiple commands by passing an array to the `run()` method:

    $client->run(array(
      'cd /var/www',
      'php artisan cache:clear',
      'php artisan migrate'
    ));
    
To access the output of the executed commands, you can pass a callback closure as the second parameter of the `run()` method:

    $client->run('which php', function($line)
    {
      Log::info($line);
    });
      
Lastly, you can string the `SSH` facade along with the `run()` method to make your code more readable:

    SSH::into('production')
      ->run(array(
        'cd /var/www',
        'ls -la',
        'php artisan cache:clear'
      ), function($line)
      {
        Log::info($line);
      });
      
<a name="tasks"></a>
## Tasks

You can easily group a set of commands into a task for future reference and easy access. To define a task on a connection, use the `SSH` facade and the `define()` method:

    SSH::into('production')->define('composer:install', array(
      'cd /var/www',
      'php composer.phar install --no-dev'
    ));
    
To execute a particular task, use the `task()` method.

    SSH::into('production')->task('composer:install', function($line)
    {
      Log::info($line);
    });
    
<a name="files"></a>
## Files

The `SSH` facade can also be used to put local files (or strings) on the remote server.

    SSH::into('production')->put($local, $remote);
    
    SSH::into('production')->putString($remote, $contents);


<a name="use-cases"></a>
## Use Cases

When combining the Remote Component with [Artisan Commands](/docs/commands), the Remote Component can be used to establish a healthy deployment workflow. For example, we could define a deploy command that has the following `fire()` method.

    public function fire()
    {
      $me = $this;
      $remote = $this->argument('remote');
      
      SSH::into($remote)->run(array(
        'cd /var/www',
        'git checkout',
        'git pull',
        'php artisan cache:clear',
        'php artisan migrate',
        'php composer.phar install --no-dev'
      ), function($line) use ($me)
      {
        $me->info($line);
      });
      
      $this->info('All done!');
    }
    
> Please note that this is simply a suggested workflow, and should not be used in production as is.
