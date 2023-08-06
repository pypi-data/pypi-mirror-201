let original_modal_content = document.getElementById("create-modal-body").innerHTML;
let edit_listener_id = null;

function deleteListener(id) {
    fetch("/listeners/" + id + "/remove?json=true", {
        method: "DELETE"
    }).then(response => response.json())
        .then(data => {
            // show notification
            showNotification(data.message, data.status);
            // check if success
            if (data.status === "success") {
                // sleep 1 second
                setTimeout(function () {
                    // reload page
                    location.reload();
                }, 1000);
            }
        });
}

function editListener(){
    document.getElementById("edit-button").disabled = true;
    let form = document.getElementById("edit-form");
    let data = new FormData(form);

    // remove id
    data.delete("id");

    // have to increment the id by 1 because the id is 0 indexed
    fetch(`/listeners/${edit_listener_id + 1}/edit?json=true`, {
        method: "PUT",
        body: data
    }).then(response => response.json())
        .then(data => {
            // show notification
            showNotification(data.message, data.status);
            // check if success
            if (data.status === "success") {
                // sleep 1 second
                setTimeout(function () {
                    // reload page
                    location.reload();
                }, 1000);
            }
        });
    // activate button
    document.getElementById("edit-button").disabled = false;
}
function startListener(id) {
    fetch("/listeners/" + id + "/start?json=true", {
        method: "POST"
    }).then(response => response.json())
        .then(data => {
            // show notification
            showNotification(data.message, data.status);
            // check if success
            if (data.status === "success") {
                // sleep 1 second
                setTimeout(function () {
                    // reload page
                    location.reload();
                }, 1000);
            }
        });
}

function restartListener(id) {
    showNotification(`Restarting listener.`, "info");
    // set listener activity status to false
    document.getElementById("active-" + id).innerHTML = '<i class="material-icons" style="color: red; margin-top: 4px;">circle</i>'
    fetch("/listeners/" + id + "/restart?json=true", {
        method: "POST"
    }).then(response => response.json())
        .then(data => {
            // show notification
            showNotification(data.message, data.status);
            // check if success
            if (data.status === "success") {
                // set listener activity status to true
                document.getElementById("active-" + id).innerHTML = '<i class="material-icons" style="color: green; margin-top: 4px;">circle</i>';
            }
        });
}

function stopListener(id) {
    fetch("/listeners/" + id + "/stop?json=true", {
        method: "POST"
    }).then(response => response.json())
        .then(data => {
            // show notification
            showNotification(data.message, data.status);
            // check if success
            if (data.status === "success") {
                // sleep 1 second
                setTimeout(function () {
                    // reload page
                    location.reload();
                }, 1000);
            }
        });
}

function resetModal() {
    // reset modal content
    document.getElementById("create-modal-body").innerHTML = original_modal_content;
    changeCreateType();
}
function changeCreateType() {
    // get type from select
    const type = document.getElementById("type").value;
    // get corresponding form
    const form = document.getElementById(type + "-form");
    // change content of modal
    document.getElementById("create-form-content").innerHTML = form.innerHTML 
}

function createEdit(id) {
    if (id == edit_listener_id) {
        // open modal
        $("#edit-modal").modal("show");
        return;
    }
    let listener = listeners[id];
    // get form by type
    const form = document.getElementById(listener.type + "-form");

    // set modal body
    // replace all edit with create
    document.getElementById("edit-form").innerHTML = form.innerHTML.replace(/create/g, "edit");

    // set values
    document.getElementById("type-edit").remove();
    document.getElementById("id-edit").value = listener.id;
    document.getElementById("name-edit").value = listener.name;
    document.getElementById(listener.address + "-address-edit").selected = true;
    document.getElementById("port-edit").value = listener.port;
    document.getElementById("ssl-edit").checked = listener.ssl;
    document.getElementById("enabled-edit").checked = listener.enabled;
    document.getElementById("limit-edit").value = listener.limit;
    document.getElementById("timeout-edit").value = listener.timeout;
    // set options
    for (let option_name in listener.options) {
        if (Object.prototype.hasOwnProperty.call(listener.options, option_name)) {
            let option = listener.options[option_name];
            let element = document.getElementById(option_name.toLowerCase() + "-edit");
            if (element.type === "checkbox") {
                element.checked = option;
            }
            element.value = option;
        }
    }
    edit_listener_id = id;
    // open modal
    $("#edit-modal").modal("show");


}

