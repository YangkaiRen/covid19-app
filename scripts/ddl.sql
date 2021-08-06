create table covid19_us(
    province_state varchar(100),
    lat double,
    lon double,
    confirmed int,
    deaths int,
    report_date date
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;