create or replace function beat.get_artist_idx_fnc ( p_artist_id text ) returns int as 
$$
	select ascii ( lower ( ( substring ( ( string_to_array ( p_artist_id, '/' ) )[array_length(string_to_array ( p_artist_id, '/' ),1 ) ],1,1 ) ) ) )
$$ language sql 
;