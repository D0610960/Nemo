var memberRef = firebase.database().ref("USERDATA/Member");
var pictureRef = firebase.database().ref("USERDATA/TakePicture");
var memberCards = $("#memberCards");

// clear modal
$(function () {
    $("#memberAdd").on("click", function () {
        $("#memberName").val("");
        $("#photoBtn2,#photoBtn3").prop("disabled", true);
        $(".addPhoto").prop('style', "display:none");
        $(".addPhoto").removeAttr('src');
    });
    $("#memberAddModal").on("show.bs.modal", function () {
        firebase.database().ref("USERDATA/TakePicture").update({
            Adding: true,
        });
    });
    $("#memberAddModal").on("hide.bs.modal", function () {
        firebase.database().ref("USERDATA/TakePicture").update({
            Adding: false,
        });
    });
    // take photo button control
    $(".photo").on("click", function () {
        var name = $("#memberName").val();
        name = name.trim();

        // set flag to take picture
        checkDuplicateName(name, this.value);
    });
});

// member confirm button handler
$("#memberUpdateBtn").on("click", function () {
    var name = $("#memberName").val();
    name = name.trim();
    //console.log(name);
    $("#memberAddModal").modal("show");

    // check input and update to firebase
    var listRef = firebase.storage().ref("face/" + name);
    listRef.listAll().then(function (res) {
        //console.log(res.items.length);
        if (res.items.length == 3) {
            memberRef.push(name);
            firebase.database().ref("USERDATA").update({
                Retrain: "on",
            });
            firebase.database().ref("USERDATA/TakePicture").update({
                Upload: "0",
                Adding: false
            });
            $("#memberAddModal").modal("hide");
        } else {
            alertStr = "Nemo需要正確的稱呼與三張臉部照片才能認識新成員喔";
            window.AppInventor.setWebViewString("alert" + alertStr);
        }
    });
});

function checkDuplicateName(memberName, imgNum) {
    var nameInput = document.getElementById("memberName");
    if (nameInput.checkValidity()) {
        var flag = true;
        memberRef.once("value").then(function (snapshot) {
            snapshot.forEach(function (childSnapshot) {
                if (childSnapshot.val() == memberName) {
                    flag = false;
                    nameInput.setCustomValidity("已經有相同的稱呼了，換一個吧");
                    nameInput.reportValidity();
                }
            });
            if (flag) {
                firebase.database().ref("USERDATA/TakePicture").update({
                    ImageNum: imgNum,
                    MemberName: memberName,
                });
            }
        });
    } else {
        if (nameInput.validity.valueMissing) {
            nameInput.setCustomValidity("Nemo該怎麼稱呼新成員呀");
            nameInput.reportValidity();
        } else if (nameInput.validity.patternMismatch) {
            nameInput.setCustomValidity("只可以使用英文字母與半形空格喔");
            nameInput.reportValidity();
        }
    }
}

function checkName() {
    var nameInput = document.getElementById("memberName");

    if (!nameInput.checkValidity()) {
        if (nameInput.validity.valueMissing) {
            nameInput.setCustomValidity("Nemo該怎麼稱呼新成員呀");
            nameInput.reportValidity();
        } else if (nameInput.validity.patternMismatch) {
            nameInput.setCustomValidity("只可以使用英文字母與半形空格喔");
            nameInput.reportValidity();
        }
    }
}

// firebase listening
memberRef.on("child_added", function (childSnapShot) {
    memberUpdateDOM(childSnapShot);
});

pictureRef.on("child_changed", function (childSnapShot) {
    if (childSnapShot.key == "Upload") {
        if (childSnapShot.val() != "0") {
            var temp = childSnapShot.val().split(",");
            var imgRef = firebase.storage().ref("face/" + temp[0]);
            imgRef.child(temp[1] + ".jpg").getDownloadURL().then((url) => {
                document.getElementById("photo" + temp[1]).src = url;
                document.getElementById("photo" + temp[1]).style.display = "block";
            });
            var nextNum = parseInt(temp[1]) + 1;
            if (nextNum < 4) {
                document.getElementById("photoBtn" + nextNum).disabled = false;
            }
        }
        firebase.database().ref("USERDATA/TakePicture").update({
            Upload: "0",
        });
    }
});

function memberUpdateDOM(childSnapShot) {
    // get member key & val
    var childObject = childSnapShot.val();
    var childObjectId = childSnapShot.key;
    //console.log("ID:" + childObjectId + " Name:" + childObject);

    var childRow = $("#" + childObjectId);

    if (childRow.length > 0) {
        // modify row
        childRow.find(".member-name").text(childObject);
    } else {
        // add new row
        var newContainer = $("<div>", {
                id: childObjectId,
                class: "w3-container member",
            }),
            newCard = $("<div>", {
                class: "w3-card",
                style: "background-color: #fbfbfb;",
            });

        var newImage1 = $("<img>", {
                class: "member-img",
                style: "display: block;",
                id: childObjectId + "1",
            }),
            newImage2 = $("<img>", {
                class: "member-img",
                id: childObjectId + "2",
            }),
            newImage3 = $("<img>", {
                class: "member-img",
                id: childObjectId + "3",
            });

        var buttonDiv = $("<div>", {
                style: "position: relative;",
            }),
            newBtn1 = $("<button>", {
                type: "button",
                class: "number-btn",
                value: "1",
                text: "1",
                name: childObjectId,
                disabled: true,
            }),
            newBtn2 = $("<button>", {
                type: "button",
                class: "number-btn",
                style: "right: 60px;",
                value: "2",
                text: "2",
                name: childObjectId,
            }),
            newBtn3 = $("<button>", {
                type: "button",
                class: "number-btn",
                style: "right: 12px;",
                value: "3",
                text: "3",
                name: childObjectId,
            });
        buttonDiv.append(newBtn1, newBtn2, newBtn3);

        var contentDiv = $("<div>", {
                class: "w3-container",
            }),
            newName = $("<h3>", {
                text: childObject,
                class: "member-name",
            }),
            MdeleteBtn = $("<button>", {
                class: "btn memberDeleteBtn font-en",
                "data-id": childObjectId,
            }),
            MdeleteBtnIcon = $("<i>", {
                class: "fa fa-trash fa-lg",
            });
        contentDiv.append(newName, MdeleteBtn.append(MdeleteBtnIcon, "  Delete"));

        newCard.append(newImage1, newImage2, newImage3, buttonDiv, contentDiv);
        memberCards.append(newContainer.append(newCard));

        // get image url
        var imgRef = firebase.storage().ref("face/" + childObject);
        for (let i = 1; i < 4; i++) {
            imgRef
                .child(i + ".jpg")
                .getDownloadURL()
                .then((url) => {
                    document.getElementById(childObjectId + i).src = url;
                });
        }
    }
}

// delete button handler
memberCards.on("click", ".memberDeleteBtn", function () {
    var member_id = $(this).data("id");
    var member_ref = memberRef.child(member_id);
    memberRef.on("child_removed", function (snapshot) {
        $("#" + snapshot.key).remove();
        var floderRef = firebase.storage().ref("face/" + snapshot.val());
        for (let i = 1; i < 4; i++) {
            floderRef.child(i + ".jpg").delete();
        }
    });
    member_ref.remove();
    firebase.database().ref("USERDATA").update({
        Retrain: "on",
    });
});

// display control
memberCards.on("click", ".number-btn", function () {
    var clickNum = this.value;
    var imgId = this.name;
    //console.log(clickNum, imgId);
    var btns = document.getElementsByName(imgId);
    for (let i = 1; i < 4; i++) {
        if (i == clickNum) {
            btns[i - 1].disabled = true;
            document.getElementById(imgId + i).style.display = "block";
        } else {
            btns[i - 1].disabled = false;
            document.getElementById(imgId + i).style.display = "none";
        }
    }
});

function backHome() {
    window.AppInventor.setWebViewString("backHome");
}