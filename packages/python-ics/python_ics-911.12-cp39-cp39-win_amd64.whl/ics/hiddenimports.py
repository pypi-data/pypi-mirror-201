hidden_imports = [
    "ics.structures.s_extended_data_flash_header",
    "ics.structures.tag_options_open_neo_ex",
    "ics.structures.tag_options_find_neo_ex",
    "ics.structures.tagicsneo_vi_command",
    "ics.structures.st_api_firmware_info",
    "ics.structures.can_settings",
    "ics.structures.canfd_settings",
    "ics.structures.swcan_settings",
    "ics.structures.lin_settings",
    "ics.structures.iso9141_keyword2000_init_step",
    "ics.structures.iso9141_keyword2000_settings",
    "ics.structures.uart_settings",
    "ics.structures.j1708_settings",
    "ics.structures.s_red_settings",
    "ics.structures.s_text_api_settings",
    "ics.structures.st_chip_versions",
    "ics.structures.s_neo_most_gateway_settings",
    "ics.structures.op_eth_general_settings",
    "ics.structures.srad_gptp_settings_s",
    "ics.structures.srad_gptp_and_tap_settings_s",
    "ics.structures.hw_eth_settings",
    "ics.structures.op_eth_settings",
    "ics.structures.ethernet_settings",
    "ics.structures.ethernet_settings2",
    "ics.structures.ethernet10_g_settings",
    "ics.structures.logger_settings",
    "ics.structures.disk_settings",
    "ics.structures.canterm_settings",
    "ics.structures.timesync_icshardware_settings",
    "ics.structures.s_disk_status",
    "ics.structures.s_disk_structure",
    "ics.structures.s_disk_details",
    "ics.structures.s_disk_format_progress",
    "ics.structures.start_dhcp_server_command",
    "ics.structures.stop_dhcp_server_command",
    "ics.structures.extended_response_generic",
    "ics.structures.generic_api_selector",
    "ics.structures.generic_api_status",
    "ics.structures.generic_api_data",
    "ics.structures.w_bms_manager_set_lock",
    "ics.structures.w_bms_manager_reset",
    "ics.structures.uart_port_data",
    "ics.structures.uart_port_port_bytes",
    "ics.structures.uart_port_config",
    "ics.structures.get_supported_features_response",
    "ics.structures.version_report",
    "ics.structures.get_component_versions",
    "ics.structures.get_component_versions_response",
    "ics.structures.software_update_command",
    "ics.structures.s_ext_sub_cmd_hdr",
    "ics.structures.timestamp_",
    "ics.structures.port_identity",
    "ics.structures.clock_quality_",
    "ics.structures.system_identity",
    "ics.structures.priority_vector",
    "ics.structures.gptp_status",
    "ics.structures.s_ext_sub_cmd_comm",
    "ics.structures.serdescam_settings",
    "ics.structures.serdespoc_settings",
    "ics.structures.serdesgen_settings",
    "ics.structures.rad_moon_duo_converter_settings",
    "ics.structures.rad_reporting_settings",
    "ics.structures.s_fire_settings",
    "ics.structures.s_fire_vnet_settings",
    "ics.structures.s_cyan_settings",
    "ics.structures.svcan3_settings",
    "ics.structures.svcan4_settings",
    "ics.structures.svcanrf_settings",
    "ics.structures.secu_settings",
    "ics.structures.s_pendant_settings",
    "ics.structures.sievb_settings",
    "ics.structures.seevb_settings",
    "ics.structures.srad_galaxy_settings",
    "ics.structures.srad_star2_settings",
    "ics.structures.srad_super_moon_settings",
    "ics.structures.a2_b_monitor_settings",
    "ics.structures.srada2_b_settings",
    "ics.structures.srad_moon2_settings",
    "ics.structures.srad_moon3_settings",
    "ics.structures.srad_gigalog_settings",
    "ics.structures.srad_gigastar_settings",
    "ics.structures.s_vivid_can_settings",
    "ics.structures.sobd2_sim_settings",
    "ics.structures.s_cm_probe_settings",
    "ics.structures.sobd2_pro_settings",
    "ics.structures.svcan412_settings",
    "ics.structures.secu_avb_settings",
    "ics.structures.s_pluto_l2_address_lookup_entry_s",
    "ics.structures.s_pluto_l2_address_lookup_params_s",
    "ics.structures.s_pluto_l2_forwarding_params_s",
    "ics.structures.s_pluto_l2_forwarding_entry_s",
    "ics.structures.s_pluto_l2_policing_s",
    "ics.structures.s_pluto_vlan_lookup_s",
    "ics.structures.s_pluto_mac_config_s",
    "ics.structures.s_pluto_retagging_entry_s",
    "ics.structures.s_pluto_general_params_s",
    "ics.structures.s_pluto_vl_lookup_entry_s",
    "ics.structures.s_pluto_vl_policing_entry_s",
    "ics.structures.s_pluto_vl_forwarding_params_s",
    "ics.structures.s_pluto_vl_forwarding_entry_s",
    "ics.structures.s_pluto_avb_params_s",
    "ics.structures.s_pluto_clock_sync_params_s",
    "ics.structures.s_pluto_ptp_params_s",
    "ics.structures.s_pluto_custom_params_s",
    "ics.structures.s_pluto_switch_settings_s",
    "ics.structures.srad_pluto_settings",
    "ics.structures.scan_sleep_id",
    "ics.structures.scan_hub_settings",
    "ics.structures.s_flex_vnetz_settings",
    "ics.structures.s_neo_ecu12_settings",
    "ics.structures.svcan4_ind_settings",
    "ics.structures.sobd2_lc_settings",
    "ics.structures.s_jupiter_ptp_params_s",
    "ics.structures.srad_jupiter_switch_settings",
    "ics.structures.srad_jupiter_settings",
    "ics.structures.fire3_linux_settings",
    "ics.structures.s_fire3_settings",
    "ics.structures.s_rad_moon_duo_settings",
    "ics.structures.s_ether_badge_settings",
    "ics.structures.srad_epsilon_switch_settings",
    "ics.structures.srad_epsilon_settings",
    "ics.structures.s_wil_fault_servicing_settings",
    "ics.structures.s_wil_network_data_capture_settings",
    "ics.structures.s_wil_connection_settings",
    "ics.structures.s_spi_port_settings",
    "ics.structures.s_wil_bridge_config",
    "ics.structures.sradbms_settings",
    "ics.structures.global_settings",
    "ics.structures.s_device_settings",
    "ics.structures.st_cm_iso157652_tx_message",
    "ics.structures.iso15765_2015_tx_message",
    "ics.structures.st_cm_iso157652_rx_message",
    "ics.structures.spy_filter_long",
    "ics.structures.ics_spy_message_flex_ray",
    "ics.structures.ics_spy_message_long",
    "ics.structures.ics_spy_message_vsb",
    "ics.structures.ethernet_network_status_t",
    "ics.structures.ics_fire2_device_status",
    "ics.structures.ics_fire2_vnet_device_status",
    "ics.structures.ics_vcan4_device_status",
    "ics.structures.ics_flex_vnetz_device_status",
    "ics.structures.ics_fire3_device_status",
    "ics.structures.ics_rad_moon_duo_device_status",
    "ics.structures.ics_rad_jupiter_device_status",
    "ics.structures.ics_obd2_pro_device_status",
    "ics.structures.ics_rad_pluto_device_status",
    "ics.structures.ics_vcan4_industrial_device_status",
    "ics.structures.ics_rad_epsilon_device_status",
    "ics.structures.ics_rad_bms_device_status",
    "ics.structures.ics_device_status",
    "ics.structures.s_phy_reg_pkt_hdr",
    "ics.structures.s_phy_reg_pkt_clause22_mess",
    "ics.structures.s_phy_reg_pkt_clause45_mess",
    "ics.structures.s_phy_reg_pkt",
    "ics.structures.op_eth_link_mode",
    "ics.structures.e_disk_format",
    "ics.structures.e_disk_layout",
    "ics.structures.extended_response_code",
    "ics.structures.e_gptp_port",
    "ics.structures.e_gptp_role",
    "ics.structures.a2_btdm_mode",
    "ics.structures.a2_b_node_type",
    "ics.structures.flex_vnet_mode",
    "ics.structures.e_device_settings_type",
    "ics.structures.e_plasma_ion_vnet_channel_t",
    "ics.structures.ew_bms_manager_port_t",
    "ics.structures.ew_bms_manager_lock_state_t",
    "ics.structures.e_uart_port_t",
    "ics.structures.e_generic_api_options",
    "ics.structures.ew_bms_instance_t",
    "ics.structures.s_phy_reg_pkt_status",
    "ics.structures.s_phy_reg_pkt_rw",
    "ics.structures.device_feature",
]

