select beat.post_artist_fnc ( 
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
	, p_gig_price 		:= 10 
)
;

select beat.post_gig_fnc ( 
	  p_gig_id 			:= 'test01'
	, p_gig_genre 		:= 'Country'
	, p_gig_datetime	:= '2018-07-03 12:30:00'
	, p_venue_id 		:= 'venue01'
	, p_headline_artist := array['band02']
	, p_support_artist 	:= array['band03', 'band04']
	, p_gig_price 		:= 10 
)
;

--api query for gigs
select
	gig_id 			as "gigId",
	gig_datetime 	as "gigDatetime",
	venue_id 		as "venueId",
	gig_genre 		as "gigGenre",
	headline_artist as "headlineArtist",
	support_artist 	as "supportArtist"
from 
	beat.gig_vw
;

--api query for artists 
select 
	artist_id 		as "artistId",
	beat_type 		as "beatAristType",
	artist_name 	as "artistName",
	artist_links 	as "artistLinks",
	artist_gigs 	as "artistGigs"
from 
	beat.artist 
;

--api query for venues 
select 
	venue_id 		as "venueId",
	venue_name 		as "venueName",
	venue_address 	as "venueAddress",
	lat,
	lon
from 
	beat.venue
;


--function to get the artist idx for a given artist id
create or replace function beat.get_artist_idx_fnc ( p_artist_id text ) returns int as 
$$
	select ascii ( lower ( ( substring ( ( string_to_array ( p_artist_id, '/' ) )[array_length(string_to_array ( p_artist_id, '/' ),1 ) ],1,1 ) ) ) )
$$ language sql 
;


select 
	 beat.get_artist_idx_fnc(artist_id) as artist_idx 
from 
	beat.artist_backup
;

delete from beat.artist ;

select 
	beat.post_artist_fnc ( 
	  p_artist_id 		:= artist_id
	, p_beat_type 		:= beat_type 
	, p_artist_name 	:= artist_name
	, p_artist_links 	:= artist_links
) 
from 
	beat.artist_backup 
;

select * from beat.test_tmp ;

select * from beat.get_artist_fnc ( array['/category/gig-support/fenn-wilson']) ;
select beat.push_artist_gig_fnc ( '/category/gig-support/fenn-wilson', '/gig/flying-dutchman-6' ) ;

