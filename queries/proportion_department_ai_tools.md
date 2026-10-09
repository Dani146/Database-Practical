## Proportion of AI tools in the department compared to the company

**Description:** This query allows us to see which departments use more AI tools than others. It answers the question: "How many AI tools are used by a specific department compared to the total number of AI tools deployed across the entire company?" It is very useful to identify which teams are driving AI adoption.

Written by Adrien

```
SELECT
    c.name AS company_name,
    d.name AS department_name,
    COUNT(au.ai_tool_id) AS dept_ai_tools,
    (
        SELECT COUNT(au2.ai_tool_id)
        FROM AI_usage au2
        JOIN Department d2 ON au2.department_id = d2.department_id
        WHERE d2.company_id = c.company_id
    ) AS company_total_ai_tools
FROM Department d
JOIN Company c ON d.company_id = c.company_id
LEFT JOIN AI_usage au ON d.department_id = au.department_id
GROUP BY c.company_id, c.name, d.department_id, d.name
ORDER BY company_name, dept_ai_tools DESC;
```
