# Streaming Transcript Stabilizer

**Demo/starter · Python standard library only.**

Commit token prefixes shared by consecutive hypotheses while leaving changing text provisional.

All bundled fixtures are synthetic and contain no customer data or secrets.

## Run

Use Python 3.9 or later (validated with Python 3.9.6). No installation or network access is needed. From this project directory:

```sh
python3 main.py
python3 main.py --input fixtures/demo.json --observations 3
python3 -m unittest -v
```

The default CLI executes a deterministic working demo. Invalid input exits with a readable error and nonzero status.

## Behavior

Input is a JSON list of `{text, final?}` objects. At least two observations are required. The output after every update contains committed text, provisional text and final status. A final update flushes the remaining tokens. A revision to an already committed prefix raises an explicit error.

## Limits and optional provider boundary

This is a whitespace-token consensus heuristic, not an ASR model or a guarantee of correctness. Tokens are case-sensitive. Start a new segment after a committed-prefix conflict. The fixture consists of invented text hypotheses.

A streaming ASR adapter could supply hypotheses. No audio recognition is executed here.

## Tests

`test_main.py` checks fixed expected results, edge cases and invalid inputs with `unittest`. These tests validate the local implementation, not real-world speech accuracy or production readiness. Run `python3 verify.py` to repeat this repository’s checks.

## Scope

This is an educational implementation with synthetic fixtures. Run the tests and inspect the documented limits before adapting it.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
