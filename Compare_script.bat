#!/bin/bash

read_file() {
    local file=$1
    cat "$file"
}

compare_lines() {
    local line1="$1"
    local line2="$2"

    if [[ "$line1" == "$line2" ]]; then
        echo "."
    else
        echo "$line2"
    fi
}

generate_comparison_report() {
    local file1_lines=("$@")
    local file2_lines=("$@")
    
    local file1="$1"
    local file2="$2"
    local output_file="$3"

    exec 3<"$file1"
    exec 4<"$file2"

    while read -r line1 <&3 && read -r line2 <&4; do
        compare_lines "$line1" "$line2" >> "$output_file"
    done

    exec 3<&-
    exec 4<&-
}

compare_files() {
    local file1=$1
    local file2=$2
    local output_file=$3

    # Clear output file first
    : > "$output_file"

    generate_comparison_report "$file1" "$file2" "$output_file"
    echo "Comparison report written to $output_file"
}

# Main function to call
main() {
    local file1="report1.log"
    local file2="report2.log"
    local output_file="report.txt"

    compare_files "$file1" "$file2" "$output_file"
}

main
