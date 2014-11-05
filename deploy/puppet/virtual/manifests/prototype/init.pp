class { 'python' :
  version    => latest,
  pip        => true,
  dev        => true,
  virtualenv => true,
}

python::virtualenv { '/var/www/project1' :
  ensure       => present,
  version      => 'system',
  requirements => '/var/www/project1/requirements.txt',
  proxy        => 'http://proxy.domain.com:3128',
  systempkgs   => true,
  distribute   => false,
  venv_dir     => '/home/appuser/virtualenvs',
  owner        => 'appuser',
  group        => 'apps',
  cwd          => '/var/www/project1',
  timeout      => 0,
}

class ografy_dep_script {
    exec { "easy_install pip":
        path => "/usr/local/bin:/usr/bin:/bin",
        refreshonly => true,
        require => Package["python"],
    }
}

python::requirements { '/var/www/project1/requirements.txt' :
  virtualenv => '/var/www/project1',
  proxy      => 'http://proxy.domain.com:3128',
  owner      => 'appuser',
  group      => 'apps',
}

