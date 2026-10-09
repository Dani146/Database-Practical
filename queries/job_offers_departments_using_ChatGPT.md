## Job offers in departments already using ChatGPT
**Description:** This query answers the question: "What are the current open job positions in departments that have already integrated ChatGPT into their workflow?" It helps target recruitment needs for teams that are already familiar with this specific generative AI tool.

Written by Matiss

```
SELECT 
    jo.publication_date, 
    c.name AS company_name, 
    d.name AS department, 
    r.name AS role_name,
    jo.description
FROM Job_offer jo
JOIN Department d ON jo.department_id = d.department_id
JOIN Company c ON d.company_id = c.company_id
JOIN Role r ON jo.role_id = r.role_id
WHERE d.department_id IN (
    SELECT au.department_id
    FROM AI_usage au
    JOIN AI_tool t ON au.ai_tool_id = t.ai_tool_id
    WHERE t.name = 'ChatGPT'
)
ORDER BY jo.publication_date DESC;
```