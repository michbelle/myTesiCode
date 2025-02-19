path_rmf_zenoh=~/zenoh_client_rmf
cd $path_rmf_zenoh

path_config_zenoh=~/zenoh_client_rmf/config
file_config_zenoh=bridge_mini_client.json5
./zenoh-bridge-ros2dds -c $path_config_zenoh/$file_config_zenoh
