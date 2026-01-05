# Entity Extraction Improvements

## Problem Summary

The current entity extraction has significant false positives:

### People Extraction Issues
- Regex pattern `[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+` matches:
  - ✓ Real names: "Russ Goldstein", "Phil Edie"
  - ✗ Section headings: "Best Practices", "Bug Fix"
  - ✗ Product names: "Apache Iceberg", "Bronze Layer"
  - ✗ Phrases: "Before Thursday", "Both Lokesh"

### Definition Extraction Issues
- Pattern `[A-Z]{2,}` matches:
  - ✓ Real acronyms: "API", "AWS", "SQL"
  - ✗ Random letters: "ABC", "AD", "AM"
  - ✗ Common words: "AND", "OR", "THE"

## Root Cause

**Simple regex cannot understand context.** It can't tell if "Bronze Layer" is a person or a technical term, or if "AM" is a time indicator vs an acronym.

## Solutions

### Option 1: Use LLM-Based Subagents (Recommended)

The framework already has specialized subagents designed for this:
- `entity-extractor` - Uses LLM to understand context
- `document-analyzer` - Provides intelligent summarization
- `task-extractor` - Extracts tasks with understanding

**Pros:**
- Much higher accuracy
- Understands context
- Can extract roles, relationships, definitions with explanations

**Cons:**
- Slower (requires API calls)
- More expensive for large batches
- Requires Claude API access

**Implementation:**
- Modify `process` command to use Task tool with subagents
- Process documents in batches
- Use haiku model for cost optimization

### Option 2: Improved Heuristics (Current Approach)

Continue with regex but add better filters:

**Improvements Made:**
- ✓ Require 2+ occurrences (frequency filter)
- ✓ Minimum 3 characters for acronyms
- ✓ Blacklist common words
- ✓ Pattern matching for non-people (e.g., `*-layer`, `*-architecture`)

**Remaining Issues:**
- Still can't distinguish context
- Requires ongoing curation of blacklists
- Will always have some false positives

### Option 3: Manual Curation

Keep automated extraction but require manual review:

**Process:**
1. Auto-extract with current logic
2. Generate review list
3. User approves/rejects each entity
4. Only approved entities go to knowledge base

**Pros:**
- 100% accuracy after review
- User controls what's tracked

**Cons:**
- Time-intensive for large datasets
- Doesn't scale well

### Option 4: Hybrid Approach (Best of Both Worlds)

Combine automated extraction with sampling:

1. **Auto-extract** using improved heuristics
2. **Confidence scoring** - flag low-confidence extractions
3. **Sampling** - User reviews 10-20 samples
4. **Refinement** - Adjust filters based on sample feedback
5. **Re-run** with improved filters

## Recommendations

### For Current Project (fq-test)

1. **Immediate:** Delete remaining false positives
   ```bash
   # Manual cleanup of specific bad patterns
   rm knowledge/people/best-practices.md
   rm knowledge/people/bronze-*.md
   rm knowledge/people/before-*.md
   # ... etc
   ```

2. **Better:** Keep only names from participants list
   - Documents have `participants:` in frontmatter
   - Only create profiles for listed participants
   - Safer, higher confidence

3. **Best:** Re-run Stage 2 with LLM subagents
   - Delete current extractions
   - Re-process with entity-extractor subagent
   - Higher quality, context-aware extraction

### For Future Projects

**Default to LLM-based extraction** for best results:

```python
# In /process command
for doc in documents:
    # Use subagents instead of regex
    summary = Task(subagent='document-analyzer', doc=doc)
    tasks = Task(subagent='task-extractor', doc=doc)
    entities = Task(subagent='entity-extractor', doc=doc)
```

## Implementation Plan

### Quick Win: Participant-Only Extraction

Modify extraction to only track people from `participants:` frontmatter:

```python
def extract_people(body, frontmatter):
    """Extract only people listed in frontmatter participants."""
    participants = frontmatter.get('participants', [])

    # Filter out empty strings and None
    valid_participants = [p for p in participants if p and len(p) > 3]

    return valid_participants
```

**Benefits:**
- High confidence (explicitly listed)
- No false positives
- Fast, no LLM needed

### Better: Smart Frequency + Context

```python
def extract_people(body, frontmatter):
    """Extract people using frequency and context clues."""
    participants = frontmatter.get('participants', [])

    # Pattern for names near context words
    context_pattern = r'(?:said|asked|mentioned|noted|explained|stated)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)'

    contextual_names = re.findall(context_pattern, body)

    # Combine with participants
    all_names = set(participants + contextual_names)

    # Return only names appearing 3+ times
    name_counts = Counter(all_names)
    return [name for name, count in name_counts.items() if count >= 3 and is_valid_person_name(name)]
```

### Best: LLM-Based Extraction

```python
def process_document_with_llm(doc_path, project_dir):
    """Process using Claude subagents for high-quality extraction."""

    # Launch subagents in parallel
    results = parallel_tasks([
        Task(subagent='entity-extractor', prompt=f"Extract people and terms from {doc_path}"),
        Task(subagent='task-extractor', prompt=f"Extract tasks from {doc_path}"),
        Task(subagent='document-analyzer', prompt=f"Summarize {doc_path}")
    ])

    # Process results with context-aware filtering
    return create_extractions(results)
```

## Conclusion

**For project-analysis-organization framework:**
- Keep scripts agnostic (work with any project)
- Provide both regex and LLM options
- Default to safer, high-confidence extraction
- Make quality vs speed tradeoff configurable

**For user's fq-test project:**
- Clean up remaining false positives manually or with better script
- Consider re-running with LLM extraction for best quality
- Use participant-only extraction as safe default

## Files to Update

1. `scripts/process_documents.py` → Use participant-based extraction
2. `.claude/commands/process.md` → Add option for LLM vs regex extraction
3. `scripts/organize_extractions.py` → Add validation before creating KB entries
4. `.claude/skills/entity-extractor.md` → Document LLM-based extraction option
