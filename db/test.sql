insert into beat.venue ( 
	  venue_id 		--varchar(200)
)
values 
( 'venue01')
;

insert into beat.artist ( 
	  artist_id 	--varchar(200)
)
values 
( 'band1'),( 'band2'),( 'band3'),( 'band4'),( 'band5'),( 'band6')
;


;
select beat.post_gig_fnc ( 
	  p_gig_id 			:= 'test01'
	, p_gig_genre 		:= 'Rock'
	, p_gig_datetime	:= '2018-07-01 12:30:00'
	, p_venue_id 		:= 'venue01'
	, p_headline_artist := array['band1','band2']
	, p_support_artist 	:= array['band3','band4']
)
;

select
	*
from 
	beat.gig_vw
;