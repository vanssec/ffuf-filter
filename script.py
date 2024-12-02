import json

# Replace this with the file path to your JSON file
input_file = "input.json"

# Read the JSON data
with open(input_file, "r") as file:
    data = json.load(file)

# Extract the "results" section
results = data.get("results", [])

# Filter rows based on status codes starting with 3 or 5
filtered_results = [
    result for result in results
    if not str(result.get("status", "")).startswith(("3", "5"))
]

# Start generating HTML
html = """
<!DOCTYPE html>
<html>
<head>
    <title>FFUF Results</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        th {
            position: sticky;
            top: 0;
            background-color: #f9f9f9;
            z-index: 2;
        }
        th:hover {
            background-color: #f0f0f0;
        }
    </style>
</head>
<body>
    <h1>FFUF Results</h1>
    <table id="resultsTable">
        <thead>
            <tr>
                <th onclick="sortTable()">Status</th>
                <th>Length</th>
                <th>Words Count</th>
                <th>Lines</th>
                <th>WORDS</th>
                <th>URL</th>
            </tr>
        </thead>
        <tbody>
"""

# Populate table rows
for result in filtered_results:
    status = result.get("status", "")
    length = result.get("length", "")
    words_count = result.get("words", "")
    lines = result.get("lines", "")
    words = result["input"].get("WORDS", "")  # Extract WORDS from the "input" object
    url = result.get("url", "")

    html += f"""
            <tr>
                <td>{status}</td>
                <td>{length}</td>
                <td>{words_count}</td>
                <td>{lines}</td>
                <td>{words}</td>
                <td><a href="{url}" target="_blank">{url}</a></td>
            </tr>
    """

# Add JavaScript for sorting functionality
html += """
        </tbody>
    </table>
    <script>
        let currentSortIndex = -1; // Tracks current sorting state
        let originalOrder = []; // Stores the original table rows

        // Function to sort the table dynamically
        function sortTable() {
            const table = document.getElementById('resultsTable');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.rows);

            // Save the original order of rows on the first click
            if (currentSortIndex === -1) {
                originalOrder = rows.slice();
            }

            // Collect all unique status codes
            const statuses = [...new Set(rows.map(row => row.cells[0].innerText))];

            // Increment the sort state
            currentSortIndex = (currentSortIndex + 1) % (statuses.length + 1);

            if (currentSortIndex < statuses.length) {
                // Sort by the current status
                const sortByStatus = statuses[currentSortIndex];
                rows.sort((a, b) => {
                    if (a.cells[0].innerText === sortByStatus) return -1;
                    if (b.cells[0].innerText === sortByStatus) return 1;
                    return 0;
                });
            } else {
                // Reset to the original order
                rows.splice(0, rows.length, ...originalOrder);
                currentSortIndex = -1; // Reset the sorting state
            }

            // Clear and append sorted rows to the table body
            tbody.innerHTML = '';
            rows.forEach(row => tbody.appendChild(row));
        }
    </script>
</body>
</html>
"""

# Save the HTML file
output_file = "output.html"
with open(output_file, "w") as file:
    file.write(html)

print(f"HTML file has been generated: {output_file}")
