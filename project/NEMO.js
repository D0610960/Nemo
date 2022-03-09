/* timing tools */

/* alarm */
var alarmRef = firebase.database().ref('ALARM');
var alarmTable = $('#alarmTable');

// alarm confirm button handler
$('#alarmUpdateBtn').on('click', function () {
  var time = $('#alarmTime').val(),
    week = $("input[name='alarmWeek[]']:checked").map(function () {
      return $(this).val();
    }).get(),
    sound = $('#alarmSound').val(),
    title = $('#alarmTitle').val();
  $("#alarmAddModal").modal("show");

  if (week.length == 0) {
    week.push("");
  }

  if (checkAlarmInputs("alarmTime")) {
    // update to firebase
    alarmRef.push({
      AlarmTime: time,
      Week: week,
      Sound: sound,
      Title: title
    });
    $("#alarmAddModal").modal("hide");
  }
})

// firebase listening
alarmRef.on("child_added", function (childSnapShot) {
  alarmUpdateDOM(childSnapShot);
});

alarmRef.on("child_changed", function (childSnapShot) {
  alarmUpdateDOM(childSnapShot);
});

function alarmUpdateDOM(childSnapShot) {
  // get alarm key & val
  var childObject = childSnapShot.val();
  var childObjectId = childSnapShot.key;
  //console.log(childObject, childObjectId);

  var childRow = $("#" + childObjectId);
  if (childObject.Week == "") {
    var weekFormat = "Once";
  } else {
    var weekFormat = String(childObject.Week).replace(new RegExp(",", "g"), ", ");
  }

  if (childRow.length > 0) {
    // modify row
    childRow.find(".alarm-title").text(childObject.Title);
    childRow.find(".alarm-time").text(childObject.AlarmTime);
    childRow.find(".alarm-week").text(weekFormat);
  } else {
    // add new row
    var newAlarmTime = $('<td>', {
        text: childObject.AlarmTime,
        class: "alarm-time"
      }),
      newWeek = $('<td>', {
        text: weekFormat,
        class: "alarm-week"
      }),
      newTitle = $('<td>', {
        text: childObject.Title,
        class: "alarm-title"
      });

    var AeditBtn = $('<button>', {
        class: "btn alarmEditBtn",
        style: "background-color:#80A2D1;color:white;font-size:16px;padding:8px 10px 4px;line-height:1.5;border-radius:4px;margin:5px",
        'data-id': childObjectId
      }),
      AeditBtnIcon = $('<span>', {
        class: "glyphicon glyphicon-edit",
        style: ""
      }),

      AdeleteBtn = $('<button>', {
        class: "btn alarmDeleteBtn",
        style: "background-color:#F1656E;color:white;font-size:16px;padding:8px 10px 4px;line-height:1.5;border-radius:4px;margin:5px",
        'data-id': childObjectId
      }),
      AdeleteBtnIcon = $('<span>', {
        class: "glyphicon glyphicon-remove"
      });

    var childRow = $('<tr>', {
      id: childObjectId,
      class: "font-en"
    });

    var rowButton = $('<td>');
    rowButton.append(AeditBtn.append(AeditBtnIcon), AdeleteBtn.append(AdeleteBtnIcon))

    var rowLine = $('<tr>', {
        id: childObjectId + "line"
      }),
      rowSpace = $('<td colspan="4">', {
        style: "position: relative;"
      }),
      lineImage = $('<img>', {
        src: "./line.png",
        style: "display:block;margin:32px 0px;height:2px;width:100%;opacity:0.4;"
      })
    rowLine.append(rowSpace.append(lineImage))

    childRow.append(newTitle, newAlarmTime, newWeek, rowButton);
    alarmTable.append(rowLine, childRow);
  }
}

// edit button handler
alarmTable.on('click', '.alarmEditBtn', function () {
  var alarm_id = $(this).data('id');
  var alarm_ref = alarmRef.child(alarm_id);

  alarm_ref.once('value', function (snapshot) {
    $('#modal-edit-Atime').val(snapshot.val().AlarmTime);
    $("input[name='modal-edit-Aweek[]']").map(function () {
      return $(this).val(snapshot.val().Week);
    }).get();
    $('#modal-edit-Asound').val(snapshot.val().Sound);
    $('#modal-edit-Atitle').val(snapshot.val().Title);
    $('#alarm-id').val(alarm_id);
    $("#alarmEditModal").modal("show");
  });
});

function alarmEdit(childRef) {
  var newtime = $('#modal-edit-Atime').val(),
    newweek = $("input[name='modal-edit-Aweek[]']:checked").map(function () {
      return $(this).val();
    }).get(),
    newsound = $('#modal-edit-Asound').val(),
    newtitle = $('#modal-edit-Atitle').val();

  if (newweek.length == 0) {
    newweek.push("");
  }

  // update to firebase
  childRef.update({
    AlarmTime: newtime,
    Week: newweek,
    Sound: newsound,
    Title: newtitle
  });
}

$("#alarmEditModal").on('click', '#alarmEditBtn', function () {
  var childRef = alarmRef.child($('#alarmEditModal').find('#alarm-id').val());
  if (checkAlarmInputs("modal-edit-Atime")) {
    alarmEdit(childRef);
    $("#alarmEditModal").modal("hide");
  }
})

// delete button handler
alarmTable.on('click', '.alarmDeleteBtn', function () {
  var alarm_id = $(this).data('id');
  var alarm_ref = alarmRef.child(alarm_id);
  alarmRef.on('child_removed', function (snapshot) {
    $('#' + snapshot.key).remove();
  });
  alarm_ref.remove();
  deleteLine(alarm_id + "line", "alarmTable");
  document.getElementById('alarmAdd').disabled = false;
})

/* memo */
var memoRef = firebase.database().ref('MEMO');
var memoTable = $('#memoTable');

// memo confirm button handler
$('#memoUpdateBtn').on('click', function () {
  var time = $('#memoTime').val(),
    date = $('#memoDate').val(),
    week = $("input[name='memoWeek[]']:checked").map(function () {
      return $(this).val();
    }).get(),
    repeat = $("input[name='memoRepeat']:checked").map(function () {
      return $(this).val();
    }).get(),
    text = $('#memoText').val();
  $("#memoAddModal").modal("show");

  if (week.length == 0) {
    week.push("");
  }
  if (repeat.length == 0) {
    repeat.push("");
  }

  if (checkMemoInputs("memoTime", "memoText")) {
    // update to firebase
    memoRef.push({
      MemoTime: time,
      Date: date,
      Week: week,
      Text: text,
      Repeat: repeat,
      Flag: true
    });
    $("#memoAddModal").modal("hide");
  }
})

// firebase listening
memoRef.on("child_added", function (childSnapShot) {
  memoUpdateDom(childSnapShot);
});

memoRef.on("child_changed", function (childSnapShot) {
  memoUpdateDom(childSnapShot);
});

function memoUpdateDom(childSnapShot) {
  // get memo key & val
  var childObjectId = childSnapShot.key;
  var childObject = childSnapShot.val();

  var childRow = $("#" + childObjectId);
  var dateFormat = "",
    weekFormat = "";
  if (childObject.Date != "") {
    dateFormat = String(new Date(childObject.Date));
    if (childObject.Repeat == "yes") {
      dateFormat = dateFormat.slice(8, 10) + 'th of Each Month';
    } else {
      dateFormat = dateFormat.slice(4, 10) + ", " + dateFormat.slice(11, 15);
    }
  }
  if (childObject.Week != "") {
    weekFormat = String(childObject.Week).replace(new RegExp(",", "g"), ", ");
  }
  if (childRow.length > 0) {
    // modify row
    childRow.find(".memo-time").text(childObject.MemoTime);
    if (childObject.Date == "") {
      childRow.find(".memo-da").text(weekFormat);
    } else {
      childRow.find(".memo-da").text(dateFormat);
    }
    childRow.find(".memo-text").text(childObject.Text);
  } else {
    // add new row
    var newMemoTime = $('<td>', {
      text: childObject.MemoTime,
      class: "memo-time"
    })
    if (childObject.Date == "") {
      var newDa = $('<td>', {
        text: weekFormat,
        class: "memo-da"
      })
    } else {
      var newDa = $('<td>', {
        text: dateFormat,
        class: "memo-da"
      })
    }
    var newText = $('<td>', {
      text: childObject.Text,
      class: "memo-text"
    })

    var NeditBtn = $('<button>', {
        class: "btn memoEditBtn",
        style: "background-color:#80A2D1;color:white;font-size:16px;padding:8px 10px 4px;line-height:1.5;border-radius:4px;margin:5px",
        'data-id': childObjectId
      }),
      NeditBtnIcon = $('<span>', {
        class: "glyphicon glyphicon-edit",
        style: ""
      }),

      NdeleteBtn = $('<button>', {
        class: "btn memoDeleteBtn",
        style: "background-color:#F1656E;color:white;font-size:16px;padding:8px 10px 4px;line-height:1.5;border-radius:4px;margin:5px",
        'data-id': childObjectId
      }),
      NdeleteBtnIcon = $('<span>', {
        class: "glyphicon glyphicon-remove"
      });

    var childRow = $('<tr>', {
      id: childObjectId,
      class: "font-en"
    });

    var rowButton = $('<td>');
    rowButton.append(NeditBtn.append(NeditBtnIcon), NdeleteBtn.append(NdeleteBtnIcon))

    var rowLine = $('<tr>', {
        id: childObjectId + "line"
      }),
      rowSpace = $('<td colspan="4">', {
        style: "position: relative;"
      }),
      lineImage = $('<img>', {
        src: "./line.png",
        style: "display:block;margin:32px 0px;height:2px;width:100%;opacity:0.4;"
      })
    rowLine.append(rowSpace.append(lineImage))

    childRow.append(newText, newMemoTime, newDa, rowButton);
    memoTable.append(rowLine, childRow);
  }
}

// edit button handler
memoTable.on('click', '.memoEditBtn', function () {
  var memo_id = $(this).data('id');
  var memo_ref = memoRef.child(memo_id);
  memo_ref.once('value', function (snapshot) {
    $('#modal-edit-Mtime').val(snapshot.val().MemoTime);
    $('#modal-edit-Mdate').val(snapshot.val().Date);
    $("input[name='modal-edit-Mweek[]']").map(function () {
      return $(this).val(snapshot.val().Week);
    }).get();
    $("input[name='modal-edit-MRepeat']").map(function () {
      return $(this).val(snapshot.val().Repeat);
    }).get();
    if ($('#modal-edit-Mdate').val() != "") {
      $("input[name='modal-edit-MRepeat']:disabled").attr("disabled", false);
    } else {
      $("input[name='modal-edit-MRepeat']:disabled").attr("disabled", true);
    }
    $('#modal-edit-Mtext').val(snapshot.val().Text);
    $('#memo-id').val(memo_id);
    $("#memoEditModal").modal("show");
  });
});

function memoEdit(childRef) {
  var
    newtime = $('#modal-edit-Mtime').val(),
    newdate = $('#modal-edit-Mdate').val(),
    newweek = $("input[name='modal-edit-Mweek[]']:checked").map(function () {
      return $(this).val();
    }).get(),
    newrepeat = $("input[name='modal-edit-MRepeat']:checked").map(function () {
      return $(this).val();
    }).get(),
    newtext = $('#modal-edit-Mtext').val();

  if (newweek.length == 0) {
    newweek.push("");
  }
  if (newrepeat.length == 0) {
    newrepeat.push("");
  }

  // update to firebase
  childRef.update({
    MemoTime: newtime,
    Date: newdate,
    Week: newweek,
    Text: newtext,
    Repeat: newrepeat,
    Flag: true
  });
}

$("#memoEditModal").on('click', '#memoEditBtn', function () {
  var childRef = memoRef.child($('#memoEditModal').find('#memo-id').val());
  if (checkMemoInputs("modal-edit-Mtime", "modal-edit-Mtext")) {
    memoEdit(childRef);
    $("#memoEditModal").modal("hide");
  }
})

// delete button handler
memoTable.on('click', '.memoDeleteBtn', function () {
  var memo_id = $(this).data('id');
  var memo_ref = memoRef.child(memo_id);
  memoRef.on('child_removed', function (snapshot) {
    $('#' + snapshot.key).remove();
  });
  memo_ref.remove();
  deleteLine(memo_id + "line", "memoTable");
  document.getElementById('memoAdd').disabled = false;
})

function deleteLine(lineRowId, tableName) {
  var index = document.getElementById(lineRowId).rowIndex;
  document.getElementById(tableName).deleteRow(index);
}

// input control
$(function () {
  $("#alarmAdd").on('click', function () {
    alarmRef.once("value").then(function (snapshot) {
      if (snapshot.numChildren() == 20) {
        document.getElementById('alarmAdd').disabled = true;
        alertStr = "你設定太多鬧鐘啦";
        window.AppInventor.setWebViewString("alert" + alertStr);
      }
    });
    var now = new Date();
    var addOneMinute = now;
    addOneMinute.setMinutes(now.getMinutes() + 1)
    var time = String(addOneMinute).slice(16, 21);
    $('#alarmTime').val(time);
    $("input[name='alarmWeek[]']:checked").prop("checked", false);
    $('#alarmTitle').val('');
  });

  $("input[name='memoRepeat']").attr("disabled", true);
  $("input[name='modal-edit-MRepeat']").attr("disabled", true);

  $("input[name='memoWeek[]']").click(function () {
    $("#memoDate").val("");
    $("input[name='memoRepeat']:checked").prop("checked", false);
    $("input[name='memoRepeat']").attr("disabled", true);
  });
  $("#memoDate").click(function () {
    $("input[name='memoWeek[]']:checked").prop("checked", false);
    $("input[name='memoRepeat']:checked").prop("checked", false);
    $("input[name='memoRepeat']").attr("disabled", false);
  });
  $("input[name='modal-edit-Mweek[]']").click(function () {
    $("#modal-edit-Mdate").val("");
    $("input[name='modal-edit-MRepeat']:checked").prop("checked", false);
    $("input[name='modal-edit-MRepeat']").attr("disabled", true);
  });
  $("#modal-edit-Mdate").click(function () {
    $("input[name='modal-edit-Mweek[]']:checked").prop("checked", false);
    $("input[name='modal-edit-Mweek[]']:checked").prop("checked", false);
    $("input[name='modal-edit-MRepeat']").attr("disabled", false);
  });

  $("#memoAdd").on('click', function () {
    memoRef.once("value").then(function (snapshot) {
      if (snapshot.numChildren() == 20) {
        document.getElementById('memoAdd').disabled = true;
        alertStr = "你設定太多備忘錄啦";
        window.AppInventor.setWebViewString("alert" + alertStr);
      }
    });
    var now = new Date();
    var addOneMinute = now;
    addOneMinute.setMinutes(now.getMinutes() + 1)
    var time = String(addOneMinute).slice(16, 21);
    $('#memoTime').val(time);
    $('#memoDate').val("");
    $("input[name='memoWeek[]']:checked").prop("checked", false);
    $("input[name='memoRepeat']").attr("disabled", true);
    $('#memoText').val("");
  });
});

function checkAlarmInputs(timeId) {
  let time = document.getElementById(timeId);
  if (time.checkValidity()) {
    return true;
  } else {
    time.setCustomValidity("響鈴時間一定要填寫喔");
    time.reportValidity();
    return false;
  }
}

function checkMemoInputs(timeId, textId) {
  let time = document.getElementById(timeId);
  let text = document.getElementById(textId);
  if (time.checkValidity() && text.checkValidity()) {
    return true;
  } else {
    if (time.validity.valueMissing) {
      time.setCustomValidity("提醒時間一定要填寫喔");
      time.reportValidity();
    } else if (text.validity.valueMissing) {
      text.setCustomValidity("提醒文字一定要填寫喔");
      text.reportValidity();
    }
    return false;
  }
}

/* indoor monitor */
/* canvas */
let timeLabels = [];
let dateMark = '';
let H = [];
let T = [];
let G = [];
let cnt = 0;
let today = new Date(+new Date() + 8 * 3600 * 1000);
let endTime = new Date().toTimeString().substr(0, 5);
let endDate = today.toISOString().substr(0, 10);
let startTime = "";
let startDate = "";

if (endTime >= "00:00" && endTime <= "05:59"){
  if (endTime <= "00:59"){
    startTime = 12-(endTime.substr(0, 2))+6 + ":" + endTime.substr(3, 5);
  }
  else if (endTime <= "01:59"){
    startTime = 12-(endTime.substr(0, 2))+8 + ":" + endTime.substr(3, 5);
  }
  else if (endTime <= "02:59"){
    startTime = 12-(endTime.substr(0, 2))+10 + ":" + endTime.substr(3, 5);
  }
  else if (endTime <= "03:59"){
    startTime = 12-(endTime.substr(0, 2))+12 + ":" + endTime.substr(3, 5);
  }
  else if (endTime <= "04:59"){
    startTime = 12-(endTime.substr(0, 2))+14 + ":" + endTime.substr(3, 5);
  }
  else if (endTime <= "05:59"){
    startTime = 12-(endTime.substr(0, 2))+16 + ":" + endTime.substr(3, 5);
  }
  today.setDate(today.getDate() - 1);
  startDate = today.toISOString().substr(0, 10);
}
else{
  startTime = ((endTime.substr(0, 2))-06) + ":" + endTime.substr(3, 5);
}

if (startTime >= "0:00" && startTime <= "9:59"){
  startTime = "0"+startTime;
}

// lastest data
function getHT() {
  let ref = firebase.database().ref("DHT").child(endDate);
  let dataH = "";
  let dataT = "";
  ref.on("value", dateSnap => {
    dateSnap.forEach(function (timeSnap) {
      let temp = new Date(dateSnap.key + " " + timeSnap.key);
      temp = String(temp).slice(0, 21);
      document.getElementById("dhtTime").innerHTML = temp;
      timeSnap.forEach(function (HTSnap) {
        if (HTSnap.key == "Humidity") {
          dataH = "<i class=flaticon-humidity></i>" + HTSnap.val() + "%";
          document.getElementById("humidity").innerHTML = dataH;
        } else if (HTSnap.key == "Temperature") {
          dataT = "<i class=flaticon-hot></i>" + HTSnap.val() + "°C";
          document.getElementById("temperature").innerHTML = dataT;
        }
      })
    })
  })
}

function getGas() {
  let ref = firebase.database().ref("GAS").child(endDate);;
  let dataG = "";

  ref.once("value", function (dateSnap) {
    dateSnap.forEach(function (timeSnap) {
      dataG = "<i class=flaticon-gas></i>" + timeSnap.child('Gas').val();
      document.getElementById("gas").innerHTML = dataG;
    })
  })
}

function drawAllCanvas() {

  let ref = firebase.database().ref("USERDATA").child("TempMode");
  ref.on("value", snap => {
    var ctx = document.getElementById("humidityCanvas").getContext("2d");
    drawLineCanvas(ctx, lineChartDataHumidity, "%", "");
    var ctxT = document.getElementById("temperatureCanvas").getContext("2d");
    drawLineCanvas(ctxT, lineChartDataTemperature, "°" + snap.val(), "");
    var ctxG = document.getElementById("gasCanvas").getContext("2d");
    drawLineCanvas(ctxG, lineChartDataGasvalue, "", "gas");
  })
}

function getHT_6H() {
  let dataH = "";
  let dataT = "";
  if (endTime >= "00:00" && endTime <= "05:59"){
    let ref = firebase.database().ref("DHT").child(startDate);
    ref.on("value", datesnap => {
      datesnap.forEach(function (timeSnap) {
        let uploaddate = startDate.slice(5, 7) + '/' + startDate.slice(8, 10);
        let uploadtime = timeSnap.key.slice(0, 5);
        timeSnap.forEach(function (HTSnap) {
          if (HTSnap.key == "Humidity") {
            dataH = HTSnap.val();
            if (uploadtime >= startTime  && uploadtime <= "23:59") {
              H.push(dataH);
              if (uploaddate != dateMark) {
                timeLabels.push([uploadtime, uploaddate]);
                dateMark = uploaddate;
              } else {
                timeLabels.push(uploadtime);
              }
            }
          }
          else if (HTSnap.key == "Temperature") {
            dataT = HTSnap.val();
            if (uploadtime >= startTime  && uploadtime <= "23:59") {
              T.push(dataT);
            }
          }
        })
      })
    })
  }
  let ref = firebase.database().ref("DHT").child(endDate);
  ref.on("value", datesnap => {
    datesnap.forEach(function (timeSnap) {
      let uploaddate = endDate.slice(5, 7) + '/' + endDate.slice(8, 10);
      let uploadtime = timeSnap.key.slice(0, 5);
      timeSnap.forEach(function (HTSnap) {
        if (HTSnap.key == "Humidity") {
          dataH = HTSnap.val();
          if (endTime >= "00:00" && endTime <= "05:59"){
            if (uploadtime >= "00:00"  && uploadtime <= endTime) {
              H.push(dataH)
              if (uploaddate != dateMark) {
                timeLabels.push([uploadtime, uploaddate]);
                dateMark = uploaddate;
              } else {
                timeLabels.push(uploadtime);
              }
            }
          }
          else {
            if (uploadtime >= "00:00"  && uploadtime <= "23:59") {
              H.push(dataH)
              if (uploaddate != dateMark) {
                timeLabels.push([uploadtime, uploaddate]);
                dateMark = uploaddate;
              } else {
                timeLabels.push(uploadtime);
              }
            }
          }
          
        }
        else if (HTSnap.key == "Temperature") {
          dataT = HTSnap.val();
          if (tempMode == "F") {
            dataT = dataT * (9 / 5) + 32;
          }
          if (endTime >= "00:00" && endTime <= "05:59"){
            if (uploadtime >= "00:00"  && uploadtime <= endTime) {
              T.push(dataT);
            }
          }
          else {
            if (uploadtime >= startTime  && uploadtime <= "23:59") {
              T.push(dataT);
            }
          }
          
        }
      })
    })
  })
}

function getG_6H() {
  let dataG = "";
  
  if (endTime >= "00:00" && endTime <= "05:59"){
    let ref = firebase.database().ref("GAS").child(startDate);
    ref.on("value", datesnap => {
      datesnap.forEach(function (timeSnap) {
        let uploadtime = timeSnap.key.slice(0, 5);
        timeSnap.forEach(function (GSnap) {
          if (GSnap.key == "GasValue") {
            dataG = GSnap.val();
            if (uploadtime >= startTime  && uploadtime <= "23:59") {
              G.push(dataG);
            }
          }
        })
      })
    })
  }
  let ref = firebase.database().ref("GAS").child(endDate);
  ref.on("value", datesnap => {
    cnt += 1;
    datesnap.forEach(function (timeSnap) {
      let uploadtime = timeSnap.key.slice(0, 5);
      timeSnap.forEach(function (GSnap) {
        if (GSnap.key == "GasValue") {
          dataG = GSnap.val();
          if (endTime >= "00:00" && endTime <= "05:59"){
            if (uploadtime >= "00:00"  && uploadtime <= endTime) {
              G.push(dataG);
            }
          }
          else {
            if (uploadtime >= startTime  && uploadtime <= "23:59") {
              G.push(dataG);
            }
          }
        }

      })
      let arrayLen = G.length;
      if (cnt > 1 ){
        H.splice(0, arrayLen);
        T.splice(0, arrayLen);
        G.splice(0, arrayLen);
        timeLabels.splice(0, arrayLen);
        cnt = 1;
      }
      drawAllCanvas();
    })
  })
}


getHT();
getGas();
getHT_6H();
getG_6H();


var lineChartDataHumidity = {
  labels: timeLabels,
  datasets: [{
    label: 'Humidity',
    lineTension: 0.3,
    backgroundColor: "#7196c7",
    borderColor: "#7196c7",
    borderWidth: 2,
    data: H,
    fill: false,
  }, ]
};

var lineChartDataTemperature = {
  labels: timeLabels,
  datasets: [{
    label: 'Temperature',
    lineTension: 0.3,
    backgroundColor: "#d1677e",
    borderColor: "#d1677e",
    borderWidth: 2,
    data: T,
    fill: false,
  }, ]
};

var lineChartDataGasvalue = {
  labels: timeLabels,
  datasets: [{
    label: 'Gas Value',
    lineTension: 0.3,
    backgroundColor: "#da7f4a",
    borderColor: "#da7f4a",
    borderWidth: 2,
    data: G,
    fill: false,
  }, ]
};

function drawLineCanvas(ctx, data, label, lineid) {
  window.myLine = new Chart(ctx, {
    type: 'line',
    data: data,
    options: {
      responsive: true,
      elements: {
        point: {
          radius: 0,
        },
      },
      title: {
        display: false
      },
      legend: {
        display: false,
        labels: {
          boxWidth: 12
        },
      },
      tooltips: {
        mode: 'index',
        intersect: false
      },
      hover: {
        mode: 'index',
        intersect: false
      },
      scales: {
        xAxes: [{
          display: true,
          gridLines: {
            display: true,
            lineWidth: 1,
            drawTicks: true,
            tickMarkLength: 16,
            color: "rgba(0, 0, 0, 0.1)"
          },
          ticks: {
            userCallback: function (item, index) {
              if (!(index % 12)) return item;
            },
            autoSkip: false,
            fontSize: 14,
            fontFamily: "Titillium Web",
            maxRotation: 0,
            fontStyle: "bold"
          }
        }],
        yAxes: [{
          display: true,
          id: lineid,
          type: 'linear',
          gridLines: {
            display: true,
            lineWidth: 1,
            zeroLineWidth: 3,
            drawTicks: true,
            tickMarkLength: 16,
            color: "rgba(0, 0, 0, 0.1)"
          },
          ticks: {
            fontSize: 14,
            fontFamily: "Titillium Web",
            fontStyle: "bold",
            beginAtZero: false
          },
          scaleLabel: {
            display: true,
            labelString: label,
            fontSize: 18,
            fontFamily: "Titillium Web",
            fontColor: "696e75",
            fontStyle: "bold"
          }
        }]
      },
      annotation: {
        annotations: [{
            type: 'line',
            mode: 'horizontal',
            scaleID: 'gas',
            value: '0.4',
            borderColor: '#ffc642',
            borderWidth: 2,
            label: {
              enabled: false,
              content: 'Warning',
              position: 'right',
            }
          },
          {
            type: 'line',
            mode: 'horizontal',
            scaleID: 'gas',
            value: '0.6',
            borderColor: '#ff7575',
            borderWidth: 2,
            label: {
              enabled: false,
              content: 'Danger',
              position: 'right',
            }
          },
        ]
      }
    }
  });
}


/* home security */

// real time image
function getImage() {
  let modal = document.getElementById("imgModal");
  let image = document.getElementById("img");

  let ref = firebase.database().ref("CAMERA/Image");
  ref.on("value", snap => {
    ref = firebase.storage().ref('image').child(snap.val());
    ref.getDownloadURL().then((url) => {
      image.src = url;

      ref.getMetadata().then(function (metadata) {
        for (key in metadata) {
          if (key == 'updated') {
            name = metadata[key];
          }
        }

        let time = snap.val().slice(4, 10);
        time = time.substr(0, 2) + ":" + time.substr(2, 2) + ":" + time.substr(4, 2);
        let temp = new Date(name.slice(0, 10) + " " + time);
        temp = String(temp).slice(0, 24);
        document.getElementById('imgTime').innerHTML = temp;
      })

      // modal
      image.onclick = function () {
        modal.style.display = "block";
        document.getElementById("imgL").src = url;
      }
      let span = document.getElementsByClassName("closeImgL")[0];
      span.onclick = function () {
        modal.style.display = "none";
      }
    })
  })
}

// family image
var slideIndexFamily = 1;
showSlidesFamily(slideIndexFamily);

function plusSlidesFamily(n) {
  showSlidesFamily(slideIndexFamily += n);
}

function showSlidesFamily(n) {
  let iFamily;
  let slidesFamily = document.getElementsByClassName("slideFamily");
  if (n > slidesFamily.length) {
    slideIndexFamily = slidesFamily.length
  }
  if (n < 1) {
    slideIndexFamily = 1
  }
  getSlidesURL("f", slideIndexFamily);
  for (iFamily = 0; iFamily < slidesFamily.length; iFamily++) {
    slidesFamily[iFamily].style.display = "none";
  }
  slidesFamily[slideIndexFamily - 1].style.display = "block";
}

// stranger image
var slideIndexStranger = 1;
showSlidesStranger(slideIndexStranger);

function plusSlidesStranger(n) {
  showSlidesStranger(slideIndexStranger += n);
}

function showSlidesStranger(n) {
  let iStranger;
  let slidesStranger = document.getElementsByClassName("slideStranger");
  if (n > slidesStranger.length) {
    slideIndexStranger = slidesStranger.length;
  }
  if (n < 1) {
    slideIndexStranger = 1;
  }
  getSlidesURL("s", slideIndexStranger);
  for (iStranger = 0; iStranger < slidesStranger.length; iStranger++) {
    slidesStranger[iStranger].style.display = "none";
  }
  slidesStranger[slideIndexStranger - 1].style.display = "block";
}

// unknown image
var slideIndexUnknown = 1;
showSlidesUnknown(slideIndexUnknown);

function plusSlidesUnknown(n) {
  showSlidesUnknown(slideIndexUnknown += n);
}

function showSlidesUnknown(n) {
  let iUnknown;
  let slidesUnknown = document.getElementsByClassName("slideUnknown");
  if (n > slidesUnknown.length) {
    slideIndexUnknown = slidesUnknown.length
  }
  if (n < 1) {
    slideIndexUnknown = 1
  }
  getSlidesURL("u", slideIndexUnknown);
  for (iUnknown = 0; iUnknown < slidesUnknown.length; iUnknown++) {
    slidesUnknown[iUnknown].style.display = "none";
  }
  slidesUnknown[slideIndexUnknown - 1].style.display = "block";
}

function getSlidesURL(type, index) {
  if (type == "s") {
    var strangerID = new Array();
    for (iStranger = 0; iStranger <= 5; iStranger++) {
      strangerID[iStranger] = document.getElementById('strangerImg' + iStranger);
    }

    firebase.database().ref("CAMERA/Stranger").once("value", snap => {
      if (snap.child(index).val()) {
        firebase.storage().ref('image').child(snap.child(index).val()).getDownloadURL().then((url) => {
          strangerID[index].src = url;
        })
      }
    })
  } else if (type == "u") {
    var unknownID = new Array();
    for (iUnknown = 0; iUnknown <= 5; iUnknown++) {
      unknownID[iUnknown] = document.getElementById('unknownImg' + iUnknown);
    }

    firebase.database().ref("CAMERA/Unknown").once("value", snap => {
      if (snap.child(index).val()) {
        firebase.storage().ref('image').child(snap.child(index).val()).getDownloadURL().then((url) => {
          unknownID[index].src = url;
        })
      }
    })
  } else {
    var familyID = new Array();
    for (iFamily = 0; iFamily <= 5; iFamily++) {
      familyID[iFamily] = document.getElementById('familyImg' + iFamily);
    }

    firebase.database().ref("CAMERA/Family").once("value", snap => {
      if (snap.child(index).val()) {
        firebase.storage().ref('image').child(snap.child(index).val()).getDownloadURL().then((url) => {
          familyID[index].src = url;
        })
      }
    })
  }
}

/* wheather forecast */
function getWxIcon(value) {
  let index = parseInt(value);
  let path = "";
  if (index == 1) {
    path = "./icon/01.png";
  } else if (index == 2) {
    path = "./icon/02.png";
  } else if (index == 3) {
    path = "./icon/03.png";
  } else if (index == 4) {
    path = "./icon/04.png";
  } else if (index == 5) {
    path = "./icon/05.png";
  } else if (index == 6) {
    path = "./icon/06.png";
  } else if (index == 7) {
    path = "./icon/07.png";
  } else if ((index > 32) && (index < 37)) {
    path = "./icon/10.png";
  } else if ((index == 23) || (index == 42)) {
    path = "./icon/11.png";
  } else if (index == 37) {
    path = "./icon/12.png";
  } else if ((index > 23) && (index < 29)) {
    path = "./icon/13.png";
  } else if ((index > 11) && (index < 19) || (index == 39) || (index == 40)) {
    path = "./icon/09.png";
  } else {
    path = "./icon/08.png";
  }
  return path;
}

function getUserLoc() {
  let ref = firebase.database().ref("USERDATA");
  ref.once("value", snap => {
    document.getElementById("loc").innerHTML = "<i class=flaticon-placeholder></i>" + snap.child("City").val() + "&nbsp;" + snap.child("Dist").val();
  })
}

var tempMode = "";

function getTempMode() {
  let ref = firebase.database().ref("USERDATA").child("TempMode");
  ref.once("value", snap => {
    tempMode = snap.val();
  })
}

function drawTemp(avg) {
  let value = parseInt(avg, 10);
  let length = 0;
  let offset = 0;

  if (value < 0) {
    length = 5;
  } else if (value > 40) {
    length = 95;
  } else {
    length = Math.round((value * 90 / 40) + 5);
  }
  offset = 100 - length;
  return "position:relative;left:" + (length + 1) + "%;width:" + Math.round(offset) + "%;";
}

function checkUnit(value) {
  if (tempMode == "F") {
    value = value * 9 / 5 + 32;
  }
  return Math.round(value);
}

function getWeather() {
  let refDay1 = firebase.database().ref("WEATHER/Day1");
  let refDay2 = firebase.database().ref("WEATHER/Day2");
  let refDay3 = firebase.database().ref("WEATHER/Day3");
  let refDay4 = firebase.database().ref("WEATHER/Day4");
  let refDay5 = firebase.database().ref("WEATHER/Day5");
  let refDay6 = firebase.database().ref("WEATHER/Day6");
  let refDay7 = firebase.database().ref("WEATHER/Day7");
  let week = "";
  let date = "";
  let wx = "";
  let temp = "";
  let pop = "";
  let uvi = "";
  let aqi = "";
  let ws = "";

  let weekday = new Array(7);
  weekday[0] = "Sunday";
  weekday[1] = "Monday";
  weekday[2] = "Tuesday";
  weekday[3] = "Wednesday";
  weekday[4] = "Thursday";
  weekday[5] = "Friday";
  weekday[6] = "Saturday";

  refDay1.on("value", day1Snap => {
    date = day1Snap.child("Date").val();
    date = new Date(date + " 00:00:00");
    week = date.getDay();
    date = weekday[week] + ",&nbsp;" + String(date).slice(4, 10);
    document.getElementById("dateToday").innerHTML = date;
    document.getElementById("dateDay1").innerHTML = String(date).slice(0, 3);
    wx = day1Snap.child("Wx").val();
    document.getElementById("wxToday").src = getWxIcon(wx);
    document.getElementById("wxDay1").src = getWxIcon(wx);

    temp = day1Snap.child("Temp").val().split(",");
    document.getElementById("tempToday").innerHTML = checkUnit(temp[1]) + "<sup style=font-size:32px;>°</sup>";
    document.getElementById("drawTempDay1").style = drawTemp(temp[1], tempMode);
    document.getElementById("minTempDay1").innerHTML = checkUnit(temp[0]) + "<sup>°" + tempMode + "</sup>";
    document.getElementById("maxTempDay1").innerHTML = checkUnit(temp[2]) + "<sup>°" + tempMode + "</sup>";

    pop = day1Snap.child("Pop").val();
    document.getElementById("popToday").innerHTML = "&nbsp;" + pop + "%";
    document.getElementById("popDay1").innerHTML = pop + "%";

    uvi = day1Snap.child("Uvi").val();
    document.getElementById("uviToday").innerHTML = "&nbsp;" + uvi;

    aqi = day1Snap.child("Aq").val();
    document.getElementById("aqiToday").innerHTML = "&nbsp;" + aqi;

    ws = day1Snap.child("Ws").val();
    document.getElementById("wsToday").innerHTML = "&nbsp;" + ws + "m/s";
  })

  refDay2.on("value", day2Snap => {
    date = day2Snap.child("Date").val();
    date = new Date(date + " 00:00:00");
    week = date.getDay();
    date = weekday[week] + ",&nbsp;" + String(date).slice(4, 10);
    document.getElementById("dateDay2").innerHTML = String(date).slice(0, 3);
    wx = day2Snap.child("Wx").val();
    document.getElementById("wxDay2").src = getWxIcon(wx);

    temp = day2Snap.child("Temp").val().split(",");
    document.getElementById("drawTempDay2").style = drawTemp(temp[1], tempMode);
    document.getElementById("minTempDay2").innerHTML = checkUnit(temp[0]) + "<sup>°" + tempMode + "</sup>";
    document.getElementById("maxTempDay2").innerHTML = checkUnit(temp[2]) + "<sup>°" + tempMode + "</sup>";

    pop = day2Snap.child("Pop").val();
    document.getElementById("popDay2").innerHTML = pop + "%";
  })

  refDay3.on("value", day3Snap => {
    date = day3Snap.child("Date").val();
    date = new Date(date + " 00:00:00");
    week = date.getDay();
    date = weekday[week] + ",&nbsp;" + String(date).slice(4, 10);
    document.getElementById("dateDay3").innerHTML = String(date).slice(0, 3);
    wx = day3Snap.child("Wx").val();
    document.getElementById("wxDay3").src = getWxIcon(wx);

    temp = day3Snap.child("Temp").val().split(",");
    document.getElementById("drawTempDay3").style = drawTemp(temp[1], tempMode);
    document.getElementById("minTempDay3").innerHTML = checkUnit(temp[0]) + "<sup>°" + tempMode + "</sup>";
    document.getElementById("maxTempDay3").innerHTML = checkUnit(temp[2]) + "<sup>°" + tempMode + "</sup>";

    pop = day3Snap.child("Pop").val();
    document.getElementById("popDay3").innerHTML = pop + "%";
  })

  refDay4.on("value", day4Snap => {
    date = day4Snap.child("Date").val();
    date = new Date(date + " 00:00:00");
    week = date.getDay();
    date = weekday[week] + ",&nbsp;" + String(date).slice(4, 10);
    document.getElementById("dateDay4").innerHTML = String(date).slice(0, 3);
    wx = day4Snap.child("Wx").val();
    document.getElementById("wxDay4").src = getWxIcon(wx);

    temp = day4Snap.child("Temp").val().split(",");
    document.getElementById("drawTempDay4").style = drawTemp(temp[1], tempMode);
    document.getElementById("minTempDay4").innerHTML = checkUnit(temp[0]) + "<sup>°" + tempMode + "</sup>";
    document.getElementById("maxTempDay4").innerHTML = checkUnit(temp[2]) + "<sup>°" + tempMode + "</sup>";

    pop = day4Snap.child("Pop").val();
    document.getElementById("popDay4").innerHTML = pop + "%";
  })

  refDay5.on("value", day5Snap => {
    date = day5Snap.child("Date").val();
    date = new Date(date + " 00:00:00");
    week = date.getDay();
    date = weekday[week] + ",&nbsp;" + String(date).slice(4, 10);
    document.getElementById("dateDay5").innerHTML = String(date).slice(0, 3);
    wx = day5Snap.child("Wx").val();
    document.getElementById("wxDay5").src = getWxIcon(wx);

    temp = day5Snap.child("Temp").val().split(",");
    document.getElementById("drawTempDay5").style = drawTemp(temp[1], tempMode);
    document.getElementById("minTempDay5").innerHTML = checkUnit(temp[0]) + "<sup>°" + tempMode + "</sup>";
    document.getElementById("maxTempDay5").innerHTML = checkUnit(temp[2]) + "<sup>°" + tempMode + "</sup>";

    pop = day5Snap.child("Pop").val();
    document.getElementById("popDay5").innerHTML = pop + "%";
  })

  refDay6.on("value", day6Snap => {
    date = day6Snap.child("Date").val();
    date = new Date(date + " 00:00:00");
    week = date.getDay();
    date = weekday[week] + ",&nbsp;" + String(date).slice(4, 10);
    document.getElementById("dateDay6").innerHTML = String(date).slice(0, 3);
    wx = day6Snap.child("Wx").val();
    document.getElementById("wxDay6").src = getWxIcon(wx);

    temp = day6Snap.child("Temp").val().split(",");
    document.getElementById("drawTempDay6").style = drawTemp(temp[1], tempMode);
    document.getElementById("minTempDay6").innerHTML = checkUnit(temp[0]) + "<sup>°" + tempMode + "</sup>";
    document.getElementById("maxTempDay6").innerHTML = checkUnit(temp[2]) + "<sup>°" + tempMode + "</sup>";

    pop = day6Snap.child("Pop").val();
    document.getElementById("popDay6").innerHTML = pop + "%";
  })

  refDay7.on("value", day7Snap => {
    date = day7Snap.child("Date").val();
    date = new Date(date + " 00:00:00");
    week = date.getDay();
    date = weekday[week] + ",&nbsp;" + String(date).slice(4, 10);
    document.getElementById("dateDay7").innerHTML = String(date).slice(0, 3);
    wx = day7Snap.child("Wx").val();
    document.getElementById("wxDay7").src = getWxIcon(wx);

    temp = day7Snap.child("Temp").val().split(",");
    document.getElementById("drawTempDay7").style = drawTemp(temp[1], tempMode);
    document.getElementById("minTempDay7").innerHTML = checkUnit(temp[0]) + "<sup>°" + tempMode + "</sup>";
    document.getElementById("maxTempDay7").innerHTML = checkUnit(temp[2]) + "<sup>°" + tempMode + "</sup>";

    pop = day7Snap.child("Pop").val();
    document.getElementById("popDay7").innerHTML = pop + "%";
  })
}

// radar and satellite image
var slideIndexWeatherImg = 1;
showSlidesWeatherImg(slideIndexWeatherImg);

function plusSlidesWeatherImg(n) {
  showSlidesWeatherImg(slideIndexWeatherImg += n);
}

function showSlidesWeatherImg(n) {
  let slidesWeatherImg = document.getElementsByClassName("slideWeatherImg");
  if (n > slidesWeatherImg.length) {
    slideIndexWeatherImg = slidesWeatherImg.length;
  }
  if (n < 1) {
    slideIndexWeatherImg = 1;
  }
  if (slideIndexWeatherImg == 1) {
    slidesWeatherImg[0].style.display = "block";
    slidesWeatherImg[1].style.display = "none";
  } else {
    slidesWeatherImg[1].style.display = "block";
    slidesWeatherImg[0].style.display = "none";
  }
}

getImage();
getUserLoc();
getTempMode();
getWeather();

function checkDefault() {
  firebase.database().ref("USERDATA/WalkMode").once("value", snap => {
    if (snap.val() == "control") {
      firebase.database().ref("USERDATA").update({
        WalkMode: "auto"
      }).then(() => {
        console.log('change nemo walking mode to auto successful');
      });
    }
  })
}