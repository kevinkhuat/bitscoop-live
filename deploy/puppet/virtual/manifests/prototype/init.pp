class { 'python' :
  version    => latest,
  pip        => true,
  dev        => true,
  virtualenv => true,
}

python::virtualenv { '~/enviroments/ografy-3.4' :
  ensure       => present,
  version      => latest,
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

exec { "dependencies.sh":
  command => "sh ~/dependences.sh",
  creates => "~/sites"
}
