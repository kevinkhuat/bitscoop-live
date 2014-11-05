# Define: nginx_passenger::vhost
#
# Creates nginx virtual hosts
#
# Parameters:
#   $host
#       The title of the resource  is used as the host.
#   $port
#       Virtual host port
#   $root
#       Virtual host path
#   $create_root
#       True or false, allows to create the path for the virtual host
#   $rails
#       True or false, sets if the application is rails based or not.
# Actions:
#       Creates a virtual host
#
# Requires:
#       nginx
#
# Sample Usage:
#
#  nginx_passenger::vhost { 'test':
#    sever_name =>  'blog.test.com'
# }
define nginx_passenger::vhost(
  $host = $name,
  $server_name = $name,
  $port = '80',
  $root    = "/var/www/${host}",
  $makeroot = true,
  $rails = false,
  $proxy = false,
  $proxy_ssl = false,
  $ssl = off,
  $ssl_certificate = '',
  $ssl_certificate_key = '',
  $ssl_port = '443',
  $ssl_default_server = false
){
  include nginx_passenger

  if $makeroot{
    file { $root:
      ensure  => directory,
      owner   => 'www-data',
      group   => 'www-data',
      mode    => '0755',
    }
  }

  $template =  $rails ? {
    true    => 'vhost.rails.erb',
    default => 'vhost.erb',
  }

  file { $host:
    ensure  => present,
    path    => "${nginx_passenger::installdir}/conf/sites-available/${host}",
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => template("nginx_passenger/${template}"),
  }

  file { "${nginx_passenger::installdir}/conf/sites-enabled/${host}":
    ensure  => link,
    target  => "${nginx_passenger::installdir}/conf/sites-available/${host}",
    require => File[$host],
  }

  exec { "nginx ${host}":
    command => '/etc/init.d/nginx restart',
    require => File["${nginx_passenger::installdir}/conf/sites-enabled/${host}"],
    refreshonly => true,
    subscribe => File["${nginx_passenger::installdir}/conf/sites-enabled/${host}"],
  }
}

Class['nginx_passenger']->Type['nginx_passenger::vhost']
