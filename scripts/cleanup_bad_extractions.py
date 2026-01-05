#!/usr/bin/env python3
"""
Clean up bad extractions (meaningless people/definitions).
"""

import sys
import re
from pathlib import Path


# Same filters as the improved processor
COMMON_WORDS = {
    'am', 'pm', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
    'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from',
    'as', 'is', 'was', 'are', 'were', 'be', 'been', 'being', 'what', 'when', 'where', 'who',
    'why', 'how', 'which', 'a', 'i', 'an', 'ad', 'about', 'above', 'after', 'again', 'against',
    'all', 'also', 'although', 'always', 'another', 'any', 'anything', 'anyone', 'anywhere',
    'around', 'because', 'before', 'behind', 'below', 'between', 'both', 'during', 'each',
    'either', 'enough', 'even', 'every', 'everything', 'everyone', 'everywhere', 'few', 'first',
    'follow', 'following', 'however', 'instead', 'into', 'just', 'last', 'later', 'least', 'less',
    'like', 'many', 'more', 'most', 'much', 'never', 'next', 'now', 'often', 'once', 'one',
    'only', 'other', 'others', 'otherwise', 'our', 'over', 'own', 'same', 'several', 'should',
    'since', 'some', 'something', 'someone', 'somewhere', 'still', 'such', 'than', 'that',
    'their', 'them', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'too',
    'under', 'unless', 'until', 'very', 'well', 'when', 'where', 'whether', 'while', 'who',
    'whom', 'whose', 'will', 'with', 'within', 'without', 'would', 'your'
}


def is_bad_person_file(filename):
    """Check if a person file is likely a false positive."""
    stem = filename.stem

    # Check against common words
    if stem.lower() in COMMON_WORDS:
        return True

    # Check if it starts with common words
    if any(stem.lower().startswith(word + '-') for word in {'and', 'or', 'but', 'the', 'a', 'an', 'as', 'is', 'are'}):
        return True

    # Check for sentence fragments
    if any(word in stem.lower() for word in ['-and-', '-or-', '-but-', '-the-', '-a-', '-is-', '-are-']):
        return True

    # Too short (single name)
    if len(stem.replace('-', ' ').split()) < 2:
        return True

    return False


def is_bad_definition_file(filename):
    """Check if a definition file is likely a false positive."""
    stem = filename.stem

    # Check against common words
    if stem.lower() in COMMON_WORDS:
        return True

    # Less than 3 characters when removing hyphens
    if len(stem.replace('-', '')) < 3:
        return True

    # Common non-acronym patterns
    if stem.lower() in {'and', 'or', 'but', 'the', 'a', 'an', 'as', 'is', 'are', 'was', 'were'}:
        return True

    return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 cleanup_bad_extractions.py <project_dir>")
        sys.exit(1)

    project_dir = Path(sys.argv[1]).expanduser()
    kb_dir = project_dir / 'knowledge'

    if not kb_dir.exists():
        print("Error: knowledge/ directory not found")
        sys.exit(1)

    print("\nCleaning Up Bad Extractions")
    print("============================\n")

    # Clean up people
    people_dir = kb_dir / 'people'
    if people_dir.exists():
        people_files = list(people_dir.glob('*.md'))
        bad_people = [f for f in people_files if is_bad_person_file(f)]

        print(f"People profiles: {len(people_files)} total")
        print(f"  - Bad extractions to remove: {len(bad_people)}")

        if bad_people:
            for f in bad_people:
                f.unlink()
            print(f"  ✓ Removed {len(bad_people)} bad people files")

    # Clean up definitions
    defs_dir = kb_dir / 'definitions'
    if defs_dir.exists():
        def_files = list(defs_dir.glob('*.md'))
        bad_defs = [f for f in def_files if is_bad_definition_file(f)]

        print(f"\nDefinitions: {len(def_files)} total")
        print(f"  - Bad extractions to remove: {len(bad_defs)}")

        if bad_defs:
            for f in bad_defs:
                f.unlink()
            print(f"  ✓ Removed {len(bad_defs)} bad definition files")

    # Summary
    print(f"\n\nCleanup Complete")
    print(f"================")
    print(f"Removed: {len(bad_people) if 'bad_people' in locals() else 0} people files")
    print(f"Removed: {len(bad_defs) if 'bad_defs' in locals() else 0} definition files")

    # Show remaining
    people_remaining = len(list(people_dir.glob('*.md'))) if people_dir.exists() else 0
    defs_remaining = len(list(defs_dir.glob('*.md'))) if defs_dir.exists() else 0

    print(f"\nRemaining:")
    print(f"  - People profiles: {people_remaining}")
    print(f"  - Definitions: {defs_remaining}")


if __name__ == '__main__':
    main()
