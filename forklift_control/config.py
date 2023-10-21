# Справочник маршрутов погрузчиков по складу.
# Каждый маршрут имеет id, id целевого стеллажа, а также набор контрольных точек.
# Каждая контрольная точка имеет свой id, имя, а также расстояние до следующей КТ
path_lib = {
    1: {"path_sequence": [
            {"check_point_id": 1,
             "check_point_name": "K1",
             "next_check_point_distance": 5},
            {"check_point_id": 2,
             "check_point_name": "K2",
             "next_check_point_distance": 10},
            {"check_point_id": 3,
             "check_point_name": "K3",
             "next_check_point_distance": 10}
        ],
        "target_rack_id": "X1"},
    2: {"path_sequence": [
            {"check_point_id": 1,
             "check_point_name": "K1",
             "next_check_point_distance": 5},
            {"check_point_id": 2,
             "check_point_name": "K2",
             "next_check_point_distance": 10},
            {"check_point_id": 3,
             "check_point_name": "K3",
             "next_check_point_distance": 15},
            {"check_point_id": 4,
             "check_point_name": "K4",
             "next_check_point_distance": 10}
        ],
        "target_rack_id": "X2"},
    3: {"path_sequence": [
            {"check_point_id": 1,
             "check_point_name": "K1",
             "next_check_point_distance": 5},
            {"check_point_id": 2,
             "check_point_name": "K2",
             "next_check_point_distance": 5},
            {"check_point_id": 5,
             "check_point_name": "K5",
             "next_check_point_distance": 10},
            {"check_point_id": 6,
             "check_point_name": "K6",
             "next_check_point_distance": 10}
        ],
        "target_rack_id": "X3"},
    4: {"path_sequence": [
            {"check_point_id": 1,
             "check_point_name": "K1",
             "next_check_point_distance": 5},
            {"check_point_id": 2,
             "check_point_name": "K2",
             "next_check_point_distance": 5},
            {"check_point_id": 5,
             "check_point_name": "K5",
             "next_check_point_distance": 10},
            {"check_point_id": 6,
             "check_point_name": "K6",
             "next_check_point_distance": 15},
            {"check_point_id": 7,
             "check_point_name": "K7",
             "next_check_point_distance": 10}
        ],
        "target_rack_id": "X4"},
    5: {"path_sequence": [
            {"check_point_id": 1,
             "check_point_name": "K1",
             "next_check_point_distance": 5},
            {"check_point_id": 2,
             "check_point_name": "K2",
             "next_check_point_distance": 5},
            {"check_point_id": 5,
             "check_point_name": "K5",
             "next_check_point_distance": 5},
            {"check_point_id": 8,
             "check_point_name": "K8",
             "next_check_point_distance": 10},
            {"check_point_id": 9,
             "check_point_name": "K9",
             "next_check_point_distance": 5}
        ],
        "target_rack_id": "X5"},
    6: {"path_sequence": [
            {"check_point_id": 1,
             "check_point_name": "K1",
             "next_check_point_distance": 5},
            {"check_point_id": 2,
             "check_point_name": "K2",
             "next_check_point_distance": 5},
            {"check_point_id": 5,
             "check_point_name": "K5",
             "next_check_point_distance": 5},
            {"check_point_id": 8,
             "check_point_name": "K8",
             "next_check_point_distance": 10},
            {"check_point_id": 9,
             "check_point_name": "K9",
             "next_check_point_distance": 15},
            {"check_point_id": 10,
             "check_point_name": "K10",
             "next_check_point_distance": 10}
        ],
        "target_rack_id": "X6"}
}

# cities list
cities = [
    "Rostov-on-Don",
    "Moscow",
    "Krasnodar",
    "Tver",
    "Saint Petersburg",
    "Almaty"
]
