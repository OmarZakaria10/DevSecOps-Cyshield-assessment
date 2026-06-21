#!/usr/bin/env bash

trim_whitespace() {
    local s="$1"
    s="${s#"${s%%[![:space:]]*}"}"
    s="${s%"${s##*[![:space:]]}"}"
    printf '%s' "$s"
}

processed=0
reported=0
skipped=0
seen_header=0

inventory_file="$1"

while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
    line="$(trim_whitespace "$raw_line")"

    [[ -z "$line" ]] && continue

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

    if [[ "$environment" != "prod" && "$environment" != "staging" ]]; then
        skipped=$((skipped + 1))
        continue
    fi

    parity="odd"
    if (( weight % 2 == 0 )); then
        parity="even"
    fi

    echo "Service $name on port $port has an $parity weight of $weight."
    reported=$((reported + 1))
done < "$inventory_file"

echo "Summary: processed=$processed reported=$reported skipped=$skipped"