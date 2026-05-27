const API_URL = "http://127.0.0.1:8000";

function getCheckedValues(name) {
    return Array.from(document.querySelectorAll(`input[name="${name}"]:checked`))
        .map((input) => input.value);
}

function saveRouteResult(result) {
    localStorage.setItem("routeOptimizationResult", JSON.stringify(result));
}

function saveRouteRequest(request) {
    localStorage.setItem("routeOptimizationRequest", JSON.stringify(request));
}

async function handleRouteSubmit(event) {
    event.preventDefault();

    const start = document.getElementById("start").value;
    const finish = document.getElementById("finish").value;
    const stops = getCheckedValues("stops")
        .filter((city) => city !== start && city !== finish);

    const preferences = getCheckedValues("preferences");

    const requestData = {
        start: start,
        finish: finish,
        stops: stops,
        budget: Number(document.getElementById("budget").value),
        max_time: Number(document.getElementById("maxTime").value),
        preferences: preferences,
        priority: document.getElementById("priority").value
    };

    const submitButton = document.querySelector(".submit-button");
    submitButton.textContent = "Выполняется оптимизация...";
    submitButton.disabled = true;

    try {
        const response = await fetch(`${API_URL}/optimize-route`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        });

        const result = await response.json();

        saveRouteRequest(requestData);
        saveRouteResult(result);

        window.location.href = "result.html";
    } catch (error) {
        console.error("Ошибка при расчёте маршрута:", error);
        alert("Не удалось подключиться к backend. Проверь, что сервер FastAPI запущен.");
    } finally {
        submitButton.textContent = "Рассчитать оптимальный маршрут";
        submitButton.disabled = false;
    }
}

const routeForm = document.getElementById("routeForm");

if (routeForm) {
    routeForm.addEventListener("submit", handleRouteSubmit);
}