## Correlation between AI adoption level and active workforce size

**Description:** This query answers the question: "Do companies that adopt more AI tools employ fewer people overall?" It compares the total number of AI deployments against the total number of active employees in each company to spot macro-level trends between automation and human labor.

Written by Adrien

```
SELECT
    c.name AS company_name,
    COUNT(DISTINCT au.ai_usage_id) AS total_ai_deployments,
    COUNT(DISTINCT e.employee_id) AS active_workforce
FROM Company c
LEFT JOIN Department d ON c.company_id = d.company_id
LEFT JOIN AI_usage au ON d.department_id = au.department_id
LEFT JOIN Employee e ON d.department_id = e.department_id AND e.end_time IS NULL
GROUP BY c.company_id, c.name
ORDER BY total_ai_deployments DESC, active_workforce ASC;
```
