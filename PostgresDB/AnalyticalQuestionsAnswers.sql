-- 1. Severity Distribution: What is the count of vulnerabilities for different severity levels
;
-- assuming type primary is to be considered
SELECT cvsm.baseSeverity as baseseverity, COUNT(*) as total_severities
FROM CVSSMetric cvsm
join Source_type st on cvsm.source_type_id = st.id
JOIN CVE ON cvsm.cve_id = CVE.cve_id
WHERE CVE.lastmodified < '2024-05-02' and cve.vulnstatus != 'Rejected' and st.type = 'Primary'
GROUP by baseseverity
order by baseseverity;


 -- 2.  Worst Products, Platforms : Find out the worst products, platforms with most number of known vulnerabilities
-- exclding Rejected status ones and the cpe's which are not deprecated
select cp.cpename as product, count(*) as total_known_vulnerabilities
from cpe cp
inner join Titles t on t.cpenameid = cp.cpenameid 
inner join matches m on m.cpenameid = cp.cpenameid 
inner join matchstring ms on ms.matchcriteriaid = m.matchcriteriaid 
inner join cpematch cpm on cpm.matchcriteriaid = ms.matchcriteriaid 
inner join nodes n on cpm.node_id = n.id 
inner join configurations conf on n.configuration_id = conf.id 
inner join cve cv on conf.cve_id = cv.cve_id 
WHERE cv.lastModified < '2024-05-02' 
and cv.vulnstatus != 'Rejected'
and cp.deprecated = false 
group by cp.cpename 
order by total_known_vulnerabilities desc;


-- 161,642 without any deprecated
-- with deprrecated false 156,016
-- with deprrecated and lastdate modified 155,831 

select *
from cpe cp;
-- 1283590

select *
from cpe cp
where deprecated = false;
-- 1,220,428 deprecated = false

select *
from cpe cp
where deprecated = true;
-- 63,162 deprecated = true


select count(*)
from cve cv
WHERE cv.lastModified < '2024-05-02' and cv.vulnstatus != 'Rejected'
;


-- 3  List top 10 vulnerabilities that have the highest impact

SELECT c.cve_id, cvsm.impactScore as impactScore
FROM CVSSMetric cvsm
JOIN CVE c ON cvsm.cve_id = c.cve_id
WHERE c.lastmodified < '2024-05-02' and c.vulnstatus != 'Rejected'
ORDER BY cvsm.impactScore DESC, c.cve_id
LIMIT 10;

-- 4  Top 10 Vulnerabilities with Highest Exploitability Scores

SELECT c.cve_id, cvsm.exploitabilityScore as exploitabilityscore
FROM CVSSMetric cvsm
JOIN CVE c ON cvsm.cve_id = c.cve_id
WHERE c.lastmodified < '2024-05-02' and c.vulnstatus != 'Rejected'
ORDER BY cvsm.exploitabilityScore desc, c.cve_id
LIMIT 10;


--5 List top 10 attack vectors used

SELECT cvsm.attackVector, COUNT(*) as total_count
FROM CVSSMetric cvsm
JOIN CVE c ON cvsm.cve_id = c.cve_id
WHERE c.lastmodified < '2024-05-02' and c.vulnstatus != 'Rejected'
GROUP BY attackVector
ORDER BY total_count DESC
LIMIT 10;


-- based on matchcriteriaid show all matches in cpematch API

select ms.matchcriteriaid, m.*
from matchstring ms 
join matches m on ms.matchcriteriaid = m.matchcriteriaid 
where 
--ms.status = 'Active'
ms.matchcriteriaid = '6f238c75-e24a-406f-beb5-8758c8fe9603'
;
