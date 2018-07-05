select 
	beat.post_artist_fnc ( 
	  p_artist_id 		:= 'band01'
	, p_beat_type 		:= 'headline'
	, p_artist_name 	:= 'The first band'
	, p_artist_links 	:= '{}'
)
;

select 
	beat.post_artist_fnc ( 
	  p_artist_id 		:= 'band02'
	, p_beat_type 		:= 'headline'
	, p_artist_name 	:= 'The 2nd band'
	, p_artist_links 	:= '{}'
)
;

select 
	beat.post_artist_fnc ( 
	  p_artist_id 		:= 'band03'
	, p_beat_type 		:= 'headline'
	, p_artist_name 	:= 'The 3 band'
	, p_artist_links 	:= '{}'
)
;

select 
	beat.post_artist_fnc ( 
	  p_artist_id 		:= 'band04'
	, p_beat_type 		:= 'headline'
	, p_artist_name 	:= 'The fourth band'
	, p_artist_links 	:= '{}'
)
;

select beat.post_venue_fnc (
	  p_venue_id 		:= 'venue01'
	, p_venue_name 		:= 'The first venue'
	, p_venue_address 	:= '101 Collins St, Melbourne'
	, p_lat 			:= 0
	, p_lon 			:= 0 
) 
;

select beat.post_gig_fnc ( 
	  p_gig_id 			:= 'test01'
	, p_gig_genre 		:= 'Rock'
	, p_gig_datetime	:= '2018-07-01 12:30:00'
	, p_venue_id 		:= 'venue01'
	, p_headline_artist := array['band01']
	, p_support_artist 	:= array['band02']
)
;

select beat.post_gig_fnc ( 
	  p_gig_id 			:= 'test01'
	, p_gig_genre 		:= 'Country'
	, p_gig_datetime	:= '2018-07-03 12:30:00'
	, p_venue_id 		:= 'venue01'
	, p_headline_artist := array['band02']
	, p_support_artist 	:= array['band03', 'band04']
)
;

select
	*
from 
	beat.gig_vw
;