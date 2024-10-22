import difflib

# Constants for HTML styling
COLOR_GREEN = "#00FF00"       # Bright green for new value
COLOR_RED = "#FF0000"         # Bright red for previous value
HIGHLIGHT_COLOR = "#696969"   # Highlight color for changed text
BACKGROUND_COLOR = "#2e2e2e"  # Dark background
TEXT_COLOR = "#f0f0f0"        # Light text color
CONTAINER_BACKGROUND = "#3a3a3a"  # Slightly lighter background for the report
HEADER_COLOR = "#ffcc00"      # Bright yellow for header
HEADER_HOVER_COLOR = "#ff9900"  # Color on hover for header

# Constants for CSS styling
FONT_FAMILY = "Arial, sans-serif"
CONTAINER_PADDING = "20px"
LINE_PADDING = "8px"

def read_file(file_path):
    """Read the contents of a file and return a list of lines."""
    with open(file_path, 'r') as file:
        return file.readlines()

def is_number(value):
    """Check if the given string can be converted to a float."""
    try:
        float(value)
        return True
    except ValueError:
        return False

def format_diff(original, modified):
    """Format the differences between two lines into HTML."""
    sequence_matcher = difflib.SequenceMatcher(None, original, modified)
    formatted_result = []

    for tag, i1, i2, j1, j2 in sequence_matcher.get_opcodes():
        original_substr = original[i1:i2]
        modified_substr = modified[j1:j2]

        if tag == 'equal':
            formatted_result.append(f'<span class="equal">{original_substr}</span>')
        elif tag == 'replace':
            formatted_result.extend(handle_replace(original_substr, modified_substr))
        elif tag == 'delete':
            formatted_result.append(f'<span class="removed">{original_substr}</span>')
        elif tag == 'insert':
            formatted_result.append(f'<span class="changed">{modified_substr}</span>')

    return ''.join(formatted_result)

def handle_replace(original, modified):
    """Handle the formatting for replaced text."""
    original_value = original.strip()
    new_value = modified.strip()

    highlight_span = f'<span style="background-color: {HIGHLIGHT_COLOR}; font-weight: bold; padding: 2px 4px; border-radius: 4px;">{original_value}</span>'
    
    if is_number(original_value) and is_number(new_value):
        original_value_float = float(original_value)
        new_value_float = float(new_value)

        if original_value_float > new_value_float:
            return [
                highlight_span,
                f'<span class="changed" style="color: {COLOR_GREEN};">{new_value}</span>'  # Show the new value in green
            ]
        else:
            return [
                highlight_span,
                f'<span class="changed" style="color: {COLOR_RED};">{new_value}</span>'  # Show the new value in red
            ]
    else:
        return [
            highlight_span,
            f'<span class="changed" style="color: {COLOR_RED};">{new_value}</span>'  # Show the new value in red
        ]

def compare_lines(line1, line2, line_number):
    """Compare two lines and return their formatted difference if they are not equal."""
    if line1.strip() == line2.strip():
        return f'<div class="line"><span class="line-number">{line_number}</span><span class="line-content equal">{line1.strip()}</span></div>'
    
    return f'<div class="line"><span class="line-number">{line_number}</span><span class="line-content">{format_diff(line1, line2)}</span></div>'

def generate_comparison_report(file1_lines, file2_lines):
    """Generate a comparison report from two lists of lines."""
    report = []
    for line_number, (line1, line2) in enumerate(zip(file1_lines, file2_lines), start=1):
        report.append(compare_lines(line1, line2, line_number))
    return report

def write_report(report, output_file):
    """Write the HTML report to a file."""
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparison Report</title>
    <style>
        body {{
            font-family: {FONT_FAMILY};
            background-color: {BACKGROUND_COLOR};
            color: {TEXT_COLOR};
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: flex-start;  /* Align to the top */
            height: 100vh;
        }}
        .container {{
            width: 85vw;                     /* 85% of viewport width */
            background-color: {CONTAINER_BACKGROUND};
            border-radius: 10px;
            padding: {CONTAINER_PADDING};
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.3); /* More pronounced shadow */
            overflow-y: auto;                 /* Enable scrolling */
            display: flex;
            flex-direction: column;           /* Column layout for header and lines */
        }}
        .header {{
            text-align: center;
            color: {HEADER_COLOR};
            font-size: 24px;                /* Larger font for header */
            margin-bottom: 10px;            /* Space below the header */
        }}
        .line {{
            display: flex;                    /* Flex layout for lines */
            align-items: center;              /* Center vertically */
            padding: {LINE_PADDING};
            border-radius: 5px;
            transition: background-color 0.3s;
            margin-bottom: 5px;               /* Space between lines */
            background-color: #3c3c3c;        /* Default background for lines */
        }}
        .line:hover {{
            background-color: #444;           /* Darker background on hover */
        }}
        .line-number {{
            width: 50px;                     /* Fixed width for line numbers */
            text-align: right;               /* Align to the right */
            color: #aaa;                     /* Light gray for line numbers */
            margin-right: 15px;              /* Space between number and text */
            font-weight: bold;                /* Make line numbers bold */
        }}
        .line-content {{
            flex: 1;                          /* Take remaining space */
        }}
        .removed {{
            color: {COLOR_RED};               /* Bright red for removed lines */
            text-decoration: line-through;    /* Strikethrough effect */
        }}
        .changed {{
            font-weight: bold;
            color: {COLOR_GREEN};             /* Bright green for changes */
        }}
        .equal {{
            color: #f0f0f0;                   /* Light gray for unchanged lines */
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">File Comparison Report</h1>
        {''.join(report)}
    </div>
</body>
</html>'''
    
    with open(output_file, 'w') as file:
        file.write(html_content)

def compare_files(file1, file2, output_file):
    """Compare two files and generate a comparison report."""
    file1_lines = read_file(file1)
    file2_lines = read_file(file2)
    report = generate_comparison_report(file1_lines, file2_lines)
    write_report(report, output_file)
    print(f"Comparison report written to {output_file}")

if __name__ == "__main__":
    FILE1 = 'report1.log'  # Input file 1
    FILE2 = 'report2.log'  # Input file 2
    OUTPUT_FILE = 'comparison_report.html'  # Output report file

    compare_files(FILE1, FILE2, OUTPUT_FILE)
