drop function if exists beat.get_artist_fnc ( p_artist_id varchar(200)[] ) ;
create or replace function beat.get_artist_fnc ( p_artist_id varchar(200)[] )
returns table ( 
	  artist_id 	varchar(200)
	, beat_type 	varchar(50)
	, artist_name 	varchar(200)
	, artist_links 	json
	, artist_gigs 	json
)
as 
$$
	declare 
		v_artist_idx int[] ;
	begin 
		--figure out the artist indexes required
		select 
			array_agg ( artist_idx )
		from 
			( select distinct 
				beat.get_artist_idx_fnc ( unnest ( p_artist_id ) ) as artist_idx
			) q
		into 
			v_artist_idx
		;
		return query 
		select 
			  a2.artist_id::varchar(200)
			, ( artist_object ->> 'beatArtistType' )::varchar(50)
			, ( artist_object ->> 'artistName' )::varchar(200)
			, artist_object -> 'artistLinks'
			, artist_object -> 'artistGigs'
		from 
			( select 
				  json_object_keys ( artist_object ) 					as artist_id
				, artist_object -> json_object_keys ( artist_object ) 	as artist_object 
			from 
				beat.artist a 
			where
				a.artist_idx = any(v_artist_idx)
			) a2 
		where
			a2.artist_id = any(p_artist_id)
		;
	end ;
$$ 
language plpgsql ;
;