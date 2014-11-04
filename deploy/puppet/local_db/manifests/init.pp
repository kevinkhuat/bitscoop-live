class { 'postgresql::server':
  listen_addresses          => '*',
  ip_mask_allow_all_users   => '0.0.0.0/0',
  ipv4acls                  => ['host all all 0.0.0.0/0 password'],
  postgres_password         => 'foxtrot1234!',
}

postgresql::server::db { 'ografy_db':
  user                      => 'ografy_db_user',
  password                  => postgresql_password('ografy_db_user', 'foxtrot1234'),
}
