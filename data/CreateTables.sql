create table Series (
	SeriesName	varchar(20) 	not null,
	NumberMovies	int,
	
	primary key (SeriesName)
);


create table Movie (
	Title		varchar(50)	not null,
	Year		int,
	Rating		int,
	Runtime	time,
	Genre		varchar(75),
	Director	varchar(25),
	Actors		varchar(100),
	Plot		varchar(500),
	PosterLink	varchar(200),
	Metacritic	int,

	SeriesName	varchar(20),
	SeriesNumber	int,
	Format		varchar(5),
	
	primary key (Title),
	foreign key (SeriesName) references Series(SeriesName)
);
