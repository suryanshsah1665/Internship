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