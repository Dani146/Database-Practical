## Companies with "ghost" departments without active employees

**Description:** This query answers the question: "Which departments currently have absolutely zero active employees?" It is designed to identify "ghost" departments in the database where all previous employees have either resigned or ended their contracts, leaving the department completely empty.

Written by Danylo

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
