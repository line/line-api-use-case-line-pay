window.onload = function () {
    document.getElementById('casher').addEventListener('click', function () {
        let request = new XMLHttpRequest();
        let body = {
            "userId": "demouserid1234567890",
        };

        request.open('POST', 'https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev/reserve/', true);
        request.responseType = 'json';
        request.onload = function () {
            let data = this.response;
            let response = data.info
            // 決済画面遷移
            if (response && data.returnCode == '0000') {
                window.location.href = response.paymentUrl.web;
            } else {
                alert(`${data.returnCode}:取引エラーのため再度決済ボタンを押してください`)
            }
        };
        request.send(JSON.stringify(body));

    });

    // 画面のズーム防止
    document.documentElement.addEventListener('touchstart', function (e) {
        if (e.touches.length >= 2) {
            e.preventDefault();
        }
    }, {passive: false});

    var t = 0;
    document.documentElement.addEventListener('touchend', function (e) {
        var now = new Date().getTime();
        if ((now - t) < 400){
            e.preventDefault();
        }
        t = now;
    }, false);
}