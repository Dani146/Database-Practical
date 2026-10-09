## Volume of job offers published before vs. after AI integration

**Description:** This query answers the question: "Does hiring increase or decrease after a department integrates AI?" It finds the earliest AI adoption date for each department and counts how many job offers were posted before that date versus after, highlighting the impact of AI on job creation.

Written by Danylo

```
WITH FirstAIIntegration AS (
    SELECT department_id, MIN(integration_date) AS first_ai_date
    FROM AI_usage
    GROUP BY department_id
)
SELECT 
    d.name AS department_name,
    f.first_ai_date,
    SUM(CASE WHEN jo.publication_date < f.first_ai_date THEN 1 ELSE 0 END) AS offers_before_ai,
    SUM(CASE WHEN jo.publication_date >= f.first_ai_date THEN 1 ELSE 0 END) AS offers_after_ai
FROM Department d
JOIN FirstAIIntegration f ON d.department_id = f.department_id
LEFT JOIN Job_offer jo ON d.department_id = jo.department_id
GROUP BY d.name, f.first_ai_date
ORDER BY offers_after_ai DESC;
```