--function to upsert a gig 
drop function if exists beat.post_gig_fnc ( 
	  p_gig_id 			varchar(200)
	, p_gig_genre 		varchar(100)
	, p_gig_datetime		timestamp
	, p_venue_id 			varchar(200)
	, p_headline_artist 	varchar(200)[]
	, p_support_artist 	varchar(200)[]
)
;
create or replace function beat.post_gig_fnc ( 
	  p_gig_id 			varchar(200)
	, p_gig_genre 		varchar(100)
	, p_gig_datetime	timestamp
	, p_venue_id 		varchar(200)
	, p_headline_artist varchar(200)[]
	, p_support_artist 	varchar(200)[]
) returns void as 
;

do
$$ 
	declare 
		p_headline_artist 	varchar(200)[] := array['band1','band2'] ;
		v_existing_gig 		json ; 
	 	v_remove_artists	varchar(200)[] ;
	 	v_new_artists 		varchar(200)[] ;
	begin 
		select 
			gig_details -> 'test_gig_id' 
		from 	
			beat.gig g 
		where 
			g.gig_date = ('2018-07-01 12:30:00'::timestamp)::date
		into 
			v_existing_gig
		;
		--determine new bands as part of the gig
		select 
		 	  array_agg ( new_artist ) 
		 	, array_agg ( remove_artist ) 
		from 
			( select 
				  case when ea.existing_artist is null then ia.input_artist
				  end as new_artist
				, case when ia.input_artist is null then ia.input_artist
				  end as remove_artist
			from 
				( select 
					unnest ( p_headline_artist )::varchar(200) as input_artist 
				) ia 
				full outer join 
				( select 
					( json_array_elements ( v_existing_gig -> 'headlineArtist' ) )::varchar(200) as existing_artist 
				) ea
					on ia.input_artist = ea.existing_artist
			) q 
		into 
			  v_new_artists
			, v_remove_artists
		;
		--insert the new gig
		--if there was a gig with the previous id, update the artist gig fields
		drop table if exists test_tmp ;
		create temporary table test_tmp as select v_new_artists, v_remove_artists
		;
	end ;
$$ 
language plpgsql ;
;

select * from test_tmp 
;
select 
	gig_details
from 	
	beat.gig g 
where 
	g.gig_date = ('2018-07-06 12:30:00'::timestamp)::date
;


-- determine if the gig already exists
select 
	gig_details -> 'test_gig_id' as existing_gig
from 	
	beat.gig g 
where 
	g.gig_date = ('2018-07-01 12:30:00'::timestamp)::date
;


--insert a couple of bands 
insert into beat.artist ( 
	artist_id
)
values ( 'band1' ), ( 'band2' )
;

--insert a new gig
insert into  beat.gig ( 
	  gig_date 		
	, gig_details 
)
select  
	  '2018-07-01'
	, json_build_object ( 
		'test_gig_id', json_build_object (
			'gigGenre', 'Rock',
			'headlineArist',array['band1','band2']
	  	 )
	 )
;

--update that gig, insert another new gig