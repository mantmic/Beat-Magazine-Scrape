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
) returns text as 
$$
	declare 
		v_artist_gigs	json := '[]' ;
	begin 
		-- get any existing object gigs
		select 
			coalesce ( artist_object -> p_artist_id -> 'artistGigs', '[]' )
		from 
			beat.artist a 
		where
			a.artist_idx = beat.get_artist_idx_fnc ( p_artist_id )
		into 
			v_artist_gigs
		;
		v_artist_gigs = case when v_artist_gigs::text = 'null' or v_artist_gigs is null then '[]' else v_artist_gigs end ;
		insert into beat.artist ( 
			  artist_idx 		--char(1)
			, artist_object  	--json
		)
		values ( 
			  beat.get_artist_idx_fnc ( p_artist_id )
			, json_build_object ( 
				 p_artist_id, json_build_object (
					'beatArtistType',p_beat_type,
					'artistName',p_artist_name,
					'artistLinks',p_artist_links,
					'artistGigs',v_artist_gigs
			  	 )
			 )
		)
		on conflict on constraint artist_pk do --when there already are gigs on this date 
		update set 
			  artist_object = jsonb_set(artist.artist_object::jsonb, ('{' || p_artist_id || '}')::text[] , (excluded.artist_object -> p_artist_id)::jsonb , true)
		;
		return p_artist_id ;
	end ;
$$ language plpgsql 
;