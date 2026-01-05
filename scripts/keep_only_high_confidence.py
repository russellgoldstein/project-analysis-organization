#!/usr/bin/env python3
"""
Keep only high-confidence extractions.
- People: Only those listed in document participants
- Definitions: Only well-known technical terms
"""

import sys
import re
import yaml
from pathlib import Path
from collections import Counter


def read_frontmatter(file_path):
    """Extract YAML frontmatter from markdown file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        if not content.startswith('---'):
            return None

        end_match = re.search(r'\n---\n', content[3:])
        if not end_match:
            return None

        frontmatter_text = content[3:end_match.start() + 3]
        return yaml.safe_load(frontmatter_text)
    except:
        return None


# Well-known technical terms that are safe to keep
KNOWN_TECH_TERMS = {
    # Cloud/AWS
    'aws', 's3', 'ec2', 'rds', 'sqs', 'sns', 'iam', 'vpc', 'lambda', 'cloudformation',
    'cloudwatch', 'dynamodb', 'kinesis', 'glue', 'athena',

    # Apache
    'apache-iceberg', 'apache-kafka', 'apache-spark', 'apache-hadoop', 'apache-hudi',
    'apache-parquet', 'apache-avro',

    # Databases
    'mongodb', 'postgres', 'postgresql', 'mysql', 'mariadb', 'redis', 'cassandra',
    'elasticsearch', 'solr', 'couchdb', 'neo4j',

    # Data formats
    'json', 'xml', 'yaml', 'csv', 'parquet', 'avro', 'orc', 'protobuf', 'bson',

    # Protocols/APIs
    'api', 'rest', 'graphql', 'grpc', 'http', 'https', 'websocket', 'mqtt',
    'sql', 'nosql', 'crud', 'cors', 'jwt', 'oauth', 'saml', 'oidc',

    # DevOps
    'docker', 'kubernetes', 'k8s', 'helm', 'terraform', 'ansible', 'jenkins',
    'gitlab', 'github', 'bitbucket', 'circleci', 'travis-ci',

    # Data Engineering
    'etl', 'elt', 'olap', 'oltp', 'acid', 'cdc', 'change-data-capture',
    'medallion', 'lakehouse', 'data-lake', 'data-warehouse',

    # General IT
    'sdk', 'cli', 'api', 'url', 'uri', 'uuid', 'guid', 'rbac', 'saas', 'paas', 'iaas',
    'cicd', 'ci-cd', 'vpn', 'dns', 'ssl', 'tls', 'ssh', 'ftp', 'sftp',

    # Programming
    'oop', 'functional', 'async', 'await', 'promise', 'callback', 'event-loop',
    'thread', 'process', 'mutex', 'semaphore',

    # Monitoring/Security
    'monitoring', 'logging', 'metrics', 'tracing', 'alerting',
    'encryption', 'hashing', 'authentication', 'authorization'
}


def get_all_participants(processed_dir):
    """Get all people from participants frontmatter across all documents."""
    all_participants = set()

    for doc in processed_dir.glob('*.md'):
        fm = read_frontmatter(doc)
        if fm and 'participants' in fm:
            participants = fm['participants']
            if isinstance(participants, list):
                for p in participants:
                    if p and isinstance(p, str) and len(p) > 3:
                        all_participants.add(p)

    return all_participants


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 keep_only_high_confidence.py <project_dir>")
        sys.exit(1)

    project_dir = Path(sys.argv[1]).expanduser()
    kb_dir = project_dir / 'knowledge'
    processed_dir = project_dir / 'processed'

    if not kb_dir.exists():
        print("Error: knowledge/ directory not found")
        sys.exit(1)

    print("\nHigh-Confidence Extraction Filter")
    print("==================================\n")

    # Get all participants from documents
    if processed_dir.exists():
        print("Collecting participants from processed documents...")
        valid_participants = get_all_participants(processed_dir)
        print(f"Found {len(valid_participants)} unique participants\n")
    else:
        valid_participants = set()
        print("Warning: No processed/ directory found, using empty participant list\n")

    # Clean up people - keep only those in participants
    people_dir = kb_dir / 'people'
    if people_dir.exists():
        people_files = list(people_dir.glob('*.md'))
        kept_people = []
        removed_people = []

        for f in people_files:
            # Convert filename to display name
            display_name = f.stem.replace('-', ' ').title()

            # Check if this person is in participants
            if display_name in valid_participants:
                kept_people.append(f)
            else:
                removed_people.append(f)
                f.unlink()

        print(f"People Profiles:")
        print(f"  - Total: {len(people_files)}")
        print(f"  - Kept (in participants): {len(kept_people)}")
        print(f"  - Removed (not in participants): {len(removed_people)}")

        if kept_people:
            print(f"\n  Kept people:")
            for f in sorted(kept_people)[:10]:
                print(f"    - {f.stem.replace('-', ' ').title()}")
            if len(kept_people) > 10:
                print(f"    ... and {len(kept_people) - 10} more")

    # Clean up definitions - keep only known technical terms
    defs_dir = kb_dir / 'definitions'
    if defs_dir.exists():
        def_files = list(defs_dir.glob('*.md'))
        kept_defs = []
        removed_defs = []

        for f in def_files:
            # Check if this is a known technical term
            if f.stem.lower() in KNOWN_TECH_TERMS:
                kept_defs.append(f)
            else:
                removed_defs.append(f)
                f.unlink()

        print(f"\nDefinitions:")
        print(f"  - Total: {len(def_files)}")
        print(f"  - Kept (known tech terms): {len(kept_defs)}")
        print(f"  - Removed (unknown/uncertain): {len(removed_defs)}")

        if kept_defs:
            print(f"\n  Kept definitions:")
            for f in sorted(kept_defs)[:15]:
                print(f"    - {f.stem}")
            if len(kept_defs) > 15:
                print(f"    ... and {len(kept_defs) - 15} more")

    # Summary
    print(f"\n\nCleanup Complete")
    print(f"================")
    people_kept = len(kept_people) if 'kept_people' in locals() else 0
    defs_kept = len(kept_defs) if 'kept_defs' in locals() else 0

    print(f"\nHigh-confidence extractions:")
    print(f"  - People profiles: {people_kept}")
    print(f"  - Definitions: {defs_kept}")

    print(f"\n✓ Only high-confidence extractions remain")
    print(f"✓ All false positives removed")


if __name__ == '__main__':
    main()
