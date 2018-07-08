--function to upsert a gig 
drop function if exists beat.post_gig_fnc ( 
	  p_gig_id 			varchar(200)
	, p_gig_genre 		varchar(100)
	, p_gig_datetime	timestamp
	, p_venue_id 		varchar(200)
	, p_headline_artist varchar(200)[]
	, p_support_artist 	varchar(200)[]
	, p_gig_price 		float
)
;

--need to fix bug where can't update date of gig
create or replace function beat.post_gig_fnc ( 
	  p_gig_id 			varchar(200)
	, p_gig_genre 		varchar(100)
	, p_gig_datetime	timestamp
	, p_venue_id 		varchar(200)
	, p_headline_artist varchar(200)[]
	, p_support_artist 	varchar(200)[]
	, p_gig_price 		float
) returns void as 
$$ 
	declare 
		v_existing_gig 		json ; 
		v_existing_date 	date ;
		v_existing_artist 	json ;
	 	v_remove_artists	varchar(200)[] ; --artists that had this gig that are now not part of the gig
	 	v_new_artists 		varchar(200)[] ; --artists that previously didn't have this gig that now should have this gig
	 	v_row 				record ;
	begin 
		select 
			  gv.gig_date
			, gv.headline_artist::jsonb || gv.support_artist::jsonb
		from 
			beat.gig_vw gv
		where
			gig_id = p_gig_id 
		into 
			  v_existing_date
			, v_existing_artist
		;
		--determine new bands as part of the gig
		select 
		 	  array_agg ( new_artist ) 		filter ( where new_artist is not null ) 
		 	, array_agg ( remove_artist ) 	filter ( where remove_artist is not null ) 
		from 
			( select 
				  case when ea.existing_artist is null then ia.input_artist
				  end as new_artist
				, case when ia.input_artist is null then ea.existing_artist
				  end as remove_artist
				, existing_artist
				, input_artist
			from 
				( select 
					unnest ( p_headline_artist )::varchar(200) as input_artist 
				  union all 
				  select 
				  	unnest ( p_support_artist )::varchar(200) as input_artist
				) ia 
				full outer join 
				( select 
					( json_array_elements ( v_existing_artist ) #>> '{}' )::varchar(200) as existing_artist 
				) ea
					on ia.input_artist = ea.existing_artist
			) q
		into 
			  v_new_artists
			, v_remove_artists
		;
		--update the fields on the artists
		--remove old artists
		/*update 
			beat.artist 
		set 
			artist_gigs = array_remove ( artist_gigs, p_gig_id )
		where
			artist_id = any ( v_remove_artists )
		;
		--add new artists 
		update 
			beat.artist 
		set 
			artist_gigs = array_append ( artist_gigs, p_gig_id )
		where
			artist_id = any ( v_new_artists )
		;
		*/
	 	--drop table if exists beat.test_tmp ;
 		--create table beat.test_tmp as select p_gig_id, v_remove_artists, v_new_artists, v_existing_artist, p_headline_artist ;
		for v_row in select unnest ( v_remove_artists )::varchar(200) as artist_id loop 
			perform beat.drop_artist_gig_fnc ( p_artist_id := v_row.artist_id, p_gig_id := p_gig_id ) ;
		end loop 
		;
		for v_row in select unnest ( v_new_artists )::varchar(200) as artist_id loop  
			perform beat.push_artist_gig_fnc ( p_artist_id := v_row.artist_id, p_gig_id := p_gig_id ) ;
		end loop 
		;
		--remove the existing object
		update 
			beat.gig 
		set 
			gig_details = gig_details::jsonb - p_gig_id
		where 
			gig_date = v_existing_date
		;
		--insert the new gig
		insert into beat.gig ( 
			  gig_date 		
			, gig_details 
		)
		values ( 
			  date_trunc ( 'day', p_gig_datetime )
			, json_build_object ( 
				 p_gig_id, json_build_object (
					'gigGenre', p_gig_genre,
					'headlineArtist',p_headline_artist,
					'supportArtist',p_support_artist,
					'gigDatetime',p_gig_datetime,
					'venueId',p_venue_id,
					'gigPrice',p_gig_price
			  	 )
			 )
		)
		on conflict on constraint gig_pk do --when there already are gigs on this date 
		update set 
			  gig_details = jsonb_set(gig.gig_details::jsonb, ('{' || p_gig_id || '}')::text[] , (excluded.gig_details -> p_gig_id)::jsonb , true)
			, last_updated_ts = current_timestamp 
		;
	end ;
$$ 
language plpgsql ;
;

