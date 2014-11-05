## Puppet Nginx Passenger Module

This is a fork of [puppet-nginx-passenger](https://github.com/jrabary/puppet-nginx-passenger) to install nginx with
passenger using default ruby version on debian wheezy or ubuntu precise.

After inclusion, this module ensures that any user in group `www-data` is able to deploy through tools such as capistrano or mina, this of course as long as you have right ssh configuration (keys or forwarding) in place.

This module installs Nginx using [puppet-rvm](https://github.com/maestrodev/puppet-rvm/). Please, read the documentation before you begin. This module has been tested on Ubuntu Precise (12.04). For custom types, do not forget to enable pluginsync:
```puppet
[main]
pluginsync = true

```

### Basic usage

Install nginx_passenger with

```puppet
include nginx_passenger
```

By default installs on _/opt/nginx_, there are some variables you might override

```puppet
class {'nginx_passenger':
    ruby_version      => 'ruby-1.9.3-p125',
    passenger_version => '4.0.23',
    installdir        => '/opt/nginx',
    logdir            => '/var/log/nginx',
    www               => '/var/www',
}
```

A custom installation might look like this:

```puppet
node webserver {
    class { 'nginx_passenger':
      installdir => '/usr/local/nginx',
      logdir     => '/usr/local/logs/nginx',
    }
}
```

An advanced installation using nginx source would look like the following. Take a look at the [pagespeed module](http://forge.puppetlabs.com/kbatra/nginx_pagespeed) for help with downloading the source.
```puppet
class { 'nginx_passenger':
    nginx_source_dir => '/home/vagrant/nginx-1.4.2',
    nginx_extra_configure_flags =>  '--add-module=/home/vagrant/ngx_pagespeed-release-1.6.29.5-beta'
}
```

### Virtual Hosts

You can easily configure a virtual host. An example is:

```puppet
nginx::vhost { 'www.example.com':
	port => '8080'
	rails => true,
}
```
The _rails_ attribute is optional and set to false by default. However, if you want to deploy a rails app, use this attribute and the rails template will be used instead.

### SSL

You can enable SSL for a virtual host like so:

```puppet
nginx_passenger::vhost { 'www.example.com': 
  ssl  => on,
  ssl_certificate  => '/etc/ssl/example.crt',
  ssl_certificate_key => '/etc/ssl/example.key',
  ssl_default_server => true    # optional, to set this as default SSL server
}
```

### MIT License

Copyright (C) 2012 by Sergio Galván

Copyright (C) 2013 by Karan Batra

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
