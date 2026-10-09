## Immediate job displacement: Departures shortly after AI integration

**Description:** This query answers the question: "Are employees leaving their jobs shortly (within 6 months) after an AI tool is introduced in their team?" It tracks the direct short-term displacement effect by correlating the AI integration date with employee departure dates.

Written by Adrien

```
SELECT
    c.name AS company_name,
    d.name AS department_name,
    r.name AS role_name,
    au.integration_date,
    e.end_time AS departure_date,
    e.end_reason
FROM Employee e
JOIN Department d ON e.department_id = d.department_id
JOIN Company c ON d.company_id = c.company_id
JOIN Role r ON e.role_id = r.role_id
JOIN AI_usage au ON d.department_id = au.department_id
WHERE e.end_time IS NOT NULL
  AND e.end_time > au.integration_date
  -- PostgreSQL syntax for interval comparison
  AND (e.end_time - au.integration_date) <= INTERVAL '6 months'
ORDER BY (e.end_time - au.integration_date) ASC;
```
