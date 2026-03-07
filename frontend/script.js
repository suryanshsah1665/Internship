let complexityChart = null;

async function analyzeCode() {

    const code = document.getElementById("codeInput").value;

    try {

        const response = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code: code })
        });

        const data = await response.json();

        console.log("API Response:", data);

        if (data.error) {
            document.getElementById("result").innerHTML = "Error: " + data.error;
            return;
        }

        // Prediction display
        document.getElementById("result").innerHTML =
            "Prediction: " + data.predicted_quality +
            "<br>Confidence: " + data.confidence;

        const f = data.features;
        // ----- Code Quality Score -----

let score = 100;

// penalties
score -= f.cyclomatic_complexity * 2;
score -= f.num_loops * 1.5;
score -= f.num_conditionals * 1;
score -= f.nested_loop_depth * 5;

if (f.avg_function_length > 15) {
    score -= 10;
}

if (score < 0) score = 0;

score = Math.round(score);

// status label
let status = "";
let color = "";

if (score >= 80) {
    status = "Good";
    color = "green";
}
else if (score >= 50) {
    status = "Moderate";
    color = "orange";
}
else {
    status = "Poor";
    color = "red";
}

// display
document.getElementById("scoreValue").innerText = score + "/100";
document.getElementById("scoreValue").style.color = color;
document.getElementById("scoreLabel").innerText = status;
        // -------- AI Suggestions --------
const suggestions = [];

if (f.cyclomatic_complexity > 15) {
    suggestions.push("High cyclomatic complexity detected. Consider simplifying logic or splitting functions.");
}

if (f.nested_loop_depth >= 2) {
    suggestions.push("Nested loops detected. Try reducing nesting by using helper functions or early returns.");
}

if (f.num_loops > 5) {
    suggestions.push("Many loops found. Check if some loops can be optimized or combined.");
}

if (f.avg_function_length > 20) {
    suggestions.push("Functions appear long. Consider breaking them into smaller reusable functions.");
}

if (f.num_conditionals > 8) {
    suggestions.push("Large number of conditionals. Consider using polymorphism, dictionaries, or strategy patterns.");
}

if (f.num_functions === 0) {
    suggestions.push("No functions detected. Consider organizing logic into reusable functions.");
}

if (suggestions.length === 0) {
    suggestions.push("Code structure looks good. No major complexity issues detected.");
}

const panel = document.getElementById("suggestionsPanel");
panel.innerHTML = "";

suggestions.forEach(s => {
    const li = document.createElement("li");
    li.innerText = s;
    panel.appendChild(li);
});
        // Feature panel
        document.getElementById("f_lines").innerText = f.lines_of_code;
        document.getElementById("f_functions").innerText = f.num_functions;
        document.getElementById("f_loops").innerText = f.num_loops;
        document.getElementById("f_conditionals").innerText = f.num_conditionals;
        document.getElementById("f_depth").innerText = f.nested_loop_depth;
        document.getElementById("f_avg").innerText = f.avg_function_length;
        document.getElementById("f_complexity").innerText = f.cyclomatic_complexity;

        // Chart Data
        const labels = [
            "Functions",
            "Loops",
            "Conditionals",
            "Cyclomatic Complexity"
        ];

        const values = [
            f.num_functions,
            f.num_loops,
            f.num_conditionals,
            f.cyclomatic_complexity
        ];

        const ctx = document.getElementById("complexityChart");

        if (ctx) {

            if (complexityChart) {
                complexityChart.destroy();
            }

            complexityChart = new Chart(ctx, {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Code Complexity Metrics",
                        data: values
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

        }

        loadHistory();

    } catch (error) {

        console.error(error);
        document.getElementById("result").innerHTML = "Server error.";

    }
}


async function loadHistory() {

    try {

        const response = await fetch("http://127.0.0.1:5000/history");
        const data = await response.json();

        const tableBody = document.querySelector("#historyTable tbody");
        tableBody.innerHTML = "";

        data.forEach(item => {

            const row = `
                <tr>
                    <td>${item.id}</td>
                    <td>${item.lines_of_code}</td>
                    <td>${item.num_functions}</td>
                    <td>${item.num_loops}</td>
                    <td>${item.nested_loop_depth}</td>
                    <td>${item.cyclomatic_complexity}</td>
                    <td>${item.predicted_label}</td>
                    <td>${item.created_at}</td>
                </tr>
            `;

            tableBody.innerHTML += row;

        });

    } catch (error) {

        console.error("History load error:", error);

    }

}