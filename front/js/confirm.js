window.onload = function () {

    function getParam(name, url) {
        if (!url) url = window.location.href;
        name = name.replace(/[\[\]]/g, "\\$&");
        let regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
            results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, " "));
    }

    let body = {
        "transactionId": getParam('transactionId'),
        "orderId": getParam('orderId')
    };
    let request = new XMLHttpRequest();
    // 決済確定API
    request.open('POST', 'https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev/confirm/', true);
    request.responseType = 'json';
    request.onload = function () {
        data = this.response;
    }
    request.send(JSON.stringify(body));
}