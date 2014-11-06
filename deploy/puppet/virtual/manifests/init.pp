user { "ografy":
  ensure     => "present",
  managehome => true,
  before     => "copy_dependencies_sh_file",
}

exec { "copy_dependencies_sh_file":
  command    => "/usr/bin/scp williambroza@192.168.1.2:/users/williambroza/DEV/Repos/ografy/deploy/scripts/dependances ~/",
  before     => "dependencies.sh",
}

file { 'dependencies.sh':
  path       => '~/dependencies.sh',
  ensure     => present,
  mode       => a+x,
  before     => "sh dependencies.sh",
}

exec { 'sh dependencies.sh':
  user       => 'ografy',
}
