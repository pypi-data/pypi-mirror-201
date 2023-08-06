SELECT works.id, 
typeof(works.published_year), typeof(oaj_start),
works.published_year> oaj_start,
doaj_url FROM works
  INNER JOIN open_access_journals ON
    open_access_journals.issn_print = works.issn_print
    OR
    open_access_journals.issn_eprint = works.issn_electronic
 ;

select doaj_url from open_access_journals where oaj_start = '';

UPDATE open_access_journals SET oaj_start = null WHERE oaj_start = '';
UPDATE open_access_journals SET oaj_start = cast(oaj_start as integer);
