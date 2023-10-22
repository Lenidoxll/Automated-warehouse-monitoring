function SetActive(i){
    var p_n = document.getElementById("p_n");
    p_n.innerHTML ='';
    var t_1 = document.getElementById("t_1");
    var t_2 = document.getElementById("t_2");
    var t_3 = document.getElementById("t_3");
    var t_4 = document.getElementById("t_4");
    var t_5 = document.getElementById("t_5");
    var tables = [t_1, t_2, t_3, t_4, t_5]
    t_1.style.display = 'none';
    t_2.style.display = 'none';
    t_3.style.display = 'none';
    t_4.style.display = 'none';
    t_5.style.display = 'none';

    if(i==1){
        t_1.style.display = 'block';
        p_n.innerHTML ='Пройденное расстояние';
    }
    if(i==2){
        t_2.style.display = 'block';
        p_n.innerHTML ='Количество выполненных заказов';
    }
    if(i==3){
        t_3.style.display = 'block';
        p_n.innerHTML ='Время в движениее';
    }
    if(i==4){
        t_4.style.display = 'block';
        p_n.innerHTML ='Время простоя';
    }
    if(i==5){
        t_5.style.display = 'block';
        p_n.innerHTML ='Время нахождения в каждом статусе';
    }
}