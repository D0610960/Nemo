var sidebar = document.getElementById("sidebar");

function openSide() {
    if (sidebar.style.display == 'block') {
        sidebar.style.display = 'none';
    } else {
        sidebar.style.display = 'block';
    }
}

function closeSide() {
    sidebar.style.display = "none";
}

var ref = firebase.database().ref("USERDATA");

/* citys */
var citys_en = ["Keelung City", "New Taipei City", "Taipei City", "Yilan County", "Taoyuan City",
    "Hsinchu City", "Hsinchu County", "Miaoli County", "Taichung City", "Changhua County",
    "Nantou County", "Yunlin County", "Chiayi City", "Chiayi County", "Tainan City", "Kaohsiung City",
    "Pingtung County", "Taitung County", "Hualien County", "Penghu County", "Kinmen County",
    "Lienchiang County"
];
var citys_ch = ["基隆市", "新北市", "臺北市", "宜蘭縣", "桃園市", "新竹市", "新竹縣", "苗栗縣", "臺中市",
    "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣", "臺南市", "高雄市", "屏東縣", "臺東縣", "花蓮縣",
    "澎湖縣", "金門縣", "連江縣"
];

/* dists */
var dists_en = new Array();
dists_en[0] = ["Anle Dist.", "Zhongshan Dist.", "Zhongzheng Dist.", "Qidu Dist.", "Xinyi Dist.",
    "Ren&apos;ai Dist.", "Nuannuan Dist."
];
dists_en[1] = ["Shimen Dist.", "Sanzhi Dist.", "Jinshan Dist.", "Tamsui Dist.", "Wanli Dist.", "Bali Dist.",
    "Xizhi Dist.", "Linkou Dist.", "Wugu Dist.", "Ruifang Dist.", "Luzhou Dist.", "Shuangxi Dist.",
    "Sanchong Dist.", "Gongliao Dist.", "Pingxi Dist.", "Taishan Dist.", "Xinzhuang Dist.", "Shiding Dist.",
    "Banqiao Dist.", "Shenkeng Dist.", "Yonghe Dist.", "Shulin Dist.", "Zhonghe Dist.", "Tucheng Dist.",
    "Xindian Dist.", "Pinglin Dist.", "Yingge Dist.", "Sanxia Dist.", "Wulai Dist."
];
dists_en[2] = ["Beitou Dist.", "Shilin Dist.", "Neihu Dist.", "Zhongshan Dist.", "Datong Dist.",
    "Songshan Dist.", "Nangang Dist.", "Zhongzheng Dist.", "Wanhua Dist.", "Xinyi Dist.",
    "Da&apos;an Dist.", "Wenshan Dist."
];
dists_en[3] = ["Toucheng Township", "Jiaoxi Township", "Zhuangwei Township", "Yuanshan Township",
    "Yilan City", "Datong Township", "Wujie Township", "Sanxing Township", "Luodong Township",
    "Dongshan Township", "Nan&apos;ao Township", "Su&apos;ao Township"
];
dists_en[4] = ["Dayuan Dist.", " Luzhu Dist.", " Guanyin Dist.", " Guishan Dist.", " Taoyuan Dist.",
    " Zhongli Dist.", " Xinwu Dist.", " Bade Dist.", " Pingzhen Dist.", " Yangmei Dist.", " Dasi Dist.",
    " Longtan Dist.", " Fuxing Dist."
]
dists_en[5] = ["North Dist.", " Xiangshan Dist.", " East Dist."];
dists_en[6] = ["Xinfeng Township", " Hukou Township", " Xinpu Township", " Zhubei City", " Guanxi Township",
    " Qionglin Township", " Zhudong Township", " Baoshan Township", " Jianshi Township",
    " Hengshan Township", " Beipu Township", " Emei Township", " Wufeng Township"
];
dists_en[7] = ["Zhunan Township", "Toufen Township", "Sanwan Township", "Zaoqiao Township",
    "Houlong Township",
    "Nanzhuang Township", "Touwu Township", "Shitan Township", "Miaoli City", "Xihu Township",
    "Tongxiao Township", "Gongguan Township", "Tongluo Township", "Tai&apos;an Township", "Yuanli Township",
    "Dahu Township", "Sanyi Township", "Zhuolan Township"
];
dists_en[8] = ["Beitun Dist.", "Xitun Dist.", "North Dist.", "Nantun Dist.", "West Dist.", "East Dist.",
    "Central Dist.", "South Dist.", "Heping Dist.", "Dajia Dist.", "Da&apos;an Dist.", "Waipu Dist.",
    "Houli Dist.", "Qingshui Dist.", "Dongshi Dist.", "Shengang Dist.", "Longjing Dist.", "Shigang Dist.",
    "Fengyuan Dist.", "Wuqi Dist.", "Xinshe Dist.", "Shalu Dist.", "Daya Dist.", "Tanzi Dist.",
    "Dadu Dist.", "Taiping Dist.", "Wuri Dist.", "Dali Dist.", "Wufeng Dist."
];
dists_en[9] = ["Shengang Township", "Hemei Township", "Xianxi Township", "Lukang Township", "Changhua City",
    "Xiushui Township", "Fuxing Township", "Huatan Township", "Fenyuan Township", "Fangyuan Township",
    "Puyan Township", "Dacun Township", "Erlin Township", "Yuanlin Township", "Xihu Township",
    "Puxin Township", "Yongjing Township", "Shetou Township", "Pitou Township", "Tianwei Township",
    "Dacheng Township", "Tianzhong Township", "Beidou Township", "Zhutang Township", "Xizhou Township",
    "Ershui Township"
];
dists_en[10] = ["Ren&apos;ai Township", "Guoxing Township", "Puli Township", "Caotun Township",
    "Zhongliao Township", "Nantou City", "Yuchi Township", "Shuili Township", "Mingjian Township",
    "Xinyi Township", "Jiji Township", "Zhushan Township", "Lugu Township"
];
dists_en[11] = ["Mailiao Township", "Erlun Township", "Lunbei Township", "Xiluo Township", "Citong Township",
    "Linnei Township", "Taixi Township", "Tuku Township", "Huwei Township", "Baozhong Township",
    "Dongshi Township", "Dounan Township", "Sihu Township", "Gukeng Township", "Yuanchang Township",
    "Dapi Township", "Kouhu Township", "Beigang Township", "Shuilin Township", "Douliu City"
];
dists_en[12] = ["East Dist.", "West Dist."];
dists_en[13] = ["Dalin Township", "Xikou Township", "Alishan Township", "Meishan Township",
    "Xingang Township", "Minxiong Township", "Liujiao Township", "Zhuqi Township", "Dongshi Township",
    "Taibao City", "Fanlu Township", "Puzi City", "Shuishang Township", "Zhongpu Township",
    "Budai Township", "Lucao Township", "Yizhu Township", "Dapu Township"
];
dists_en[14] = ["Annan Dist.", "West Central Dist.", "Anping Dist.", "East Dist.", "South Dist.",
    "North Dist.", "Baihe Dist.", "Houbi Dist.", "Yanshui Dist.", "Xinying Dist.", "Dongshan Dist.",
    "Beimen Dist.", "Liuying Dist.", "Xuejia Dist.", "Xiaying Dist.", "Liujia Dist.", "Nanhua Dist.",
    "Jiangjun Dist.", "Nanxi Dist.", "Madou Dist.", "Guantian Dist.", "Jiali Dist.", "Danei Dist.",
    "Qigu Dist.", "Yujing Dist.", "Shanhua Dist.", "Xigang Dist.", "Shanshang Dist.", "Anding Dist.",
    "Xinshi Dist.", "Zuozhen Dist.", "Xinhua Dist.", "Yongkang Dist.", "Guiren Dist.", "Guanmiao Dist.",
    "Longqi Dist.", "Rende Dist."
];
dists_en[15] = ["Nanzi Dist.", "Zuoying Dist.", "Sanmin Dist.", "Gushan Dist.", "Lingya Dist.",
    "Xinxing Dist.", "Qianjin Dist.", "Yancheng Dist.", "Qianzhen Dist.", "Qijin Dist.", "Xiaogang Dist.",
    "Namaxia Dist.", "Jiaxian Dist.", "Liugui Dist.", "Shanlin Dist.", "Neimen Dist.", "Maolin Dist.",
    "Meinong Dist.", "Qishan Dist.", "Tianliao Dist.", "Hunei Dist.", "Qieding Dist.", "Alian Dist.",
    "Luzhu Dist.", "Yong&apos;an Dist.", "Gangshan Dist.", "Yanchao Dist.", "Mituo Dist.", "Qiaotou Dist.",
    "Dashu Dist.", "Ziguan Dist.", "Dashe Dist.", "Renwu Dist.", "Niaosong Dist.", "Daliao Dist.",
    "Fengshan Dist.", "Linyuan Dist.", "Taoyuan Dist."
];
dists_en[16] = ["Gaoshu Township", "Ligang Township", "Yanpu Township", "Jiuru Township", "Changzhi Township",
    "Majia Township", "Pingtung City", "Neipu Township", "Linluo Township", "Taiwu Township",
    "Wanluan Township", "Zhutian Township", "Wandan Township", "Laiyi Township", "Chaozhou Township",
    "Xinyuan Township", "Kanding Township", "Xinpi Township", "Nanzhou Township", "Donggang Township",
    "Linbian Township", "Jiadong Township", "Chunri Township", "Shizi Township", "Liuqiu Township",
    "Fangshan Township", "Mudan Township", "Manzhou Township", "Checheng Township", "Hengchun Township",
    "Fangliao Township", "Sandimen Township", "Wutai Township"
];
dists_en[17] = ["Changbin Township", "Haiduan Township", "Chishang Township", "Chenggong Township",
    "Guanshan Township", "Donghe Township", "Luye Township", "Yanping Township", "Beinan Township",
    "Taitung City", "Taimali Township", "Ludao Township", "Daren Township", "Dawu Township",
    "Lanyu Township", "Jinfeng Township"
];
dists_en[18] = ["Xiulin Township", "Xincheng Township", "Hualien City", "Ji&apos;an Township",
    "Shoufeng Township", "Wanrong Township", "Fenglin Township", "Fengbin Township", "Guangfu Township",
    "Zhuoxi Township", "Ruisui Township", "Yuli Township", "Fuli Township"
];
dists_en[19] = ["Baisha Township", "Xiyu Township", "Huxi Township", "Magong City", "Wang&apos;an Township",
    "Qimei Township"
];
dists_en[20] = ["Jincheng Township", "Jinhu Township", "Jinsha Township", "Jinning Township",
    "Lieyu Township", "Wuqiu Township"
];
dists_en[21] = ["Nangan Township", "Beigan Township", "Jyuguang Township", "Dongyin Township"];

var dists_ch = new Array();
dists_ch[0] = ["安樂區", "中山區", "中正區", "七堵區", "信義區", "仁愛區", "暖暖區"];
dists_ch[1] = ["石門區", "三芝區", "金山區", "淡水區", "萬里區", "八里區", "汐止區", "林口區", " 五股區",
    "瑞芳區", "蘆洲區", "雙溪區", "三重區", "貢寮區", "平溪區", "泰山區", " 新莊區", "石碇區", "板橋區",
    "深坑區", "永和區", "樹林區", "中和區", "土城區", " 新店區", "坪林區", "鶯歌區", "三峽區", "烏來區"
];
dists_ch[2] = ["北投區", "士林區", "內湖區", "中山區", "大同區", "松山區", "南港區", "中正區", " 萬華區",
    "信義區", "大安區", "文山區"
];
dists_ch[3] = ["頭城鎮", "礁溪鄉", "壯圍鄉", "員山鄉", "宜蘭市", "大同鄉", "五結鄉", "三星鄉", "羅東鎮",
    "冬山鄉", "南澳鄉", "蘇澳鎮"
];
dists_ch[4] = ["大園區", "蘆竹區", "觀音區", "龜山區", "桃園區", "中壢區", "新屋區", "八德區", " 平鎮區",
    "楊梅區", "大溪區", "龍潭區", "復興區"
]
dists_ch[5] = ["北區", "香山區", "東區"];
dists_ch[6] = ["新豐鄉", "湖口鄉", "新埔鎮", "竹北市", "關西鎮", "芎林鄉", "竹東鎮", "寶山鄉", " 尖石鄉",
    "橫山鄉", "北埔鄉", "峨眉鄉", "五峰鄉"
];
dists_ch[7] = ["竹南鎮", "頭份市", "三灣鄉", "造橋鄉", "後龍鎮", "南庄鄉", "頭屋鄉", "獅潭鄉", " 苗栗市",
    "西湖鄉", "通霄鎮", "公館鄉", "銅鑼鄉", "泰安鄉", "苑裡鎮", "大湖鄉", " 三義鄉", "卓蘭鎮"
];
dists_ch[8] = ["北屯區", "西屯區", "北區", "南屯區", "西區", "東區", "中區", "南區", "和平區", "大甲區",
    "大安區", "外埔區", "后里區", "清水區", "東勢區", "神岡區", "龍井區", "石岡區", "豐原區", "梧棲區",
    "新社區", "沙鹿區", "大雅區", "潭子區", "大肚區", "太平區", "烏日區", "大里區", "霧峰區"
];
dists_ch[9] = ["伸港鄉", "和美鎮", "線西鄉", "鹿港鎮", "彰化市", "秀水鄉", "福興鄉", "花壇鄉", " 芬園鄉",
    "芳苑鄉", "埔鹽鄉", "大村鄉", "二林鎮", "員林市", "溪湖鎮", "埔心鄉", " 永靖鄉", "社頭鄉", "埤頭鄉",
    "田尾鄉", "大城鄉", "田中鎮", "北斗鎮", "竹塘鄉", " 溪州鄉", "二水鄉"
];
dists_ch[10] = ["仁愛鄉", "國姓鄉", "埔里鎮", "草屯鎮", "中寮鄉", "南投市", "魚池鄉", "水里鄉", " 名間鄉",
    "信義鄉", "集集鎮", "竹山鎮", "鹿谷鄉"
];
dists_ch[11] = ["麥寮鄉", "二崙鄉", "崙背鄉", "西螺鎮", "莿桐鄉", "林內鄉", "臺西鄉", "土庫鎮", " 虎尾鎮",
    "褒忠鄉", "東勢鄉", "斗南鎮", "四湖鄉", "古坑鄉", "元長鄉", "大埤鄉", " 口湖鄉", "北港鎮", "水林鄉", "斗六市"
];
dists_ch[12] = ["東區", "西區"];
dists_ch[13] = ["大林鎮", "溪口鄉", "阿里山鄉", "梅山鄉", "新港鄉", "民雄鄉", "六腳鄉", "竹崎鄉", "東石鄉",
    "太保市", "番路鄉", "朴子市", "水上鄉", "中埔鄉", "布袋鎮", "鹿草鄉", "義竹鄉", "大埔鄉"
];
dists_ch[14] = ["安南區", "中西區", "安平區", "東區", "南區", "北區", "白河區", "後壁區", "鹽水區", "新營區",
    "東山區", "北門區", "柳營區", "學甲區", "下營區", "六甲區", "南化區", " 將軍區", "楠西區", "麻豆區",
    "官田區", "佳里區", "大內區", "七股區", "玉井區", " 善化區", "西港區", "山上區", "安定區", "新市區",
    "左鎮區", "新化區", "永康區", "歸仁區", "關廟區", "龍崎區", "仁德區"
];
dists_ch[15] = ["楠梓區", "左營區", "三民區", "鼓山區", "苓雅區", "新興區", "前金區", "鹽埕區", "前鎮區",
    "旗津區", "小港區", "那瑪夏區", "甲仙區", "六龜區", "杉林區", "內門區", "茂林區", "美濃區", "旗山區",
    "田寮區", "湖內區", "茄萣區", "阿蓮區", "路竹區", "永安區", "岡山區", "燕巢區", "彌陀區", "橋頭區",
    "大樹區", "梓官區", "大社區", "仁武區", "鳥松區", "大寮區", "鳳山區", "林園區", "桃源區"
];
dists_ch[16] = ["高樹鄉", "三地門鄉", "霧臺鄉", "里港鄉", "鹽埔鄉", "九如鄉", "長治鄉", "瑪家鄉", "屏東市",
    "內埔鄉", "麟洛鄉", "泰武鄉", "萬巒鄉", "竹田鄉", "萬丹鄉", "來義鄉", "潮州鎮", "新園鄉", "崁頂鄉",
    "新埤鄉", "南州鄉", "東港鎮", "林邊鄉", "佳冬鄉", "春日鄉", "獅子鄉", "琉球鄉", "枋山鄉", "牡丹鄉",
    "滿州鄉", "車城鄉", "恆春鎮", "枋寮鄉"
];
dists_ch[17] = ["長濱鄉", "海端鄉", "池上鄉", "成功鎮", "關山鎮", "東河鄉", "鹿野鄉", "延平鄉", "卑南鄉",
    "臺東市", "太麻里鄉", "綠島鄉", "達仁鄉", "大武鄉", "蘭嶼鄉", "金峰鄉"
];
dists_ch[18] = ["秀林鄉", "新城鄉", "花蓮市", "吉安鄉", "壽豐鄉", "萬榮鄉", "鳳林鎮", "豐濱鄉", "光復鄉",
    "卓溪鄉", "瑞穗鄉", "玉里鎮", "富里鄉"
];
dists_ch[19] = ["白沙鄉", "西嶼鄉", "湖西鄉", "馬公市", "望安鄉", "七美鄉"];
dists_ch[20] = ["金城鎮", "金湖鎮", "金沙鎮", "金寧鄉", "烈嶼鄉", "烏坵鄉"];
dists_ch[21] = ["南竿鄉", "北竿鄉", "莒光鄉", "東引鄉"];

function defaultLoc() {
    var innerCity = "";
    ref.child("City").once("value", snap => {
        for (var i = 0; i < citys_ch.length; i++) {
            if (citys_ch[i] == snap.val()) {
                innerCity += "<option value=\"" + citys_ch[i] + "\" selected>" + citys_ch[i] +
                    "&nbsp;" + citys_en[i] + "</option>";
            } else {
                innerCity += "<option value=\"" + citys_ch[i] + "\">" + citys_ch[i] + "&nbsp;" +
                    citys_en[i] + "</option>";
            }
        }
        document.getElementById("cityList").innerHTML = innerCity;
        changeCity(document.getElementById("cityList"));
    })
}

function defaultName() {
    ref.child("Nickname").on("value", snap => {
        document.getElementById("userName").value = snap.val();
    })
}

function defaultTempMode() {
    ref.child("TempMode").on("value", snap => {
        if (snap.val() == "C") {
            document.getElementById("tempMode").checked = true;
            document.getElementById("showTemp").style = "transform: translateX(-23px);";
            document.getElementById("showTemp").innerHTML = "°C";
        } else {
            document.getElementById("tempMode").checked = false;
            document.getElementById("showTemp").style = "transform: translateX(23px);";
            document.getElementById("showTemp").innerHTML = "°F";
        }
    })
}

function defaultChar() {
    ref.child("Char").on("value", snap => {
        var charbutton = document.getElementsByName("char");
        for (let i = 0; i < charbutton.length; i++) {
            if (snap.val() == charbutton[i].id) {
                charbutton[i].disabled = true;
            } else {
                charbutton[i].disabled = false;
            }
        }
    })
}

function defaultWalkMode() {
    ref.child("WalkMode").on("value", snap => {
        var walkbutton = document.getElementsByName("walk");
        for (let i = 0; i < walkbutton.length; i++) {
            if (snap.val() == walkbutton[i].id) {
                walkbutton[i].disabled = true;
            } else {
                walkbutton[i].disabled = false;
            }

            if (snap.val() == "control") {
                document.getElementById("wheel").style = "display: inline;";
            } else {
                document.getElementById("wheel").style = "display: none;";
            }
        }
    })
}

function defaultCamMode() {
    ref.on("value", snap => {
        if (snap.child("CamMode").val() == "on") {
            document.getElementById("camMode").checked = true;
            document.getElementById("showCam").style = "transform: translateX(-22px);";
            document.getElementById("showCam").innerHTML = "ON";
            document.getElementById("timedOn").style = "display: none;";
        } else {
            document.getElementById("camMode").checked = false;
            document.getElementById("showCam").style = "transform: translateX(12px);";
            document.getElementById("showCam").innerHTML = "OFF";
            document.getElementById("timedOn").style = "display: block;";

            if (snap.child("CamTimedOn").val() == "on") {
                document.getElementById("camTimedOn").checked = true;
                document.getElementById("showTimedOn").style = "transform: translateX(-22px);";
                document.getElementById("showTimedOn").innerHTML = "ON";
                document.getElementById("camStart").disabled = false;
                document.getElementById("camEnd").disabled = false;
            } else {
                document.getElementById("camTimedOn").checked = false;
                document.getElementById("showTimedOn").style = "transform: translateX(12px);";
                document.getElementById("showTimedOn").innerHTML = "OFF";
                document.getElementById("camStart").disabled = true;
                document.getElementById("camEnd").disabled = true;
            }
        }
    })
}

function defaultCamStart() {
    ref.child("CamStart").on("value", snap => {
        document.getElementById("camStart").defaultValue = snap.val();
    })
}

function defaultCamEnd() {
    ref.child("CamEnd").on("value", snap => {
        document.getElementById("camEnd").defaultValue = snap.val();
    })
}

function defaultVol() {
    let icon = "";
    ref.child("Volume").on("value", snap => {
        document.getElementById("rangeVol").value = snap.val();
        document.getElementById("volume").innerHTML = snap.val();
        if (snap.val() == 0) {
            icon = "fa fa-volume-off";
        } else if (snap.val() < 50) {
            icon = "fa fa-volume-down";
        } else {
            icon = "fa fa-volume-up";
        }
        document.getElementById("iconVol").setAttribute("class", icon);
    })
}

function changeCity(changed) {
    let index = changed.selectedIndex;
    let innerDist = "";
    ref.child("Dist").once("value", snap => {
        for (let i = 0; i < dists_ch[index].length; i++) {
            if (dists_ch[index][i] == snap.val()) {
                innerDist += "<option value=\"" + dists_ch[index][i] + "\" selected>" +
                    dists_ch[index][i] + "&nbsp;" + dists_en[index][i] + "</option>";
            } else {
                innerDist += "<option value=\"" + dists_ch[index][i] + "\">" + dists_ch[index][i] +
                    "&nbsp;" + dists_en[index][i] + "</option>";
            }
        }
        document.getElementById("distList").innerHTML = innerDist;
    })
}

function setLoc(updateCity, updateDist) {
    firebase.database().ref("USERDATA").update({
        City: updateCity.value,
        Dist: updateDist.value
    }).then(() => {
        console.log('update user location successful');
        alertStr = "Nemo現在住在" + updateCity.value + updateDist.value + "啦";
        window.AppInventor.setWebViewString("alert" + alertStr);
    });
}

function setName() {
    let name = document.getElementById("userName");
    let str = name.value.trim();
    if (name.checkValidity()) {
        firebase.database().ref("USERDATA").update({
            Nickname: str
        }).then(() => {
            console.log('update user name successful');
            alertStr = "以後就稱呼你為" + name.value + "啦~請多多指教";
            window.AppInventor.setWebViewString("alert" + alertStr);
        });
    } else {
        if(name.validity.valueMissing){
            name.setCustomValidity("告訴Nemo該怎麼稱呼你");
            name.reportValidity();
        } else if(name.validity.patternMismatch){
            name.setCustomValidity("只可以使用英文字母與半形空格喔");
            name.reportValidity();
        }
    }
}

function setTempMode() {
    let temp = document.getElementById("tempMode");
    let mode = "";
    if (temp.checked) {
        mode = "C";
        document.getElementById("showTemp").style = "transform: translateX(-35px);";
    } else {
        mode = "F";
        document.getElementById("showTemp").style = "transform: translateX(35px);";
    }
    document.getElementById("showTemp").innerHTML = "°" + mode;
    firebase.database().ref("USERDATA").update({
        TempMode: mode
    }).then(() => {
        console.log('update user temperature mode successful');
    });
}

function setChar(clicked) {
    let char = clicked.id;
    firebase.database().ref("USERDATA").update({
        Char: char
    }).then(() => {
        console.log('update nemo character successful');
        defaultChar();
    })
}

function setWalkMode(clicked) {
    let walk = clicked.id;
    firebase.database().ref("USERDATA").update({
        WalkMode: walk
    }).then(() => {
        console.log('update nemo walking mode successful');
        defaultWalkMode();
    })
}

$(function () {
    $("#wheel").click(function () {
        window.AppInventor.setWebViewString('gotoRemoteControl');
    });
    $("#member").click(function () {
        window.location="members.html";
    });
});

function setCamMode() {
    let cam = document.getElementById("camMode");
    let mode = "";
    if (cam.checked) {
        mode = "on";
        document.getElementById("showCam").style = "transform: translateX(-23px);";
    } else {
        mode = "off";
        document.getElementById("showCam").style = "transform: translateX(23px);";
    }
    document.getElementById("showCam").innerHTML = mode;
    firebase.database().ref("USERDATA").update({
        CamMode: mode
    }).then(() => {
        console.log('update camera mode successful');
    });
}

function setTimedOn() {
    let timed = document.getElementById("camTimedOn");
    let mode = "";
    if (timed.checked) {
        mode = "on";
        document.getElementById("showTimedOn").style = "transform: translateX(-23px);";
    } else {
        mode = "off";
        document.getElementById("showTimedOn").style = "transform: translateX(23px);";
    }
    document.getElementById("showTimedOn").innerHTML = mode;
    firebase.database().ref("USERDATA").update({
        CamTimedOn: mode
    }).then(() => {
        console.log('update camera timed on mode successful');
    });
}

function setCamStart(changed) {
    firebase.database().ref("USERDATA").update({
        CamStart: changed.value
    }).then(() => {
        console.log('update camera time start successful');
    });
}

function setCamEnd(changed) {
    firebase.database().ref("USERDATA").update({
        CamEnd: changed.value
    }).then(() => {
        console.log('update camera time end successful');
    });
}

function changeVol(range) {
    let icon = "";
    let val = range.value;
    document.getElementById("volume").innerHTML = val;
    if (val == 0) {
        icon = "fa fa-volume-off";
    } else if (val < 50) {
        icon = "fa fa-volume-down";
    } else {
        icon = "fa fa-volume-up";
    }
    document.getElementById("iconVol").setAttribute("class", icon);
    firebase.database().ref("USERDATA").update({
        Volume: range.value
    }).then(() => {
        console.log('update volume end successful');
    });
}

function logout() {
    window.AppInventor.setWebViewString('logout');
}

function loadDefault() {
    defaultLoc();
    defaultName();
    defaultTempMode();
    defaultWalkMode();
    defaultCamMode();
    defaultCamStart();
    defaultCamEnd();
    defaultChar();
    defaultVol();
}