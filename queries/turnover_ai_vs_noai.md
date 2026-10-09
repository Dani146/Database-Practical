## Turnover rate comparison between AI-equipped and non-AI-equipped departments

**Description:** This query answers the question: _"Do departments using AI have a higher employee turnover rate than those without AI?"_ It calculates and compares the percentage of departures, helping to understand if AI integration correlates with job instability or workforce reduction.

Written by Adrien

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
