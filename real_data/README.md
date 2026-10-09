# Real-World Data

## 1. Data Sources

For our database, we used two publicly available datasets containing information about job offers, companies, job roles, and AI tools.

### Dataset 1 — Lynceus Open Job Index

- **Source:** https://huggingface.co/datasets/Lynceus/jobs
- **Publisher:** Lynceus
- **Publication date:** October 5, 2026
- **License:** CC BY 4.0
- **Format:** CSV

The original dataset contains around 234,000 job offers from more than 6,000 companies. It includes company names, job titles, locations, publication dates, and information about remote work.

We selected 10,000 job offers and divided the data into three CSV files to match our database structure:

| File | Number of records |
|---|---:|
| `companies.csv` | 3,277 |
| `roles.csv` | 9,198 |
| `job_offers.csv` | 10,000 |

These files are used to populate the `Company`, `Role`, and `Job_offer` tables.

### Dataset 2 — AutoVenture AI Tools

- **Source:** https://github.com/autoventure-projects/ai-tools-dataset
- **Publisher:** AutoVenture
- **Publication:** Publicly announced June 24, 2026
- **License:** CC BY 4.0
- **Format:** CSV

The second dataset contains information about AI tools currently available on the market. From the original dataset, we selected 120 different tools to populate our `AI_tool` table.

We only kept the tool names and generated unique IDs, since additional information such as software versions was not consistently available.

Both datasets are free to download, do not require registration, and contain more than 50 unique records.

## 2. Why We Chose These Datasets

We chose these datasets because they cover different parts of our database.

They are also relevant to our project, which focuses on employment and AI adoption. Although the datasets do not directly show how AI affects employment, they provide real-world information for testing our database.

## 3. Data Cleaning and Transformation

Before using the data, we needed to make a few changes to match our database schema.

### Missing Values

In the job offers dataset, some records did not contain publication dates. Out of the 10,000 selected job offers, 614 had missing dates.

We left these fields empty rather than generating dates, so they can be stored as `NULL` in SQL.

The original dataset also did not provide department IDs or job descriptions. Since we could not obtain this information, we removed these columns from our simplified `Job_offer` table.

For the AI tools dataset, we removed the `version` column because version information was not consistently available.

### Date Formatting

The job publication dates follow the `YYYY-MM-DD` format, which is compatible with the SQL `DATE` data type.

We kept this format during data preparation. Missing dates were left empty.

The AI tools dataset does not contain any date fields that we needed for our database.

### Duplicate Records

The original job dataset contained 6,308 identical rows.

To reduce duplicates, we compared records based on company name, job title, and publication date. We then selected 10,000 records from the remaining data.

We also extracted unique company names and job titles into separate tables to avoid storing the same information repeatedly.

For the AI tools dataset, we checked for duplicate names and kept 120 unique tools.

One limitation is that different job advertisements can have the same company, title, and publication date, so our method might occasionally treat separate vacancies as duplicates.

### Inconsistent Naming

Some company names and job titles had differences in capitalization or formatting.

We removed unnecessary whitespace but generally kept the original spelling and capitalization to avoid accidentally changing company names or merging different job titles.

We also checked the AI tool names for duplicates caused by capitalization differences.

## 4. Database Integration

We reorganized the original data into separate tables to match our ERD.

| Table | Attributes |
|---|---|
| Company | `company_id`, `name` |
| Role | `role_id`, `name` |
| Job_offer | `job_offer_id`, `company_id`, `role_id`, `publication_date` |
| AI_tool | `ai_tool_id`, `name` |

We generated primary keys for each table and connected job offers to their corresponding companies and roles using foreign keys.

We also made a few changes to our original schema. We added `company_id` to `Job_offer` and removed `department_id` and `description`. We also removed `version` from `AI_tool`.

The cleaned CSV files are prepared for import into our SQL database. After importing them, we still need to run our queries again and check that the constraints work correctly.

## 5. Schema Constraints and Normalization


## 6. Limitations

The main limitation is that the datasets do not provide information about individual employees, internal company departments, or which AI tools are actually used by specific companies.

Because this information is difficult to find in publicly available datasets, we created synthetic data for the `Employee`, `Department`, and `AI_usage` tables.

These records are only used to test the database and do not represent real employees or confirmed AI usage.

The two real-world datasets are therefore used for the `Company`, `Role`, `Job_offer`, and `AI_tool` tables, while the remaining tables contain fictional records for testing purposes.
