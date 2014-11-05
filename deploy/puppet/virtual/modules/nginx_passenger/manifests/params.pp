class nginx_passenger::params {
  $nx_run_dir = '/var/nginx'
  $proxy_redirect = off
  $proxy_set_header = [
    'Host $host',
    'X-Real-IP $remote_addr',
    'X-Forwarded-For $proxy_add_x_forwarded_for',
  ]
  $proxy_cache_path = false
  $proxy_cache_levels = 1
  $proxy_cache_keys_zone = 'd2:100m'
  $proxy_cache_max_size = '500m'
  $proxy_cache_inactive = '20m'

  $client_body_temp_path = "${nx_run_dir}/client_body_temp"
  $client_body_buffer_size = '128k'
  $client_max_body_size = '10m'
  $proxy_temp_path = "${nx_run_dir}/proxy_temp"
  $proxy_connect_timeout = '90'
  $proxy_send_timeout = '90'
  $proxy_read_timeout = '90'
  $proxy_buffers = '32 4k'
  $proxy_http_version = '1.0'
  $proxy_buffer_size = '8k'
}