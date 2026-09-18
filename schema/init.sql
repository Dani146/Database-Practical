CREATE TABLE Company (
    company_id INT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE Department (
    department_id INT PRIMARY KEY,
    name VARCHAR(50),
    company_id INT,
    FOREIGN KEY (company_id) REFERENCES Company(company_id)
);

CREATE TABLE Role (
    role_id INT PRIMARY KEY,
    name VARCHAR(40)
);

CREATE TABLE Employee (
    employee_id INT PRIMARY KEY,
    department_id INT,
    role_id INT,
    start_time DATE,
    end_time DATE,
    end_reason VARCHAR(255),
    FOREIGN KEY (department_id) REFERENCES Department(department_id),
    FOREIGN KEY (role_id) REFERENCES Role(role_id)
);

CREATE TABLE Job_offer (
    job_offer_id INT PRIMARY KEY,
    department_id INT,
    role_id INT,
    publication_date DATE,
    description TEXT,
    FOREIGN KEY (department_id) REFERENCES Department(department_id),
    FOREIGN KEY (role_id) REFERENCES Role(role_id)
);

CREATE TABLE AI_tool (
    ai_tool_id INT PRIMARY KEY,
    name VARCHAR(50),
    version VARCHAR(30)
);

CREATE TABLE AI_usage (
    ai_usage_id INT PRIMARY KEY,
    department_id INT,
    ai_tool_id INT,
    integration_date DATE,
    FOREIGN KEY (department_id) REFERENCES Department(department_id),
    FOREIGN KEY (ai_tool_id) REFERENCES AI_tool(ai_tool_id)
);