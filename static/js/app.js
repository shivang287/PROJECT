function findMatches() {

    const button = document.querySelector(".match-btn");

    button.innerHTML = "⏳ AI Analyzing...";
    button.disabled = true;

    setTimeout(() => {

        window.location.href = "/matching";

    }, 1200);
}
function joinPool() {

    const button = event.target;

    button.innerHTML = "⏳ Joining Pool...";
    button.disabled = true;

    setTimeout(() => {

        button.innerHTML = "✓ Pool Joined";

        button.style.background = "#26743a";

    }, 1000);
}


function acceptOffer() {

    const button = event.target;

    button.innerHTML = "⏳ Processing...";
    button.disabled = true;

    setTimeout(() => {

        button.innerHTML = "✓ Offer Accepted";

        button.style.background = "#26743a";

    }, 1000);
}
async function loadForecast() {

    const chart =
        document.getElementById("forecast-chart");

    const insight =
        document.getElementById("forecast-insight");

    // Make sure this function only runs
    // on pages that contain the forecast.
    if (!chart || !insight) {
        return;
    }

    try {

        const response =
            await fetch("/api/forecast");

        if (!response.ok) {

            throw new Error(
                `API Error: ${response.status}`
            );

        }

        const data =
            await response.json();

        console.log("Forecast API:", data);


        if (
            !data.forecast ||
            data.forecast.length === 0
        ) {

            throw new Error(
                "No forecast data received."
            );

        }


        // Clear loading message
        chart.innerHTML = "";


        // Find highest predicted demand
        const maxDemand =
            Math.max(
                ...data.forecast.map(
                    item => item.demand_kg
                )
            );


        // Create bars
        data.forecast.forEach(item => {

            const height =
                (item.demand_kg / maxDemand) * 100;


            const bar =
                document.createElement("div");

            bar.className =
                "forecast-bar-container";


            bar.innerHTML = `

                <div class="forecast-value">
                    ${item.demand_kg.toLocaleString()} kg
                </div>

                <div class="forecast-bar-area">

                    <div
                        class="forecast-bar"
                        style="height: ${height}%"
                    ></div>

                </div>

                <div class="forecast-date">
                    ${item.date}
                </div>

            `;


            chart.appendChild(bar);

        });


        // Calculate forecast trend
        const first =
            data.forecast[0].demand_kg;

        const last =
            data.forecast[
                data.forecast.length - 1
            ].demand_kg;


        const change =
            ((last - first) / first) * 100;


        const direction =
            change >= 0
                ? "increasing"
                : "decreasing";


        insight.innerHTML = `

            💡 <strong>AI Insight:</strong>

            Tomato demand is expected to be
            <strong>
                ${Math.abs(change).toFixed(1)}%
            </strong>
            ${direction} over the forecast period.

        `;

    }

    catch (error) {

        console.error(
            "Forecast Error:",
            error
        );


        chart.innerHTML = `

            <div class="forecast-error">

                ⚠️ Unable to generate forecast.

                <br>

                <small>
                    Check the Flask terminal for the error.
                </small>

            </div>

        `;


        insight.innerHTML = `

            <strong>
                Forecast service unavailable.
            </strong>

        `;

    }

}


// Start forecast when page loads
loadForecast();