#!/usr/bin/env bash

set -euo pipefail

print_error() {
	echo "Error: $1" >&2
}

print_warning() {
	echo "Warning: $1" >&2
}

trim_whitespace() {
	local s="$1"
	s="${s#"${s%%[![:space:]]*}"}"
	s="${s%"${s##*[![:space:]]}"}"
	printf '%s' "$s"
}

is_positive_integer() {
	[[ "$1" =~ ^[0-9]+$ ]] && [[ "$1" -gt 0 ]]
}

is_valid_port() {
	local port="$1"
	[[ "$port" =~ ^[0-9]+$ ]] && [[ "$port" -ge 1 && "$port" -le 65535 ]]
}

process_record() {
	local name="$1"
	local environment="$2"
	local port="$3"
	local weight="$4"

	if [[ "$environment" != "prod" && "$environment" != "staging" ]]; then
		skipped=$((skipped + 1))
		return 0
	fi

	if ! is_valid_port "$port"; then
		print_warning "skipping service '$name' due to invalid port: '${port:-<missing>}'"
		skipped=$((skipped + 1))
		return 0
	fi

	if ! is_positive_integer "$weight"; then
		print_warning "skipping service '$name' due to invalid weight: '${weight:-<missing>}'"
		skipped=$((skipped + 1))
		return 0
	fi

	local parity="odd"
	if (( weight % 2 == 0 )); then
		parity="even"
	fi

	echo "Service $name on port $port has an $parity weight of $weight."
	reported=$((reported + 1))
}

if [[ $# -lt 1 ]]; then
	print_error "inventory file path is required."
	exit 1
fi

inventory_file="$1"

if [[ ! -e "$inventory_file" ]]; then
	print_error "file does not exist: $inventory_file"
	exit 1
fi

if [[ ! -r "$inventory_file" ]]; then
	print_error "file is not readable: $inventory_file"
	exit 1
fi

processed=0
reported=0
skipped=0
seen_header=0

while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
	line="$(trim_whitespace "$raw_line")"

	if [[ -z "$line" ]]; then
		continue
	fi

	if [[ "$seen_header" -eq 0 ]]; then
		seen_header=1
		continue
	fi

	processed=$((processed + 1))

	IFS=':' read -r name environment port weight _extra <<< "$line"

	name="$(trim_whitespace "${name:-}")"
	environment="$(trim_whitespace "${environment:-}")"
	port="$(trim_whitespace "${port:-}")"
	weight="$(trim_whitespace "${weight:-}")"

	process_record "$name" "$environment" "$port" "$weight"
done < "$inventory_file"

echo "Summary: processed=$processed reported=$reported skipped=$skipped" >&2