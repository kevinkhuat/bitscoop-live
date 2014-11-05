# Class: nginx_passenger
#
# This module installs Nginx and its default configuration using rvm as the provider.
#
# Parameters:
#   $ruby_version
#       Ruby version to install.
#   $passenger_version
#      Passenger version to install.
#   $logdir
#      Nginx's log directory.
#   $installdir
#      Nginx's install directory.
#   $www
#      Base directory for
# Actions:
#
# Requires:
#    puppet-rvm
#
# Sample Usage:  include nginx_passenger
class nginx_passenger (
  $ruby_version = 'ruby-2.0.0-p247',
  $passenger_version = '4.0.23',
  $logdir = '/var/log/nginx',
  $installdir = '/opt/nginx',
  $www    = '/var/www',
  $nginx_source_dir = '',
  $nginx_extra_configure_flags = '',
  $app_environment = 'production') inherits nginx_passenger::params {

    $base_options = "--auto --prefix=${installdir}"

    if $nginx_source_dir {
      if $nginx_extra_configure_flags {
        # Double escape with help of slashes outside the escaped quote since options
        # get passed down to another set of escaped quotes
        # and then to the shell
        $options = "${base_options} --nginx-source-dir ${nginx_source_dir} --extra-configure-flags \\\"${nginx_extra_configure_flags}\\\""
      }
      else {
        $options = "${base_options} --nginx-source-dir ${nginx_source_dir}"
      }
    }
    else {
      $options = "${base_options} --auto-download"  
    }

    $passenger_deps = [ 'libcurl4-openssl-dev' ]

    include rvm

    package { $passenger_deps: ensure => present }

    rvm_system_ruby {
      $ruby_version:
        ensure      => 'present',
        default_use => true;
    }

    rvm_gem {
      "${ruby_version}/passenger":
        ensure => $passenger_version,
  		require => Rvm_system_ruby["${ruby_version}"],
  		ruby_version => $ruby_version;
    }

    exec { 'create container':
      command => "/bin/mkdir ${www} && /bin/chown www-data:www-data ${www} && /bin/chmod g+rws ${www}",
      unless  => "/usr/bin/test -d ${www}",
      before  => Exec['nginx-install']
    }

    exec { 'nginx-install':
      command => "/bin/bash -l -i -c \"/usr/local/rvm/gems/${ruby_version}/bin/passenger-install-nginx-module ${options}\"",
      group   => 'root',
      unless  => "/usr/bin/test -d ${installdir}",
      require => [ Package[$passenger_deps], Rvm_system_ruby[$ruby_version], Rvm_gem["${ruby_version}/passenger"]],
  	  environment => "HOME=/home/vagrant/",
    }

    file { 'nginx-config':
      path    => "${installdir}/conf/nginx.conf",
      owner   => 'root',
      group   => 'root',
      mode    => '0644',
      content => template('nginx_passenger/nginx.conf.erb'),
      require => Exec['nginx-install'],
    }

    file { 'proxy-config':
      path    => "${installdir}/conf/proxy.conf",
      owner   => 'root',
      group   => 'root',
      mode    => '0644',
      content => template('nginx_passenger/proxy.conf.erb'),
      require => Exec['nginx-install'],
    }

    file { $nx_run_dir:
      ensure => directory,
    } 

    exec { 'create sites-conf':
      path    => ['/usr/bin','/bin'],
      unless  => "/usr/bin/test -d  ${installdir}/conf/sites-available && /usr/bin/test -d ${installdir}/conf/sites-enabled",
      command => "/bin/mkdir  ${installdir}/conf/sites-available && /bin/mkdir ${installdir}/conf/sites-enabled",
      require => Exec['nginx-install'],
    }

    file { 'nginx-service':
      path      => '/etc/init.d/nginx',
      owner     => 'root',
      group     => 'root',
      mode      => '0755',
      content   => template('nginx_passenger/nginx.init.erb'),
      require   => [File['nginx-config'], File['proxy-config']],
      subscribe => [File['nginx-config'], File['proxy-config']],
    }

    file { $logdir:
      ensure => directory,
      owner  => 'root',
      group  => 'root',
      mode   => '0644'
    }

    service { 'nginx':
      ensure     => running,
      enable     => true,
      hasrestart => true,
      hasstatus  => true,
      subscribe  => [File['nginx-config'], File['proxy-config']],
      require    => [ File[$logdir], File['nginx-service']],
    }

}
