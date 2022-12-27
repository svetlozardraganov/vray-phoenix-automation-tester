from sikuli import * 

screen_center = Location(Screen().getW()/2 , Screen().getH()/2)


#################################################-CHAOSGROUP-INSTALLER-COMMON-#################################################
cg_max_install_win = "cg_max_install_win.png"
cg_maya_install_win = "cg_maya_install_win.png"

cg_install_I_accept = "1671729673920.png"
cg_install_next = "cg_install_install_now.png"
cg_share_analitisc_data = "cg_share_analitisc_data.png"

cg_install_finish = "cg_install_finish.png"

#################################################-VRAY-4-MAYA-#################################################

vray_maya_install_win = "vray_maya_install_win.png"
vray_maya_install_checkbox = Pattern("vray_maya_install_checkbox.png").exact()
vray_maya_plugin_loaded = "vray_maya_plugin_loaded.png"
vray_maya_ipr_viewport = "vray_maya_ipr_viewport.png"
vray_vfb_stop = "vray_vfb_stop.png"
vray_vfb_stopped = "vray_vfb_stopped.png"

#################################################-VRAY-3DSMAX-3-#################################################

vray3_i_agree = "vray_I_agree.png"
vray3_install_now = "vray_install_now.png"
vray3_finish = Pattern("vray3_finish.png").similar(0.98)
vray3_checkbox = Pattern("vray3_checkbox.png").similar(0.97)


#################################################-PHOENIX-FD-3-3DSMAX-#################################################

phoenixFD_install_win = "phoenixFD_install_win.png"
phoenixFD_finish = "phoenixFD_finish.png"
phoenixFD_checkbox_enabled = Pattern("phoenixFD_checkbox_enabled.png").exact()
phoenix_beer = "phoenix_button_beer.png"
phoenix_fire = "phoenix_fire.png"
phoenix_start_sim = "phoenix_button_start_sim.png"
phoenix_stop_sim = "phoenix_stop_sim.png"

#################################################-3DSMAX-#################################################
max_viewport = "max_viewport.png"
max_listener_menu = "max_listener_menu.png"
max_command_panel = {'2019':"max_command_panel_2018.png",'2018':"max_command_panel_2018.png",'2017':"max_command_panel_2018.png",'2016':"max_command_panel_2016.png",'2015':"max_command_panel_2016.png",'2014':"max_command_panel_2016.png"}
max_top = "max_top.png"
max_anim_tools = {'2019':"max_anim_tools_2018.png",'2018':"max_anim_tools_2018.png",'2017':"max_anim_tools_2018.png",'2016':"max_anim_tools_2016.png",'2015':"max_anim_tools_2016.png",'2014':"max_anim_tools_2016.png"}
max_maximize_viewport = {'2019':"max_maximize_viewport_2018.png",'2018':"max_maximize_viewport_2018.png",'2017':"max_maximize_viewport_2018.png",'2016':"maximize_viewport_2016.png",'2015':"maximize_viewport_2016.png",'2014':"maximize_viewport_2016.png"}
max_domelight = "max_domelight.png"
max_standard_primitives ={'2019':Pattern("max_geometry_2018.png").targetOffset(2,30),'2018':Pattern("max_geometry_2018.png").targetOffset(2,14),'2017':Pattern("max_geometry_2018.png").targetOffset(2,14),'2016':Pattern("max_geometry_2016.png").targetOffset(7,31),'2015':Pattern("max_geometry_2016.png").targetOffset(5,17),'2014':Pattern("max_geometry_2016.png").targetOffset(5,17)}
max_box = Pattern("max_button_box.png").similar(0.80)
max_box_keyboard_entry_rollout = {'2019':"max_box_rollout_keyboard_entry.png",'2018':"max_box_rollout_keyboard_entry.png",'2017':"max_box_rollout_keyboard_entry.png",'2016':"max_box_rollout_keyboard_entry_2016.png",'2015':"max_box_rollout_keyboard_entry_2016.png",'2014':"max_box_rollout_keyboard_entry_2016.png"}
max_box_keyboard_entry = {'2019':Pattern("max_box_keyboard_entry.png").similar(0.71).targetOffset(-10,9),'2018':Pattern("max_box_keyboard_entry.png").similar(0.71).targetOffset(-10,9),'2017':Pattern("max_box_keyboard_entry.png").similar(0.71).targetOffset(-10,9),'2016':Pattern("max_box_keyboard_entry_2016.png").targetOffset(-6,9),'2015':Pattern("max_box_keyboard_entry_2016.png").targetOffset(-6,9),'2014':Pattern("max_box_keyboard_entry_2016.png").targetOffset(-6,9)}
max_box_create = Pattern("max_box_button_create.png").similar(0.85)
max_render_btn = {'2019':"max_render_btn_2018.png",'2018':"max_render_btn_2018.png",'2017':"max_render_btn_2018.png",'2016':"max_render_btn_2016.png",'2015':"max_render_btn_2016.png",'2014':"max_render_btn_2016.png"}
max_script_mini = "max_script_mini.png"
max_viewport_nav = "max_viewport_nav.png"
max_command_pannel = "max_command_pannel.png"
max_toolbar = "max_toolbar.png"
max_menu = "max_menu.png"

#################################################-MAYA-#################################################

maya_timeline = "maya_timeline.png"
maya_mel_script = "1542730504746.png"



