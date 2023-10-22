var example = document.getElementById("example"), ctx = example.getContext('2d');
var mouse = { x:0, y:0};
example.height = 680;
example.width  = 1150;
var y_offset = 10;
var x_offset = 10;
var scale = 0.75;

DrawScheme();
function DrawScheme(){
    ctx.beginPath();
    ctx.moveTo(0*scale+x_offset, 30*scale+y_offset);
    ctx.lineTo(1050*scale+x_offset, 30*scale+y_offset);
    ctx.moveTo(0*scale+x_offset, 180*scale+y_offset);
    ctx.lineTo(1050*scale+x_offset, 180*scale+y_offset);
    ctx.moveTo(0*scale+x_offset, 330*scale+y_offset);
    ctx.lineTo(1050*scale+x_offset, 330*scale+y_offset);
    ctx.moveTo(1050*scale+x_offset, 30*scale+y_offset);
    ctx.lineTo(1050*scale+x_offset, 480*scale+y_offset);
    ctx.stroke();
    
    
    ctx.beginPath();
    ctx.roundRect(0*scale+x_offset, 75*scale+y_offset, 950*scale, 60*scale, [30, 30, 30, 30]);
    ctx.roundRect(0*scale+x_offset, 225*scale+y_offset, 950*scale, 60*scale, [30, 30, 30, 30]);
    ctx.roundRect(0*scale+x_offset, 375*scale+y_offset, 950*scale, 60*scale, [30, 30, 30, 30]);
    ctx.fillStyle = "#a0a0a0";
    ctx.shadowOffsetY = 1;
    ctx.shadowColor = "#111111";
    ctx.shadowBlur = 10;
    ctx.fill();
    
    ctx.beginPath();
    ctx.moveTo(750*scale+x_offset, 30*scale+y_offset);
    ctx.arc(750*scale+x_offset, 30*scale+y_offset, 30*scale, 0, Math.PI * 2, true);
    ctx.moveTo(750*scale+x_offset, 180*scale+y_offset);
    ctx.arc(750*scale+x_offset, 180*scale+y_offset, 30*scale, 0, Math.PI * 2, true);
    ctx.moveTo(750*scale+x_offset, 330*scale+y_offset);
    ctx.arc(750*scale+x_offset, 330*scale+y_offset, 30*scale, 0, Math.PI * 2, true);
    ctx.fillText("K", 750*scale+x_offset, 320*scale+y_offset);
    
    ctx.moveTo(1050*scale+x_offset, 30*scale+y_offset);
    ctx.arc(1050*scale+x_offset, 30*scale+y_offset, 30*scale, 0, Math.PI * 2, true);
    ctx.moveTo(1050*scale+x_offset, 180*scale+y_offset);
    ctx.arc(1050*scale+x_offset, 180*scale+y_offset, 30*scale, 0, Math.PI * 2, true);
    ctx.moveTo(1050*scale+x_offset, 330*scale+y_offset);
    ctx.arc(1050*scale+x_offset, 330*scale+y_offset, 30*scale, 0, Math.PI * 2, true);
    ctx.moveTo(1050*scale+x_offset, 480*scale+y_offset);
    ctx.arc(1050*scale+x_offset, 480*scale+y_offset, 30*scale, 0, Math.PI * 2, true);
    
    ctx.moveTo(300*scale+x_offset, 30*scale+y_offset);
    ctx.arc(300*scale+x_offset, 30*scale+y_offset, 30*scale, 0, Math.PI * 2, true);
    ctx.moveTo(330*scale+x_offset, 180*scale+y_offset);
    ctx.arc(300*scale+x_offset, 180*scale+y_offset, 30*scale, 0, Math.PI * 2, true);
    ctx.moveTo(135*scale+x_offset, 330*scale+y_offset);
    ctx.arc(300*scale+x_offset, 330*scale+y_offset, 30*scale, 0, Math.PI * 2, true);
    
    
    ctx.moveTo(60*scale+x_offset, 105*scale+y_offset);
    ctx.arc(30*scale+x_offset, 105*scale+y_offset, 30*scale, 0, Math.PI * 2, true);
    ctx.moveTo(505*scale+x_offset, 105*scale+y_offset);
    ctx.arc(475*scale+x_offset, 105*scale+y_offset, 30*scale, 0, Math.PI * 2, true);
    ctx.moveTo(60*scale+x_offset, 255*scale+y_offset);
    ctx.arc(30*scale+x_offset, 255*scale+y_offset, 30*scale, 0, Math.PI * 2, true);
    ctx.moveTo(505*scale+x_offset, 255*scale+y_offset);
    ctx.arc(475*scale+x_offset, 255*scale+y_offset, 30*scale, 0, Math.PI * 2, true);
    ctx.moveTo(60*scale+x_offset, 405*scale+y_offset);
    ctx.arc(30*scale+x_offset, 405*scale+y_offset, 30*scale, 0, Math.PI * 2, true);
    ctx.moveTo(505*scale+x_offset, 405*scale+y_offset);
    ctx.arc(475*scale+x_offset, 405*scale+y_offset, 30*scale, 0, Math.PI * 2, true);

    ctx.fillStyle = "white";
    ctx.shadowOffsetX = 2;
    ctx.shadowOffsetY = 2;
    ctx.shadowColor = "#111111";
    ctx.shadowBlur = 10;
    
    ctx.fill();

    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;
    ctx.shadowColor = "#111111";
    ctx.shadowBlur = 0;
    ctx.fillStyle = "black";
    ctx.font = `${30*scale}px Comfortaa`;
    ctx.fillText("K10", 300*scale+x_offset*1.5-25*scale, 30*scale+y_offset+10*scale);
    ctx.fillText("K9", 750*scale+x_offset*1.5-25*scale, 30*scale+y_offset+10*scale);
    ctx.fillText("K8", 1050*scale+x_offset*1.5-25*scale, 30*scale+y_offset+10*scale);

    ctx.fillText("K7", 300*scale+x_offset*1.5-25*scale, 180*scale+y_offset+10*scale);
    ctx.fillText("K6", 750*scale+x_offset*1.5-25*scale, 180*scale+y_offset+10*scale);
    ctx.fillText("K5", 1050*scale+x_offset*1.5-25*scale, 180*scale+y_offset+10*scale);

    ctx.fillText("K4", 300*scale+x_offset*1.5-25*scale, 330*scale+y_offset+10*scale);
    ctx.fillText("K3", 750*scale+x_offset*1.5-25*scale, 330*scale+y_offset+10*scale);
    ctx.fillText("K2", 1050*scale+x_offset*1.5-25*scale, 330*scale+y_offset+10*scale);
    ctx.fillText("K1", 1050*scale+x_offset-25*scale, 480*scale+y_offset+10*scale);

    
    ctx.fillText("X6", 60*scale-25*scale, 105*scale+y_offset+10*scale);
    ctx.fillText("X5", 475*scale+x_offset*1.5-25*scale, 105*scale+y_offset+10*scale);
    ctx.fillText("X4", 60*scale-25*scale, 255*scale+y_offset+10*scale);
    ctx.fillText("X3", 475*scale+x_offset*1.5-25*scale, 255*scale+y_offset+10*scale);
    ctx.fillText("X2", 60*scale-25*scale, 405*scale+y_offset+10*scale);
    ctx.fillText("X1", 475*scale+x_offset*1.5-25*scale, 405*scale+y_offset+10*scale);
}
var arrayOfObjects = [
    { id: '(0, 0)', x: 30, y: 0 },
    { id: '(0, 1)', x: 180, y: 600 },
    { id: '(0, 2)', x:330, y: 800 }
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
        forklyft_dashboard.style.display = 'none';

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

//addElementsFromArray(arrayOfObjects);
function getCursorPosition(example, event) {
    const rect = example.getBoundingClientRect()
    const x = event.clientX - rect.left
    const y = event.clientY - rect.top
    alert("x: " + x + " y: " + y)
}
example.addEventListener('mousedown', function(e) {
    getCursorPosition(example, e)
})
var CheckPoints = [
    { point: 'K1', x: 780, y: 300 },
    { point: 'K2', x: 400, y: 250 },
    { point: 'K3', x: 590, y: 250 },
    { point: 'K4', x: 140, y: 250 },
    { point: 'K5', x: 650, y: 140 },
    { point: 'K6', x: 400, y: 140 },
    { point: 'K7', x: 140, y: 140 },
    { point: 'K8', x: 650, y: 30 },
    { point: 'K9', x: 400, y: 30 },
    { point: 'K10', x: 140, y: 30 }
];
var lyft_id_, _x, _y;
function GetCheckPoint(lyft_id, point_name){
    CheckPoints.forEach(function (object) {
        if(point_name==object.point){
            lyft_id_ = lyft_id;
            _x=object.x;
            _y=object.y;
            var elem = document.getElementById(lyft_id);
            elem.style.left = object.x+'px';
            elem.style.top = object.y-15+'px';
            //animation(lyft_id, object.x, object.y);
        }
    });
}

var rectX =0;
var rectY =0;

async function animation(id, x, y) {
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
Socket();
var request = '{"(0, 0)": "K6", "(0, 1)": "K6", "(0, 2)": "K6", "(1, 0)": "K1", "(1, 1)": "K3", "(1, 2)": "K3", "(2, 0)": "K1", "(2, 1)": "K1", "(2, 2)": "K2", "(3, 0)": "K10", "(3, 1)": "K9", "(3, 2)": "K3", "(4, 0)": "K9", "(4, 1)": "K5", "(4, 2)": "K10", "(5, 0)": "K6", "(5, 1)": "K6", "(5, 2)": "K1", "(6, 0)": "K2", "(6, 1)": "K3", "(6, 2)": "K3", "(7, 0)": "K6", "(7, 1)": "K1", "(7, 2)": "K6", "(8, 0)": "K2", "(8, 1)": "K3", "(8, 2)": "K3", "(9, 0)": "K5", "(9, 1)": "K6", "(9, 2)": "K6", "(10, 0)": "K1", "(10, 1)": "K6", "(10, 2)": "K6", "(11, 0)": "K1", "(11, 1)": "K9", "(11, 2)": "K9", "(12, 0)": "K3", "(12, 1)": "K2", "(12, 2)": "K1", "(13, 0)": "K2", "(13, 1)": "K3", "(13, 2)": "K5", "(14, 1)": "K5", "(14, 2)": "K10"}';
function Socket(){
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
        //messageElement.innerHTML = "Получено сообщение от сервера: " + event.data;
        JSONParser();
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
}
function JSONParser(){
    var obj = JSON.parse(request);
    for (let key in obj) {
        //console.log("key", key)
        //console.log("value", obj[key])
        let forklyft = new Object();
        forklyft={ id: key, x:0, y: 0 };
        arrayOfObjects.push(forklyft);
        addElementsFromArray(arrayOfObjects);
        GetCheckPoint(key, obj[key]);
    }
    //console.log(arrayOfObjects);
}