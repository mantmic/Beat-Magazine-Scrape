drop schema if exists beat cascade ;
create schema beat ;

--table to store gigs
/*
--the table really should be like this... but due to the row limit we're going to keep all gigs in a day in ONE RECORD!
create table beat.gig ( 
	  gig_id 			varchar(200)
	, gig_genre 		varchar(100)
	, gig_datetime		timestamp
	, venue_id 			varchar(200)
	, headline_artist 	varchar(200)[]
	, support_artist 	varchar(200)[]
	, constraint gig_pk primary key ( gig_id )  
)
;
*/

create table beat.gig ( 
	  gig_date 			date 
	, gig_details 		json --this will store the information in the fake table above
	, insert_ts 		timestamptz default current_timestamp 
	, last_updated_ts 	timestamptz default current_timestamp 
	, constraint gig_pk primary key ( gig_date ) 
)
;


--table to store venues
create table beat.venue ( 
	  venue_id 			varchar(200)
	, venue_name		varchar(200)
	, venue_address		varchar(200)
	, lat 				float 
	, lon 				float 
	, insert_ts 		timestamptz default current_timestamp 
	, last_updated_ts 	timestamptz default current_timestamp 
	, constraint venue_pk primary key ( venue_id ) 
)
;

--table to store both headline and support artists
create table beat.artist ( 
	  artist_id 	varchar(200)
	, beat_type 	varchar(50) 	--either headline or support
	, artist_name 	varchar(200)
	, artist_links 	json
	, artist_gigs 	varchar(200)[] 	default array[]::varchar(200)[]	--store an array of gigs this artist is part of, this will make going from artist to gig much much quicker
	, insert_ts 		timestamptz default current_timestamp 
	, last_updated_ts 	timestamptz default current_timestamp 
	, constraint artist_pk primary key ( artist_id ) 
)
;
