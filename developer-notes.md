# Developer Notes

## References

1. [Python Virtual Environment Commands)[https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/]


## Queries

### Get the daily footfall data

```SQL
select 
	date(timestamp1) as 'date', 
	-- COUNT(DISTINCT `objectid`) .
	count(*) footfall
from sensorevents 
where eventcode in ('PDD', 'PEZ', 'PLZ')
	-- and storeid in (7001, 7002)
group by date(timestamp1) order by timestamp1;
```
