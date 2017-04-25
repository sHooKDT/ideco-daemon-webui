"use strict";

var status_bar = document.getElementById("status-bar");
var status_bar_text = document.getElementById("status-bar-text");
var btn_start = document.getElementById("btn-start");
var btn_restart = document.getElementById("btn-restart");
var btn_stop = document.getElementById("btn-stop");
var cb_enable_ui = document.getElementById("cb-enable-ui");

var set_status_text = function (newtext) {
    status_bar_text.textContent = newtext;
}

var update_ui = function (service_active, control_enabled) {
    cb_enable_ui.checked = control_enabled;
    
    if (service_active) {
        status_bar.classList.remove("inactive");
        set_status_text("Сервис работает");
        btn_start.setAttribute("disabled", "disabled");
        btn_restart.removeAttribute("disabled");
        btn_stop.removeAttribute("disabled");
    } else {
        status_bar.classList.add("inactive");
        set_status_text("Сервис остановлен");
        btn_start.removeAttribute("disabled");
        btn_restart.setAttribute("disabled", "disabled");
        btn_stop.setAttribute("disabled", "disabled");
    }
    
    if (!control_enabled) {
        btn_start.setAttribute("disabled", "disabled");
        btn_restart.setAttribute("disabled", "disabled");
        btn_stop.setAttribute("disabled", "disabled");
    }
};

var checkbox_status = function() {
    if (cb_enable_ui.checked) 
        return "enableui";
    else return "disableui";
}