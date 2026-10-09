# Selecting employees having a contract period above the average

**Description:** This query answers the question: _"Which former employees stayed at the company longer than the historical average?"_ It calculates the exact duration of each past employee's contract and retrieves only those whose tenure is strictly greater than the overall average time worked by all former employees.

Written by Adrien

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
