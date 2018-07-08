--function to remove gigs from the artistgigs object for an artist
drop function if exists beat.drop_artist_gig_fnc ( p_artist_id varchar(200), p_gig_id varchar(200) ) ;
create or replace function beat.drop_artist_gig_fnc ( p_artist_id varchar(200), p_gig_id varchar(200) ) returns void as 
$$ 
	declare 
		v_artist_object json ;
	begin 
		select 
			artist_object -> p_artist_id
		from 
			beat.artist
		where 
			artist_idx = beat.get_artist_idx_fnc ( p_artist_id )
		into 
			v_artist_object
		;
		if v_artist_object is not null then 
			update 
				beat.artist 
			set 
				artist_object = jsonb_set ( artist_object::jsonb, ('{' || p_artist_id || '}')::text[], new_artist_object, false )
			from 
				( select
					 jsonb_set ( ( artist_object-> p_artist_id )::jsonb, '{"artistGigs"}'::text[], ( artist_object-> p_artist_id-> 'artistGigs' )::jsonb - p_gig_id ) as new_artist_object
				from 
					beat.artist
				where
					artist_idx = beat.get_artist_idx_fnc ( p_artist_id )
				) q 
			where  
				artist_idx = beat.get_artist_idx_fnc ( p_artist_id )
			;
		end if ;
	end ;
$$ language plpgsql 
;
