# Advanced queries for the database

## Selecting employees having a contract period above the average

**Description:** This query answers the question: *"Which former employees stayed at the company longer than the historical average?"* It calculates the exact duration of each past employee's contract and retrieves only those whose tenure is strictly greater than the overall average time worked by all former employees.

Wrote by Adrien

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

**Description:** This query allows us to see which departments use more AI tools than others. It answers the question: "How many AI tools are used by a specific department compared to the total number of AI tools deployed across the entire company?" It is very useful to identify which teams are driving AI adoption.

Wrote by Adrien

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
**Description:** This query answers the question: "What are the current open job positions in departments that have already integrated ChatGPT into their workflow?" It helps target recruitment needs for teams that are already familiar with this specific generative AI tool.

Wrote by Matiss

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
**Description:** This query answers the question: "What is the most recently adopted AI tool in each department, and when was it integrated?" It allows management to track the latest technological updates and trends within every single team.

Wrote by Matiss

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

**Description:** This query answers the question: "Which departments currently have absolutely zero active employees?" It is designed to identify "ghost" departments in the database where all previous employees have either resigned or ended their contracts, leaving the department completely empty.

wrote by Danylo

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

## Turnover rate comparison between AI-equipped and non-AI-equipped departments

**Description:** This query answers the question: *"Do departments using AI have a higher employee turnover rate than those without AI?"* It calculates and compares the percentage of departures, helping to understand if AI integration correlates with job instability or workforce reduction.

Wrote by Adrien

```
SELECT 
    CASE WHEN au.department_id IS NOT NULL THEN 'With AI' ELSE 'Without AI' END AS ai_status,
    COUNT(DISTINCT e.employee_id) AS total_historical_employees,
    SUM(CASE WHEN e.end_time IS NOT NULL THEN 1 ELSE 0 END) AS total_departures,
    ROUND(
        (SUM(CASE WHEN e.end_time IS NOT NULL THEN 1 ELSE 0 END)::numeric / 
        NULLIF(COUNT(DISTINCT e.employee_id), 0)) * 100, 
    2) AS turnover_percentage
FROM Department d
LEFT JOIN (SELECT DISTINCT department_id FROM AI_usage) au ON d.department_id = au.department_id
LEFT JOIN Employee e ON d.department_id = e.department_id
GROUP BY CASE WHEN au.department_id IS NOT NULL THEN 'With AI' ELSE 'Without AI' END;
```

## Volume of job offers published before vs. after AI integration

**Description:** This query answers the question: "Does hiring increase or decrease after a department integrates AI?" It finds the earliest AI adoption date for each department and counts how many job offers were posted before that date versus after, highlighting the impact of AI on job creation.

Wrote by Danylo

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

## Employee departures by role in AI-driven departments

**Description:** This query answers the question: "Which specific roles are experiencing the most contract terminations or resignations in departments that use AI?" This highlights if certain jobs (like secretaries or basic administrative roles) are more vulnerable to being replaced by artificial intelligence.

Wrote by Adrien

```
SELECT 
    r.name AS role_name,
    COUNT(e.employee_id) AS total_departures_in_ai_depts
FROM Employee e
JOIN Role r ON e.role_id = r.role_id
WHERE e.end_time IS NOT NULL 
  AND e.department_id IN (SELECT DISTINCT department_id FROM AI_usage)
GROUP BY r.name
ORDER BY total_departures_in_ai_depts DESC;
```

## Demand for specific AI skills in job descriptions

**Description:** This query answers the question: "Are employers explicitly looking for AI skills in new hires?" It searches the text of job descriptions for mentions of known AI tools (like ChatGPT or Copilot), proving the emergence of new AI-centric requirements in the job market.

Wrote by Adrien

```
SELECT 
    t.name AS ai_tool,
    COUNT(jo.job_offer_id) AS offers_mentioning_tool
FROM AI_tool t
LEFT JOIN Job_offer jo ON jo.description ILIKE '%' || t.name || '%'
GROUP BY t.name
ORDER BY offers_mentioning_tool DESC;
```

## Immediate job displacement: Departures shortly after AI integration

**Description:** This query answers the question: "Are employees leaving their jobs shortly (within 6 months) after an AI tool is introduced in their team?" It tracks the direct short-term displacement effect by correlating the AI integration date with employee departure dates.

Wrote by Adrien

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

## Correlation between AI adoption level and active workforce size

**Description:** This query answers the question: "Do companies that adopt more AI tools employ fewer people overall?" It compares the total number of AI deployments against the total number of active employees in each company to spot macro-level trends between automation and human labor.

Wrote by Adrien

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