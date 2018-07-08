--function to put gigs in the artistGigs objects for an artist
drop function if exists beat.push_artist_gig_fnc ( p_artist_id varchar(200), p_gig_id varchar(200) ) ;
create or replace function beat.push_artist_gig_fnc ( p_artist_id varchar(200), p_gig_id varchar(200) ) returns void as 
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
					 jsonb_set ( ( v_artist_object )::jsonb, '{"artistGigs"}'::text[], ( v_artist_object-> 'artistGigs' )::jsonb || ( '["' || p_gig_id || '"]')::jsonb ) as new_artist_object
				) q 
			where  
				artist_idx = beat.get_artist_idx_fnc ( p_artist_id )
			;
	end if ;
	end ;
$$ language plpgsql
;
