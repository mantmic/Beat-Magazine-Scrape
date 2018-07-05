drop function if exists beat.post_venue_fnc (
	  p_venue_id 		varchar(200)
	, p_venue_name 		varchar(200)
	, p_venue_address 	varchar(200)
	, p_lat 			float
	, p_lon 			float
)
;

create or replace function beat.post_venue_fnc (
	  p_venue_id 		varchar(200)
	, p_venue_name 		varchar(200)
	, p_venue_address 	varchar(200)
	, p_lat 			float
	, p_lon 			float
) returns void as 
$$
	begin 
		insert into beat.venue ( 
			  venue_id 		--varchar(200)
			, venue_name	--varchar(200)
			, venue_address --varchar(200)
			, lat 			--float 
			, lon 			--float 
		)
		values 
		( 
			  p_venue_id 
			, p_venue_name
			, p_venue_address
			, p_lat 
			, p_lon 
		)
		on conflict on constraint venue_pk do update set 
			  venue_name 	= excluded.venue_name
			, venue_address = excluded.venue_address
			, lat 			= excluded.lat
			, lon 			= excluded.lon
		;
	end ;
$$ language plpgsql 
;