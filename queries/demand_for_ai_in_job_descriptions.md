## Demand for specific AI skills in job descriptions

**Description:** This query answers the question: "Are employers explicitly looking for AI skills in new hires?" It searches the text of job descriptions for mentions of known AI tools (like ChatGPT or Copilot), proving the emergence of new AI-centric requirements in the job market.

Written by Adrien

```
SELECT 
    t.name AS ai_tool,
    COUNT(jo.job_offer_id) AS offers_mentioning_tool
FROM AI_tool t
LEFT JOIN Job_offer jo ON jo.description ILIKE '%' || t.name || '%'
GROUP BY t.name
ORDER BY offers_mentioning_tool DESC;
```