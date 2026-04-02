#!/bin/bash
# Print stats for each test case: chars, words, unique char coverage

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 -c "
import sys, string
sys.path.insert(0, '${SCRIPT_DIR}/..')

from test_cases import TEST_CASES

PRINTABLE = set(string.printable.strip())  # 95 printable ASCII chars

cases = sorted(TEST_CASES.items(), key=lambda x: len(x[1]))

print(f\"{'Name':<30} {'Chars':>10} {'Words':>8} {'Unique':>7} {'Coverage':>9}\")
print('-' * 68)

for name, content in cases:
    chars = len(content)
    words = len(content.split())
    unique = set(content) & PRINTABLE
    coverage = len(unique) / len(PRINTABLE) * 100
    print(f'{name:<30} {chars:>10,} {words:>8,} {len(unique):>5}/95 {coverage:>7.1f}%')

print('-' * 68)
print(f'Total: {len(cases)} test cases')
"
