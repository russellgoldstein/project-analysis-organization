---
description: Ask natural language questions about the project - answers based on knowledge base
allowed-tools: Grep, Glob, Read
argument-hint: <question>
---

# Ask Questions About the Project

Ask natural language questions and get answers based on the knowledge base.

## Arguments

`$ARGUMENTS` - Your question in natural language

## Examples

```bash
/ask Who is working on authentication?
/ask What was decided about the database migration?
/ask What are the current blockers?
/ask What does DAG mean in this project?
/ask What happened in last week's sprint review?
```

## Task

### 1. Analyze the Question

Identify question type and key terms:

**Question Types:**
- **Who**: Person-related → search `knowledge/people/`, task assignees
- **What decided/agreed**: Decision-related → search `knowledge/project-status/`, summaries
- **What is/means**: Definition-related → search `knowledge/definitions/`
- **What are tasks/blockers**: Task-related → search `knowledge/tasks/`
- **When/timeline**: Date-related → search for dates in status, tasks
- **How**: Process-related → search `knowledge/wiki/`
- **Status/progress**: Status-related → search `knowledge/project-status/`

### 2. Search Relevant Sources

Based on question type, search appropriate directories:

1. Extract key terms from question
2. Search in relevant knowledge base sections
3. Also search `processed/` for recent context
4. Gather matching content

### 3. Synthesize Answer

Using the gathered context:

1. Read the most relevant files completely
2. Synthesize an answer to the question
3. Cite sources for each piece of information

### 4. Format Response

```
## Answer

[Natural language answer to the question]

### Details

[Additional context or elaboration]

### Sources

- [knowledge/people/john-smith.md](knowledge/people/john-smith.md) - Person profile
- [processed/2024-01-15-zoom-sprint.md](processed/2024-01-15-zoom-sprint.md) - Sprint review meeting

### Related

You might also want to know:
- [Related topic 1]
- [Related topic 2]
```

## Question Handling Examples

### "Who is working on authentication?"

1. Search `knowledge/tasks/` for "authentication"
2. Extract assignees from matching tasks
3. Look up those people in `knowledge/people/`
4. Answer: "John Smith is the primary assignee for authentication tasks. He's working on OAuth implementation (due Jan 25). Jane Doe is reviewing."

### "What was decided about the API?"

1. Search `knowledge/project-status/` for "API" and "decided"
2. Search processed docs for "API" + decision indicators
3. Answer with decisions found, including dates and who decided

### "What does ETL mean?"

1. Search `knowledge/definitions/` for "ETL"
2. If found, return the definition
3. If not found: "ETL is not yet defined in the knowledge base. Based on context from [docs], it likely refers to Extract, Transform, Load."

## No Answer Handling

If unable to find relevant information:

```
I couldn't find information about that in the knowledge base.

**Searched:**
- knowledge/tasks/ - No matches
- knowledge/project-status/ - No matches
- processed/ - No matches

**Suggestions:**
- Try rephrasing your question
- Use /search for keyword search
- The information may not have been processed yet
```
