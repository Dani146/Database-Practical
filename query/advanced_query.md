#Advanced queries for the database

## Selecting employees having a contract period above the average

```
SELECT 
    e.employee_id, 
    r.name AS role_name, 
    d.name AS department_name, 
    e.end_reason,
    (e.end_time - e.start_time) AS duration
FROM Employee e
JOIN Role r ON e.role_id = r.role_id
JOIN Department d ON e.department_id = d.department_id
WHERE e.end_time IS NOT NULL 
  AND (e.end_time - e.start_time) > (
      SELECT AVG(end_time - start_time) 
      FROM Employee 
      WHERE end_time IS NOT NULL
  )
ORDER BY duration DESC;
```

## Proportion of AI tools in the department compared to the company

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

## Job offers in departments already using ChatGPT

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

## The latest integrated AI tool by department

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

## Companies with "ghost" departments without active employees

```
SELECT DISTINCT c.name AS company_name, d.name AS empty_department
FROM Company c
JOIN Department d ON c.company_id = d.company_id
WHERE d.department_id NOT IN (
    SELECT department_id 
    FROM Employee 
    WHERE end_time IS NULL
)
ORDER BY company_name;
```