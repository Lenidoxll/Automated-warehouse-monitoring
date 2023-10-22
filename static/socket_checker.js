const socket = new WebSocket("ws://75.119.142.124:8002/ws2");
socket.timeout = 0; // Без timeout

// Открываем соединение
socket.onopen = (event) => {
    console.log("Соединение открыто");
};

// Обработка данных, полученных от сервера
socket.onmessage = (event) => {
    console.log(event.data)
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