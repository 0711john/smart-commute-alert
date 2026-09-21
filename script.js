// ================================
// 智慧通勤風險通知系統
// 前端資料處理
// ================================


// --------------------------------
// 目前示範資料
// 未來可以改成從 API / MySQL 取得
// --------------------------------

const commuteData = {
    temperature: 32,
    rainProbability: 45,
    aqi: 78
};


// --------------------------------
// 更新網頁資料
// --------------------------------

function updateWebsite(data) {

    // 最高溫度
    document.getElementById("temperature").textContent =
        `${data.temperature} °C`;

    // 降雨機率
    document.getElementById("rain").textContent =
        `${data.rainProbability} %`;

    // AQI
    document.getElementById("aqi").textContent =
        data.aqi;

    // 通勤建議
    const advice = createAdvice(data);

    document.getElementById("advice").innerHTML =
        advice;

    // 最後更新時間
    const now = new Date();

    document.getElementById("updateTime").textContent =
        now.toLocaleString("zh-TW");
}


// --------------------------------
// 判斷通勤建議
// --------------------------------

function createAdvice(data) {

    const advice = [];

    // 降雨機率
    if (data.rainProbability >= 60) {

        advice.push(
            "☔ 降雨機率達 60%，請記得攜帶雨傘。"
        );
    }

    // 高溫
    if (data.temperature >= 33) {

        advice.push(
            "☀️ 最高溫達 33°C，請注意防曬並適時補充水分。"
        );
    }

    // AQI
    if (data.aqi >= 100) {

        advice.push(
            "😷 AQI 達 100，空氣品質較差，建議配戴口罩。"
        );
    }

    // 所有條件正常
    if (advice.length === 0) {

        return "✅ 今日天氣與空氣品質正常，適合外出通勤。";
    }

    return advice.join("<br>");
}


// --------------------------------
// 未來 MySQL / API 使用
// --------------------------------

async function loadFromAPI() {

    /*
        未來可以把 API_URL 改成：

        const API_URL =
            "https://你的後端網址/api/latest";

        後端再負責：

        MySQL
            ↓
        API
            ↓
        JavaScript
            ↓
        網頁
    */


    // 目前先使用示範資料
    updateWebsite(commuteData);
}


// --------------------------------
// 網頁載入完成
// --------------------------------

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadFromAPI();

    }
);
