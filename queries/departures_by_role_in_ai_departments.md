## Employee departures by role in AI-driven departments

**Description:** This query answers the question: "Which specific roles are experiencing the most contract terminations or resignations in departments that use AI?" This highlights if certain jobs (like secretaries or basic administrative roles) are more vulnerable to being replaced by artificial intelligence.

Written by Adrien

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