
-- создаём партиционированную по месяцам таблицу.
-- репликация таблицы настроена на второй сервер clickhouse, в нём создаём то же самое
CREATE TABLE main_data_stg_t3
(
	status String,
    id_forklift UInt64,
    id_warehouse UInt32,
    id_task UInt64,
    id_point String,
    event_timestamp DateTime64(3)
) ENGINE = ReplicatedReplacingMergeTree('/clickhouse/tables/{layer}-{shard}/main_data_stg_t3', '{replica}', id_warehouse)
PARTITION BY toYYYYMM(event_timestamp)
ORDER BY (id_forklift, id_warehouse, id_point);

-- создаём распределённую таблицу для запросов
create table main_data_stg_t3_distr as main_data_stg_t3
engine = Distributed('default', 'default', 'main_data_stg_t3', id_warehouse);


-- создаём таблицу для хранения дат ТО погрузчиков
CREATE TABLE maintenance_catalog (
    id_forklift UInt64,
    id_warehousr UInt32,
    last_maintenance_date Date,
    next_maintenance_date Date,
    _version DateTime64 MATERIALIZED now64()
) ENGINE = ReplacingMergeTree(_version) PARTITION BY tuple() ORDER BY id_forklift, id_warehousr;

-- создаём словарь для невелирования операции join и ускорения запросов для аналитики
CREATE dictionary maintenance_catalog_dict
(
    id_forklift UInt64,
    id_warehousr UInt32,
    last_maintenance_date Date,
    next_maintenance_date Date
)
PRIMARY KEY (id_forklift, id_warehousr)
SOURCE(CLICKHOUSE(HOST '75.119.142.124' PORT 9035 USER 'default' PASSWORD 'qolkasw10-=' TABLE 'maintenance_catalog' DB 'default'))
LAYOUT(COMPLEX_KEY_HASHED_ARRAY())
LIFETIME(MIN 0 MAX 1);