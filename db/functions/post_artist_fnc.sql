drop function if exists beat.post_artist_fnc ( 
	  p_artist_id 		varchar(200)
	, p_beat_type 		varchar(50) 
	, p_artist_name 	varchar(200)
	, p_artist_links 	json
)
;

create or replace function beat.post_artist_fnc ( 
	  p_artist_id 		varchar(200)
	, p_beat_type 		varchar(50) 
	, p_artist_name 	varchar(200)
	, p_artist_links 	json
) returns void as 
$$
	begin 
		insert into beat.artist ( 
			  artist_id 	--varchar(200)
			, beat_type 	--varchar(50) 
			, artist_name 	--varchar(200)
			, artist_links 	--json
		)
		values 
		( 
			  p_artist_id 
			, p_beat_type
			, p_artist_name
			, p_artist_links 
		)
		on conflict on constraint artist_pk do update set 
			  beat_type 	= excluded.beat_type
			, artist_name 	= excluded.artist_name
			, artist_links 	= excluded.artist_links
			, last_updated_ts = current_timestamp 
		;
	end ;
$$ language plpgsql 
;