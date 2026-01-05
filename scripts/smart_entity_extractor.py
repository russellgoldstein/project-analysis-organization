#!/usr/bin/env python3
"""
Smart entity extractor that uses contextual patterns to extract people and terms.
Project-agnostic - works with any document set.
"""

import sys
import re
from pathlib import Path
from collections import Counter


# Pronouns and common words to filter out
PRONOUNS = {'he', 'she', 'they', 'it', 'we', 'i', 'you', 'who', 'what', 'that', 'this', 'there'}

# Common false positive words (not people names)
COMMON_FALSE_POSITIVES = {
    'the', 'and', 'for', 'but', 'not', 'all', 'can', 'had', 'her', 'was', 'one', 'our',
    'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old',
    'see', 'two', 'way', 'any', 'boy', 'did', 'own', 'say', 'too', 'use', 'just', 'know',
    'take', 'come', 'made', 'find', 'here', 'many', 'make', 'like', 'time', 'very',
    'after', 'most', 'also', 'back', 'been', 'well', 'before', 'should', 'through',
    'first', 'where', 'about', 'being', 'could', 'going', 'great', 'might', 'never',
    'right', 'still', 'think', 'those', 'three', 'under', 'using', 'would', 'based',
    'other', 'these', 'which', 'while', 'after', 'again', 'below', 'every', 'their',
    # Common sentence starters that aren't names
    'however', 'therefore', 'meanwhile', 'furthermore', 'additionally', 'basically',
    'essentially', 'currently', 'finally', 'initially', 'overall', 'specifically',
    # Meeting/document structure words
    'meeting', 'notes', 'questions', 'points', 'summary', 'agenda', 'action', 'items',
    'transcript', 'outline', 'discussion', 'overview', 'talking', 'open', 'key',
    # Common filler/response words
    'yeah', 'okay', 'yes', 'no', 'sure', 'sorry', 'thanks', 'thank', 'right', 'let',
    'then', 'team', 'staff', 'software', 'engineer', 'senior', 'junior', 'manager',
}

# Words that indicate the "name" is actually a title/role, not a person
ROLE_WORDS = {
    'staff', 'senior', 'junior', 'lead', 'principal', 'engineer', 'manager', 'director',
    'analyst', 'developer', 'architect', 'consultant', 'specialist', 'coordinator',
    'software', 'data', 'product', 'project', 'program', 'technical', 'qa', 'devops',
}

# Words that shouldn't be the second part of a name
INVALID_NAME_ENDINGS = {
    # Filler/response words
    'yeah', 'okay', 'yes', 'no', 'so', 'sorry', 'thanks', 'well', 'right', 'um', 'uh',
    'oh', 'hi', 'hey', 'hello', 'bye', 'will', 'can', 'would', 'could', 'should',
    'cool', 'nice', 'great', 'good', 'fine', 'sure', 'yep', 'nope', 'actually',
    'exactly', 'basically', 'definitely', 'absolutely', 'probably', 'maybe',
    'everyone', 'anyone', 'someone', 'nobody', 'everybody', 'to', 'is', 'are',
    'yet', 'or', 'if', 'then', 'when', 'where', 'what', 'why', 'how',
    'exciting', 'awesome', 'look', 'discussed', 'iceberg', 'spark', 'kafka',
    # Document structure words
    'questions', 'points', 'notes', 'items', 'summary', 'transcript', 'meeting',
    'steps', 'context', 'date', 'problem', 'principles', 'walkthrough', 'practices',
    'risks', 'requirements', 'overview', 'discussion', 'decisions', 'blockers',
    'architecture', 'hydrant', 'ticket',
    # Technical terms that aren't last names
    'watermark', 'pipeline', 'layer', 'table', 'schema', 'database', 'cluster',
    'bucket', 'stream', 'query', 'model', 'service', 'process', 'job', 'task',
    'config', 'configuration', 'setup', 'deployment', 'environment', 'instance',
}

# Words that shouldn't be the first part of a name
INVALID_NAME_STARTS = {
    'next', 'business', 'due', 'architectural', 'document', 'list', 'best',
    'open', 'key', 'main', 'current', 'new', 'old', 'high', 'low', 'full',
    'initial', 'final', 'total', 'complete', 'partial', 'additional',
    'medallion', 'fire', 'some', 'have', 'be', 'fq', 'topics', 'apache', 'of',
}

# Known first names (to detect "FirstName FirstName" patterns)
# This helps filter cases like "Danyil Sunny" where both are first names
KNOWN_FIRST_NAMES = {
    'russ', 'phil', 'lokesh', 'zee', 'sunny', 'danyil', 'phuc', 'samer', 'ankit',
    'marc', 'tom', 'michael', 'brian', 'sreehari', 'mubee', 'luke', 'lawrence',
    'poorna', 'rebecca', 'richard', 'yogi', 'raghvendra', 'victoria', 'ryan',
    'jessica', 'david', 'tony', 'zeeshan',
}

# Speaking verbs that indicate a person is speaking
SPEAKING_VERBS = [
    'said', 'says', 'asked', 'asks', 'explained', 'explains', 'mentioned', 'mentions',
    'stated', 'states', 'confirmed', 'confirms', 'noted', 'notes', 'suggested', 'suggests',
    'agreed', 'agrees', 'responded', 'responds', 'clarified', 'clarifies', 'inquired',
    'inquires', 'acknowledged', 'acknowledges', 'greeted', 'greets', 'thanked', 'thanks',
    'added', 'adds', 'replied', 'replies', 'discussed', 'discusses', 'described',
    'describes', 'demonstrated', 'demonstrates', 'showed', 'shows', 'pointed', 'points',
    'continued', 'continues', 'interrupted', 'interrupts', 'concluded', 'concludes',
    'proposed', 'proposes', 'recommended', 'recommends', 'emphasized', 'emphasizes',
    'highlighted', 'highlights', 'announced', 'announces', 'reported', 'reports',
    'observed', 'observes', 'commented', 'comments', 'questioned', 'questions',
    'answered', 'answers', 'elaborated', 'elaborates', 'reiterated', 'reiterates',
    'summarized', 'summarizes', 'outlined', 'outlines', 'expressed', 'expresses',
    'indicated', 'indicates', 'informed', 'informs', 'conveyed', 'conveys',
    'shared', 'shares', 'revealed', 'reveals', 'admitted', 'admits'
]

# Common acronym false positives
ACRONYM_FALSE_POSITIVES = {
    'AM', 'PM', 'OK', 'VS', 'IE', 'EG', 'ET', 'AL', 'RE', 'FW', 'CC', 'BCC',
    'II', 'III', 'IV', 'VI', 'VII', 'VIII', 'IX', 'XI', 'XII',  # Roman numerals
    'MB', 'GB', 'TB', 'KB', 'MS',  # File sizes and milliseconds
    'MR', 'DR', 'JR', 'SR',  # Titles
    'US', 'UK', 'EU', 'UN',  # Countries/orgs
    'ID',  # Too generic
    'HI', 'BY', 'TO', 'UP', 'IN', 'ON', 'AT', 'AS', 'IS', 'IT', 'OR', 'AN',
    'BE', 'DO', 'GO', 'IF', 'MY', 'NO', 'SO', 'WE', 'HE', 'ME',
    'V1', 'V2', 'V3', 'V4', 'V5',  # Version numbers
    'PR',  # Too ambiguous (Pull Request vs generic)
    'AI',  # Too generic unless in ML context
    'TLC',  # Often meaningless
}


def extract_speakers_from_content(content):
    """Extract people names from speaker patterns in document content."""
    speakers = Counter()

    # Build regex pattern for speaking verbs
    verb_pattern = '|'.join(SPEAKING_VERBS)

    # Pattern: "Name (verb)" - captures first name before speaking verb
    pattern = rf'\b([A-Z][a-z]+)\s+(?:{verb_pattern})\b'

    for match in re.finditer(pattern, content, re.IGNORECASE):
        name = match.group(1)
        if name.lower() not in PRONOUNS and name.lower() not in COMMON_FALSE_POSITIVES:
            speakers[name] += 1

    # Also look for "Name's" pattern (possessive indicating person)
    pattern2 = r"\b([A-Z][a-z]+)'s\b"
    for match in re.finditer(pattern2, content):
        name = match.group(1)
        if name.lower() not in PRONOUNS and name.lower() not in COMMON_FALSE_POSITIVES:
            # Give less weight to possessives
            speakers[name] += 0.5

    return speakers


def extract_full_names(content):
    """Extract full names (First Last) that appear in content."""
    full_names = Counter()

    # Pattern for First Last (and optionally Middle)
    pattern = r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)(?:\s+([A-Z][a-z]+))?\b'

    for match in re.finditer(pattern, content):
        first = match.group(1)
        last = match.group(2)
        middle = match.group(3)

        # Skip if any part is a common word
        if first.lower() in COMMON_FALSE_POSITIVES or last.lower() in COMMON_FALSE_POSITIVES:
            continue
        if first.lower() in PRONOUNS or last.lower() in PRONOUNS:
            continue

        # Skip if last name is a filler word (e.g., "Phil Yeah")
        if last.lower() in INVALID_NAME_ENDINGS:
            continue

        # Skip if first name is a role word (e.g., "Staff Engineer")
        if first.lower() in ROLE_WORDS:
            continue

        # Skip if last name is a role word (e.g., "Senior Engineer")
        if last.lower() in ROLE_WORDS:
            continue

        # Skip if first name is an invalid start (e.g., "Next Steps")
        if first.lower() in INVALID_NAME_STARTS:
            continue

        # Skip if both parts are known first names (e.g., "Danyil Sunny")
        if first.lower() in KNOWN_FIRST_NAMES and last.lower() in KNOWN_FIRST_NAMES:
            continue

        # Build full name
        if middle and middle.lower() not in COMMON_FALSE_POSITIVES and middle.lower() not in INVALID_NAME_ENDINGS:
            # Skip if middle is a role/filler
            if middle.lower() in ROLE_WORDS or middle.lower() in INVALID_NAME_ENDINGS:
                full_name = f"{first} {last}"
            else:
                full_name = f"{first} {middle} {last}"
        else:
            full_name = f"{first} {last}"

        # Final validation - both parts should be reasonable lengths for names
        parts = full_name.split()
        if all(2 <= len(p) <= 15 for p in parts):
            full_names[full_name] += 1

    return full_names


def extract_acronyms(content, min_occurrences=5):
    """Extract meaningful acronyms from content."""
    acronyms = Counter()

    # Pattern for acronyms (2-6 uppercase letters, optionally with numbers)
    pattern = r'\b([A-Z][A-Z0-9]{1,5})\b'

    for match in re.finditer(pattern, content):
        acronym = match.group(1)

        # Skip false positives
        if acronym in ACRONYM_FALSE_POSITIVES:
            continue

        # Skip if too short (single letter) or contains only numbers
        if len(acronym) < 2 or acronym.isdigit():
            continue

        acronyms[acronym] += 1

    # Return only those with sufficient occurrences
    return Counter({k: v for k, v in acronyms.items() if v >= min_occurrences})


def extract_technical_phrases(content, min_occurrences=3):
    """Extract multi-word technical phrases."""
    phrases = Counter()

    # Common technical phrase patterns
    phrase_patterns = [
        r'\b(Data\s+Federation)\b',
        r'\b(Stream\s+Processing)\b',
        r'\b(Change\s+Data\s+Capture)\b',
        r'\b(Data\s+Lake(?:house)?)\b',
        r'\b(Apache\s+(?:Iceberg|Spark|Kafka|Hudi|Hadoop|Parquet|Avro))\b',
        r'\b(Medallion\s+Architecture)\b',
        r'\b(Bronze|Silver|Gold)\s+(?:Layer|Table|Zone|Data)\b',
        r'\b((?:Bronze|Silver|Gold))\b',  # Just the layer names
        r'\b(Full\s+Load)\b',
        r'\b(Initial\s+Sync)\b',
        r'\b(Data\s+Pipeline)\b',
        r'\b(Data\s+Warehouse)\b',
        r'\b(Machine\s+Learning)\b',
        r'\b(Continuous\s+Integration)\b',
        r'\b(Continuous\s+Delivery)\b',
        r'\b(Infrastructure\s+as\s+Code)\b',
        r'\b(Version\s+Control)\b',
        r'\b(Pull\s+Request)\b',
        r'\b(Code\s+Review)\b',
        r'\b(Unit\s+Test(?:ing)?)\b',
        r'\b(Integration\s+Test(?:ing)?)\b',
        r'\b(Load\s+Test(?:ing)?)\b',
        r'\b(Schema\s+Evolution)\b',
        r'\b(Time\s+Travel)\b',
        r'\b(Batch\s+Processing)\b',
        r'\b(Real[\s-]?[Tt]ime\s+Processing)\b',
    ]

    for pattern in phrase_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            phrase = match.group(1)
            # Normalize to title case
            phrase = ' '.join(word.capitalize() for word in phrase.split())
            phrases[phrase] += 1

    return Counter({k: v for k, v in phrases.items() if v >= min_occurrences})


def extract_defined_terms(content):
    """Extract terms that are explicitly defined (e.g., 'CDC (Change Data Capture)')."""
    defined_terms = {}

    # Pattern: ACRONYM (Full Definition)
    pattern = r'\b([A-Z]{2,6})\s*\(([^)]+)\)'

    for match in re.finditer(pattern, content):
        acronym = match.group(1)
        definition = match.group(2).strip()

        # Skip if definition is too short or too long
        if len(definition) < 5 or len(definition) > 100:
            continue

        # Skip if definition looks like a version number or code
        if re.match(r'^v?\d+', definition) or re.match(r'^[\d\.\-\/]+$', definition):
            continue

        # Skip if definition starts with lowercase (likely not a proper definition)
        if definition[0].islower():
            continue

        # Skip if definition contains code-like patterns
        if any(c in definition for c in ['=', '{', '}', '[', ']', '<', '>', '/', '\\']):
            continue

        # Skip common false positives
        if acronym in ACRONYM_FALSE_POSITIVES:
            continue

        # Only keep if definition looks like words (contains spaces or is a proper noun)
        if ' ' in definition or definition[0].isupper():
            if acronym not in defined_terms:
                defined_terms[acronym] = definition

    return defined_terms


def extract_product_names(content, min_occurrences=5):
    """Extract product/technology names."""
    products = Counter()

    # Common product/tech name patterns
    product_patterns = [
        r'\b(MongoDB)\b',
        r'\b(Terraform)\b',
        r'\b(Snowflake)\b',
        r'\b(Databricks)\b',
        r'\b(Fivetran)\b',
        r'\b(Confluent)\b',
        r'\b(Kubernetes)\b',
        r'\b(Docker)\b',
        r'\b(Jenkins)\b',
        r'\b(GitHub)\b',
        r'\b(GitLab)\b',
        r'\b(Jira)\b',
        r'\b(Confluence)\b',
        r'\b(Slack)\b',
        r'\b(Python)\b',
        r'\b(Scala)\b',
        r'\b(Java)\b',
        r'\b(Spark)\b',
        r'\b(Iceberg)\b',
        r'\b(Parquet)\b',
        r'\b(Hadoop)\b',
        r'\b(PySpark)\b',
        r'\b(DataFrame)\b',
        r'\b(Atlas)\b',
        r'\b(Octa)\b',
        r'\b(Netflix)\b',  # Often mentioned as Iceberg origin
    ]

    for pattern in product_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            product = match.group(1)
            # Normalize capitalization
            products[product.title() if product.lower() != 'pyspark' else 'PySpark'] += 1

    return Counter({k: v for k, v in products.items() if v >= min_occurrences})


def process_documents(project_dir):
    """Process all documents in a project directory."""
    project_dir = Path(project_dir).expanduser()
    processed_dir = project_dir / 'processed'

    if not processed_dir.exists():
        print(f"Error: processed/ directory not found in {project_dir}")
        return None, None

    # Combine all document content
    all_content = ""
    doc_count = 0

    for doc in processed_dir.glob('*.md'):
        try:
            content = doc.read_text(encoding='utf-8')
            # Skip frontmatter
            if content.startswith('---'):
                end = content.find('\n---\n', 3)
                if end > 0:
                    content = content[end + 5:]
            all_content += "\n\n" + content
            doc_count += 1
        except Exception as e:
            print(f"Warning: Could not read {doc.name}: {e}")

    print(f"Processed {doc_count} documents")

    # Extract entities
    print("\nExtracting people...")
    speakers = extract_speakers_from_content(all_content)
    full_names = extract_full_names(all_content)

    print("Extracting technical terms...")
    acronyms = extract_acronyms(all_content, min_occurrences=10)
    phrases = extract_technical_phrases(all_content, min_occurrences=5)
    defined_terms = extract_defined_terms(all_content)
    products = extract_product_names(all_content, min_occurrences=10)

    # Combine people (prefer full names when available)
    people = {}

    # First, add speakers (first names)
    for name, count in speakers.items():
        if count >= 5:  # Minimum threshold
            people[name] = {'count': int(count), 'type': 'first_name'}

    # Then, try to match with full names
    for full_name, count in full_names.items():
        if count >= 2:
            parts = full_name.split()
            first_name = parts[0]

            # If we have this first name, upgrade to full name
            if first_name in people:
                people[full_name] = {
                    'count': people[first_name]['count'] + count,
                    'type': 'full_name',
                    'first_name': first_name
                }
                del people[first_name]
            else:
                people[full_name] = {'count': count, 'type': 'full_name'}

    # Combine terms
    terms = {}

    # Add acronyms
    for acronym, count in acronyms.items():
        definition = defined_terms.get(acronym, '')
        terms[acronym] = {
            'count': count,
            'type': 'acronym',
            'definition': definition
        }

    # Add phrases
    for phrase, count in phrases.items():
        terms[phrase] = {'count': count, 'type': 'phrase'}

    # Add products
    for product, count in products.items():
        if product not in terms:  # Don't duplicate
            terms[product] = {'count': count, 'type': 'product'}

    return people, terms


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 smart_entity_extractor.py <project_dir>")
        sys.exit(1)

    project_dir = Path(sys.argv[1]).expanduser()

    print(f"\nSmart Entity Extraction")
    print(f"=======================")
    print(f"Project: {project_dir}")

    people, terms = process_documents(project_dir)

    if people is None:
        sys.exit(1)

    # Sort by count
    sorted_people = sorted(people.items(), key=lambda x: x[1]['count'], reverse=True)
    sorted_terms = sorted(terms.items(), key=lambda x: x[1]['count'], reverse=True)

    print(f"\n\n=== PEOPLE FOUND ({len(sorted_people)}) ===\n")
    for name, info in sorted_people[:30]:
        name_type = info['type']
        count = info['count']
        print(f"  {name:<25} ({count:>4} mentions, {name_type})")

    if len(sorted_people) > 30:
        print(f"  ... and {len(sorted_people) - 30} more")

    print(f"\n\n=== TECHNICAL TERMS ({len(sorted_terms)}) ===\n")
    for term, info in sorted_terms[:40]:
        term_type = info['type']
        count = info['count']
        definition = info.get('definition', '')
        if definition:
            print(f"  {term:<25} ({count:>4}x) = {definition}")
        else:
            print(f"  {term:<25} ({count:>4}x, {term_type})")

    if len(sorted_terms) > 40:
        print(f"  ... and {len(sorted_terms) - 40} more")

    # Save results
    output_file = project_dir / 'extracted_entities.md'

    with open(output_file, 'w') as f:
        f.write("# Extracted Entities\n\n")
        f.write(f"*Generated from {len(list((project_dir / 'processed').glob('*.md')))} documents*\n\n")

        f.write("## People\n\n")
        f.write("| Name | Mentions | Type |\n")
        f.write("|------|----------|------|\n")
        for name, info in sorted_people:
            f.write(f"| {name} | {info['count']} | {info['type']} |\n")

        f.write("\n## Technical Terms\n\n")
        f.write("| Term | Mentions | Type | Definition |\n")
        f.write("|------|----------|------|------------|\n")
        for term, info in sorted_terms:
            definition = info.get('definition', '')
            f.write(f"| {term} | {info['count']} | {info['type']} | {definition} |\n")

    print(f"\n\nResults saved to: {output_file}")

    return people, terms


if __name__ == '__main__':
    main()
