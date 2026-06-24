# Task 1 - Bash Scripting: Service Inventory Health Report

## Overview

This task implements a Bash script (`service_report.sh`) that parses a colon-separated service inventory file, validates each record, and generates a health report for valid services.

The implementation focuses on:

* Input and file validation
* Robust parsing of colon-separated records
* Handling missing fields and whitespace
* Validation of TCP port ranges
* Validation of positive integer weights
* Proper separation of stdout and stderr
* Clear error and warning messages

The script uses `set -euo pipefail` to improve reliability and fail safely on unexpected errors.

---

## Files

```text
task-1-bash/
├── service_report.sh
├── inventory.txt
└── README.md
```

---

## Assumptions

* The first non-empty line is the header and is skipped.
* Only `prod` and `staging` environments are considered in scope.
* Services from any other environment are skipped silently.
* TCP ports must be integers between 1 and 65535.
* Weights must be positive integers.
* Blank lines are ignored.
* Leading and trailing whitespace is trimmed from all fields before validation.

---

## Running the Script

Make the script executable:

```bash
chmod +x service_report.sh
```

Execute:

```bash
./service_report.sh inventory.txt
```

Execute with saved output:

```bash
./service_report.sh inventory.txt > run.stdout 2> run.stderr && printf 'STDOUT\n' && cat run.stdout && printf '\nSTDERR\n' && cat run.stderr
```
---

## Sample Output

### stdout

```text
Service checkout-api on port 8080 has an even weight of 42.
Service search-svc on port 9090 has an odd weight of 17.
Service cart-api on port 8082 has an even weight of 128.
```

### stderr

```text
Warning: skipping service 'notifications' due to invalid port: '<missing>'
Warning: skipping service 'billing-worker' due to invalid weight: '<missing>'
Warning: skipping service 'metrics-agent' due to invalid port: '70000'
Summary: processed=7 reported=3 skipped=4
```

---

## Validation Logic

### Environment Filter

Only the following environments are processed:

* `prod`
* `staging`

All other environments are skipped without generating warnings.

### Port Validation

Ports must:

* Be numeric
* Be within the TCP range `1-65535`

Invalid or missing ports generate warnings on stderr.

### Weight Validation

Weights must:

* Be numeric
* Be greater than zero

Invalid or missing weights generate warnings on stderr.

### Weight Classification

For valid records:

* Even weights are reported as `even`
* Odd weights are reported as `odd`

The result is printed to stdout using the required format.
