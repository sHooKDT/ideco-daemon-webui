"use strict";

try {
    var sock = new WebSocket("ws://" + window.location.host + "/ws");
} catch (err) {
    var sock = new WebSocket("wss://" + window.location.host + "/ws");
}

var handle_update = function (msg) {
    /*
        msg = {
            type: "status",
            active: true,
            enable_ui: true
        }
    */
    console.log(msg)
    try {
        var data = JSON.parse(msg.data);
        if (data.type === "status") {
            update_ui(data.active, data.enable_ui);
        }
    } catch (err) {
        console.log("bad message ", err)
    }
};

var send_action = function (act) {
    // start, stop, restart, disableui, enableui
    sock.send(JSON.stringify({
        type: "action",
        action: act
    }));
};

sock.onmessage = handle_update;
btn_start.onclick = a => send_action("start");
btn_restart.onclick = a => send_action("restart");
btn_stop.onclick = a => send_action("stop");
cb_enable_ui.onchange = a => send_action(checkbox_status());