const display = document.getElementById("display");
const message = document.getElementById("message");

function addValue(value) {
    display.value += value;
    message.innerText = "";
}

function clearDisplay() {
    display.value = "";
    message.innerText = "";
}

function deleteLast() {
    display.value = display.value.slice(0, -1);
}

async function calculate() {
    const expression = display.value.trim();

    // Check calculation format
    const pattern = /^(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)$/;

    const match = expression.match(pattern);

    if (!match) {
        message.innerText = "Enter a valid calculation!";
        return;
    }

    const num1 = Number(match[1]);
    const operator = match[2];
    const num2 = Number(match[3]);

    try {
        const response = await fetch("/calculate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                num1: num1,
                operator: operator,
                num2: num2
            })
        });

        const data = await response.json();

        if (!response.ok) {
            message.innerText = data.error || "Calculation failed";
            return;
        }

        display.value = data.result;
        message.innerText = "Calculation successful!";

    } catch (error) {
        message.innerText = "Server connection failed!";
    }
}

async function getHistory() {
    const historyDiv = document.getElementById("history");

    try {
        const response = await fetch("/history");
        const data = await response.json();

        historyDiv.innerHTML = "";

        if (data.length === 0) {
            historyDiv.innerText = "No history found.";
            return;
        }

        data.forEach(item => {
            const div = document.createElement("div");
            div.className = "history-item";

            div.textContent =
                `${item.num1} ${item.operator} ${item.num2} = ${item.result}`;

            historyDiv.appendChild(div);
        });

    } catch (error) {
        historyDiv.innerText = "Unable to load history.";
    }
}
