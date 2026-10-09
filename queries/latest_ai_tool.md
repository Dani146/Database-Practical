## The latest integrated AI tool by department

**Description:** This query answers the question: "What is the most recently adopted AI tool in each department, and when was it integrated?" It allows management to track the latest technological updates and trends within every single team.

Written by Matiss

```
SELECT
    c.name AS company_name,
    d.name AS department_name,
    t.name AS latest_ai_tool,
    au.integration_date
FROM AI_usage au
JOIN Department d ON au.department_id = d.department_id
JOIN Company c ON d.company_id = c.company_id
JOIN AI_tool t ON au.ai_tool_id = t.ai_tool_id
WHERE au.integration_date = (
    SELECT MAX(integration_date)
    FROM AI_usage au2
    WHERE au2.department_id = au.department_id
)
ORDER BY company_name, au.integration_date DESC;
```
