var example = document.getElementById("example"), ctx = example.getContext('2d');
var mouse = { x:0, y:0};
example.height = 680;
example.width  = 1150;
var y_offset = 10;
var x_offset = 10;
DrawScheme();
function DrawScheme(){
    ctx.beginPath();
    ctx.moveTo(0+x_offset, 30+y_offset);
    ctx.lineTo(1050+x_offset, 30+y_offset);
    ctx.moveTo(0+x_offset, 180+y_offset);
    ctx.lineTo(1050+x_offset, 180+y_offset);
    ctx.moveTo(0+x_offset, 330+y_offset);
    ctx.lineTo(1050+x_offset, 330+y_offset);
    ctx.moveTo(1050+x_offset, 30+y_offset);
    ctx.lineTo(1050+x_offset, 480+y_offset);
    ctx.stroke();
    
    
    ctx.beginPath();
    ctx.roundRect(0+x_offset, 75+y_offset, 950, 60, [30, 30, 30, 30]);
    ctx.roundRect(0+x_offset, 225+y_offset, 950, 60, [30, 30, 30, 30]);
    ctx.fillStyle = "#a0a0a0";
    ctx.shadowOffsetY = 1;
    ctx.shadowColor = "#111111";
    ctx.shadowBlur = 10;
    ctx.fill();
    
    ctx.beginPath();
    ctx.moveTo(750+x_offset, 30+y_offset);
    ctx.arc(750+x_offset, 30+y_offset, 30, 0, Math.PI * 2, true);
    ctx.moveTo(750+x_offset, 180+y_offset);
    ctx.arc(750+x_offset, 180+y_offset, 30, 0, Math.PI * 2, true);
    ctx.moveTo(750+x_offset, 330+y_offset);
    ctx.arc(750+x_offset, 330+y_offset, 30, 0, Math.PI * 2, true);
    
    ctx.moveTo(1050+x_offset, 30+y_offset);
    ctx.arc(1050+x_offset, 30+y_offset, 30, 0, Math.PI * 2, true);
    ctx.moveTo(1050+x_offset, 180+y_offset);
    ctx.arc(1050+x_offset, 180+y_offset, 30, 0, Math.PI * 2, true);
    ctx.moveTo(1050+x_offset, 330+y_offset);
    ctx.arc(1050+x_offset, 330+y_offset, 30, 0, Math.PI * 2, true);
    ctx.moveTo(1050+x_offset, 480+y_offset);
    ctx.arc(1050+x_offset, 480+y_offset, 30, 0, Math.PI * 2, true);
    
    ctx.moveTo(300+x_offset, 30+y_offset);
    ctx.arc(300+x_offset, 30+y_offset, 30, 0, Math.PI * 2, true);
    ctx.moveTo(330+x_offset, 180+y_offset);
    ctx.arc(300+x_offset, 180+y_offset, 30, 0, Math.PI * 2, true);
    ctx.moveTo(135+x_offset, 330+y_offset);
    ctx.arc(300+x_offset, 330+y_offset, 30, 0, Math.PI * 2, true);
    
    
    ctx.moveTo(60+x_offset, 105+y_offset);
    ctx.arc(30+x_offset, 105+y_offset, 30, 0, Math.PI * 2, true);
    ctx.moveTo(505+x_offset, 105+y_offset);
    ctx.arc(475+x_offset, 105+y_offset, 30, 0, Math.PI * 2, true);
    ctx.moveTo(60+x_offset, 255+y_offset);
    ctx.arc(30+x_offset, 255+y_offset, 30, 0, Math.PI * 2, true);
    ctx.moveTo(505+x_offset, 255+y_offset);
    ctx.arc(475+x_offset, 255+y_offset, 30, 0, Math.PI * 2, true);
    ctx.fillStyle = "white";
    ctx.shadowOffsetX = 2;
    ctx.shadowOffsetY = 2;
    ctx.shadowColor = "#111111";
    ctx.shadowBlur = 10;
    ctx.fill();
}
var arrayOfObjects = [
    { id: 'John', x: 30, y: 30 },
    { id: 'Alice', x: 25, y: 30 },
    { id: 'Bob', x: 35, y: 30 },
];
function addElementsFromArray(arrayOfObjects) {
    var scheme = document.getElementById('scheme');

    arrayOfObjects.forEach(function (object) {
        var forklyft = document.createElement('div');
        forklyft.textContent = object.id;
        forklyft.setAttribute('class', 'customElement');
        forklyft.setAttribute('id', object.id);
        forklyft.setAttribute('onclick', 'showElementId(this)');
        forklyft.style.top =`${object.x-x_offset}px`;
        forklyft.style.left =`${object.y-y_offset}px`;

        var forklyft_dashboard = document.createElement('div');
        forklyft_dashboard.setAttribute('class', 'forklyft_dashboard');
        forklyft_dashboard.setAttribute('id', `dashboard_${object.id}`);

        var dashboard_label = document.createElement('div');
        dashboard_label.setAttribute('class', 'dashboard_label');
        dashboard_label.textContent = "dashboard_label";

        var dashboard_row_1 = document.createElement('div');
        dashboard_row_1.setAttribute('class', 'dashboard_row');
        dashboard_row_1.textContent = "dashboard_row";

        var dashboard_row_2 = document.createElement('div');
        dashboard_row_2.setAttribute('class', 'dashboard_row');
        dashboard_row_2.textContent = "dashboard_row";

        var dashboard_row_3 = document.createElement('div');
        dashboard_row_3.setAttribute('class', 'dashboard_row');
        dashboard_row_3.textContent = "dashboard_row";

        var dashboard_row_4 = document.createElement('div');
        dashboard_row_4.setAttribute('class', 'dashboard_row');
        dashboard_row_4.textContent = "dashboard_row";

        forklyft_dashboard.appendChild(dashboard_label);
        forklyft_dashboard.appendChild(dashboard_row_1);
        forklyft_dashboard.appendChild(dashboard_row_2);
        forklyft_dashboard.appendChild(dashboard_row_3);
        forklyft_dashboard.appendChild(dashboard_row_4);
        forklyft.appendChild(forklyft_dashboard);
        scheme.appendChild(forklyft);
    });
}
function showElementId(clickedElement) {
    var elem = document.getElementById(`dashboard_${clickedElement.id}`);
    if(elem.style.display == 'none'){
        elem.style.display = 'block';
    }
    else{
        elem.style.display = 'none';
    }
    
}
var arrayOfObjects = [
    { id: '(0, 0)', x: 30, y: 0 },
    { id: '(0, 1)', x: 180, y: 600 },
    { id: '(0, 2)', x:330, y: 800 }
];

addElementsFromArray(arrayOfObjects);


var CheckPoints = [
    { point: 'K1', x: 180, y: 600 },
    { point: 'K2', x: 180, y: 30 },
    { point: 'K3', x: 3, y: 0 },
    { point: 'K4', x: 4, y: 0 },
    { point: 'K5', x: 5, y: 0 },
    { point: 'K6', x: 6, y: 0 },
    { point: 'K7', x: 7, y: 0 },
    { point: 'K8', x: 8, y: 0 },
    { point: 'K9', x: 9, y: 0 },
    { point: 'K10', x: 10, y: 0 }
];
var lyft_id_, _x, _y;
GetCheckPoint(CheckPoints, '(0, 0)', 'K1');
function GetCheckPoint(arrayOfObjects, lyft_id, point_name){
    arrayOfObjects.forEach(function (object) {
        if(point_name==object.point){
            lyft_id_ = lyft_id;
            _x=object.x;
            _y=object.y;
            animation(lyft_id, object.x, object.y);
        }
    });
}

var rectX =0;
var rectY =0;

function animation(id, x, y) {
    var elem = document.getElementById(id);
    if(parseInt(elem.style.left)<=x){
        rectX += 1;
    }
    if(parseInt(elem.style.top)>x){
        rectX -= 1;
    }
    if(parseInt(elem.style.left)>y){
        rectY -= 1;
    }
    if(parseInt(elem.style.left)<=y){
        rectY += 1;
    }
    //move();
    elem.style.left = rectX+'px';
    elem.style.top = rectY+'px';
    elem.textContent = rectY;
    setTimeout(animation, 10, lyft_id_, _x, _y);
}
var request = '{"(0, 0)": "K6", "(0, 1)": "K6", "(0, 2)": "K6", "(1, 0)": "K1", "(1, 1)": "K3", "(1, 2)": "K3", "(2, 0)": "K1", "(2, 1)": "K1", "(2, 2)": "K2", "(3, 0)": "K10", "(3, 1)": "K9", "(3, 2)": "K3", "(4, 0)": "K9", "(4, 1)": "K5", "(4, 2)": "K10", "(5, 0)": "K6", "(5, 1)": "K6", "(5, 2)": "K1", "(6, 0)": "K2", "(6, 1)": "K3", "(6, 2)": "K3", "(7, 0)": "K6", "(7, 1)": "K1", "(7, 2)": "K6", "(8, 0)": "K2", "(8, 1)": "K3", "(8, 2)": "K3", "(9, 0)": "K5", "(9, 1)": "K6", "(9, 2)": "K6", "(10, 0)": "K1", "(10, 1)": "K6", "(10, 2)": "K6", "(11, 0)": "K1", "(11, 1)": "K9", "(11, 2)": "K9", "(12, 0)": "K3", "(12, 1)": "K2", "(12, 2)": "K1", "(13, 0)": "K2", "(13, 1)": "K3", "(13, 2)": "K5", "(14, 1)": "K5", "(14, 2)": "K10"}';
/*function Socket(){
    const socket = new WebSocket("ws://75.119.142.124:8002/ws2");
    socket.timeout = 0; // Без timeout
    // Открываем соединение
    socket.onopen = (event) => {
        console.log("Соединение открыто");
    };
    // Обработка данных, полученных от сервера
    socket.onmessage = (event) => {
        console.log(event.data)
        request = event.data;
        const messageElement = document.getElementById("message");
        messageElement.innerHTML = "Получено сообщение от сервера: " + event.data;
    };
    // Обработка закрытия соединения
    socket.onclose = (event) => {
        if (event.wasClean) {
            console.log(`Соединение закрыто, код: ${event.code}, причина: ${event.reason}`);
        } else {
            console.error("Соединение прервано");
        }
    };
    // Обработка ошибок
    socket.onerror = (error) => {
        console.error("Ошибка при соединении:", error);
    };
}*/
function JSONParser(){
    var obj = JSON.parse(request);
}