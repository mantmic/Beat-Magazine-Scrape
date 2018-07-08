--drop view if exists beat.gig_vw ;
create or replace view beat.gig_vw as 
select 
	  gig_date
	, gig_id
	, to_timestamp ( gig_details -> gig_id ->> 'gigDatetime', 'YYYY-MM-DD"T"HH24:MI:SS' ) 	as gig_datetime
	, gig_details -> gig_id ->> 'venueId' 													as venue_id
	, gig_details -> gig_id ->> 'gigGenre' 													as gig_genre
	, gig_details -> gig_id -> 'headlineArtist' 											as headline_artist 
	, gig_details -> gig_id -> 'supportArtist'												as support_artist
	, ( gig_details -> gig_id ->> 'gigPrice' )::numeric										as gig_price
from 
	( select 
		  g.gig_date 
		, json_object_keys ( g.gig_details ) as gig_id
		, g.gig_details
	from 
		beat.gig g 
	) g2
;