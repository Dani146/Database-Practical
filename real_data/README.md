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

### Dataset 2 — AutoVenture AI Tools

- **Source:** https://github.com/autoventure-projects/ai-tools-dataset
- **Publisher:** AutoVenture
- **Publication:** Publicly announced June 24, 2026
- **License:** CC BY 4.0
- **Format:** CSV

The dataset contains information about AI tools currently available on the market.

We only kept the tool names and generated unique IDs, since additional information such as software versions was not consistently available.

## 2. Why We Chose These Datasets

We chose these datasets because they cover different parts of our database.

They are also relevant to our project, which focuses on employment and AI adoption. Although the datasets do not directly show how AI affects employment, they provide real-world information for testing our database.

## 3. Data Cleaning and Transformation

Before using the data, we needed to make a few changes to match our database schema.

### Missing Values

In the job offers dataset, some records did not contain publication dates.

We discarded rows with a missing publication date.

The original dataset also did not provide department IDs or job descriptions. Since we could not obtain this information, we simply created departments for each company in this dataset named after the company itself to maintain compatibility with our schema.

For the AI tools dataset, we didn't managed to fill the `version` column because version information was not available, so they were left as `NULL`.

### Date Formatting

The job publication dates follow the `YYYY-MM-DD` format, which is compatible with the SQL `DATE` data type.

We kept this format during data preparation. Missing dates were discarded.

### Duplicate Records

The original job dataset contained 6,308 identical rows.

To reduce duplicates, we compared records based on company name, job title, and publication date. We then selected 10,000 records from the remaining data.

We also extracted unique company names and job titles into separate tables to avoid storing the same information repeatedly.

For the AI tools dataset, we checked for duplicate names and kept 120 unique tools.

One limitation is that different job advertisements can have the same company, title, and publication date, so our method might occasionally treat separate vacancies as duplicates.

### Inconsistent Naming

Some company names and job titles had differences in capitalization or formatting.

We removed unnecessary whitespace but generally kept the original spelling and capitalization to avoid accidentally changing company names or merging different job titles.

## 4. Database Integration

The script used for this lives in `./populate.py`

## 6. Limitations

The main limitation is that the datasets do not provide information about individual employees, internal company departments, or which AI tools are actually used by specific companies.

Because this information is difficult to find in publicly available datasets, we can't fill all the tables in our database with relevant real-world data. This means the queries are limited to only the tables we can fill and cross-reference from the given data, otherwise we also have a small sample of synthetic data specifically for exploring the whole range of the ERD capabilities.

The two real-world datasets are therefore used for the `Company`, `Role`, `Job_offer`, and `AI_tool` tables, while the remaining tables contain generated records for testing purposes.
