function delAcc() {
    firebase.database().ref("USERDATA/Nickname").remove();
    firebase.database().ref("USERDATA/Account").remove();
    firebase.database().ref("USERDATA/Password").remove();
}

function keepLogin() {
    let re = /\[|\]|\"|\s+/g;
    let appInventorInput = window.AppInventor.getWebViewString();
    appInventorInput = appInventorInput.replace(re, "").split(",");
    let loginDict = {
        acc: appInventorInput[0],
        psw: appInventorInput[1],
        rem: appInventorInput[2]
    };
    if (loginDict["rem"] == "yes") {
        document.getElementById("keep").checked = true;
        document.getElementById("acc").value = loginDict["acc"];
        document.getElementById("psw").value = loginDict["psw"];
    } else {
        document.getElementById("keep").checked = false;
    }
}

function writeData(name, acc, psw) {
    name = name.trim();
    firebase.database().ref("USERDATA").update({
        Nickname: name,
        Account: acc,
        Password: psw
    });
    console.log("write succeeded");
}

document.getElementById("logForm").addEventListener("submit", function (e) {
    let formData = new FormData(document.getElementById("logForm"));
    let rootRef = firebase.database().ref("USERDATA");

    rootRef.once("value", function (rootSnap) {
        if (!rootSnap.child("USERDATA").exists()) {
            if (rootSnap.child("Account").val() == formData.get("acc") &&
                rootSnap.child("Password").val() == formData.get("psw")) {
                let webStr = "";
                if (formData.get("keep") == "on") {
                    webStr = formData.get("acc") + "," + formData.get("psw") + "," + "yes";
                } else {
                    webStr = formData.get("acc") + "," + formData.get("psw") + "," + "no";
                }
                window.AppInventor.setWebViewString(webStr);
            } else {
                alertStr = "登入失敗，帳號或密碼錯誤";
                window.AppInventor.setWebViewString("alert" + alertStr);
            }
        }
    })
    e.preventDefault();
})

document.getElementById("signForm").addEventListener("submit", function (e) {
    let formData = new FormData(document.getElementById("signForm"));
    let rootRef = firebase.database().ref("USERDATA");

    rootRef.once("value", function (rootSnap) {
        if (!rootSnap.child("Account").exists() || !rootSnap.child("Nickname").exists() ||
            !rootSnap.child("Password").exists()) {
            writeData(formData.get("name"), formData.get("acc"), formData.get("psw"));
            window.AppInventor.setWebViewString("first");
        } else {
            alertStr = "已經註冊過了";
            window.AppInventor.setWebViewString("alert" + alertStr);
        }
    })
    e.preventDefault();
})