const cityNamesRu = {
    Amsterdam: "Амстердам",
    Rotterdam: "Роттердам",
    Utrecht: "Утрехт",
    "The Hague": "Гаага",
    Leiden: "Лейден",
    Haarlem: "Харлем"
};

const resultModalData = {
    model: {
        kicker: "Mathematical model",
        title: "Как система выбирает лучший маршрут",
        formula: "R* = arg max Score(R)",
        text:
            "Программа строит все допустимые варианты маршрута, рассчитывает показатели каждого варианта, отбрасывает маршруты, нарушающие ограничения по времени и бюджету, а затем выбирает маршрут с максимальным значением целевой функции.",
        definitions: [
            ["R", "один из возможных маршрутов"],
            ["R*", "лучший найденный маршрут"],
            ["Score(R)", "итоговая оценка маршрута"],
            ["arg max", "выбор варианта с максимальным значением функции"]
        ]
    },

    route: {
        kicker: "Best route",
        title: "Почему выбран именно этот маршрут",
        formula: "Score(R*) ≥ Score(Rᵢ)",
        text:
            "Выбранный маршрут имеет наибольшую оценку среди допустимых маршрутов. Это не обязательно самый дешёвый или самый быстрый вариант, потому что система учитывает несколько критериев одновременно.",
        definitions: [
            ["время", "чем меньше, тем выше вклад в Score"],
            ["стоимость", "чем меньше, тем выше вклад в Score"],
            ["интересы", "чем больше совпадений, тем выше оценка"],
            ["рейтинг", "чем выше качество точек, тем выше оценка"]
        ]
    },

    time: {
        kicker: "Time calculation",
        title: "Расчёт времени маршрута",
        formula: "T(R) = Σtᵢⱼ + Σsᵢ",
        text:
            "Общее время маршрута складывается из времени перемещений между городами и времени посещения каждой точки маршрута.",
        definitions: [
            ["Σtᵢⱼ", "сумма времени переездов по рёбрам графа"],
            ["Σsᵢ", "сумма времени посещения выбранных точек"],
            ["T(R)", "общее время маршрута"],
            ["T_max", "ограничение пользователя по времени"]
        ]
    },

    cost: {
        kicker: "Cost calculation",
        title: "Расчёт стоимости маршрута",
        formula: "C(R) = Σcᵢⱼ + Σvᵢ",
        text:
            "Общая стоимость маршрута складывается из стоимости перемещений между точками и стоимости посещения городов или объектов.",
        definitions: [
            ["Σcᵢⱼ", "сумма стоимости переездов"],
            ["Σvᵢ", "сумма стоимости посещений"],
            ["C(R)", "общая стоимость маршрута"],
            ["B", "бюджет пользователя"]
        ]
    },

    distance: {
        kicker: "Graph edges",
        title: "Расстояние по рёбрам графа",
        formula: "D(R) = Σdᵢⱼ",
        text:
            "Расстояние считается как сумма длин рёбер между последовательными точками маршрута. Оно используется как дополнительная характеристика маршрута.",
        definitions: [
            ["dᵢⱼ", "расстояние между вершинами i и j"],
            ["D(R)", "суммарная длина маршрута"],
            ["E", "множество рёбер графа"],
            ["G", "граф маршрута"]
        ]
    },

    rating: {
        kicker: "Route quality",
        title: "Рейтинг и качество маршрута",
        formula: "Q(R) = average(rᵢ)",
        text:
            "Качество маршрута оценивается через средний рейтинг точек, входящих в маршрут. Затем показатель нормализуется и участвует в целевой функции.",
        definitions: [
            ["rᵢ", "рейтинг отдельной точки"],
            ["Q(R)", "средний рейтинг маршрута"],
            ["Q*", "нормализованное качество маршрута"],
            ["max", "чем выше рейтинг, тем лучше"]
        ]
    },

    preferences: {
        kicker: "Preference matching",
        title: "Совпадение с интересами",
        formula: "P(R) = matches / possible_matches",
        text:
            "Для каждой точки маршрута проверяется, совпадают ли её категории с выбранными интересами пользователя. Чем больше совпадений, тем выше значение P*.",
        definitions: [
            ["culture", "культура"],
            ["architecture", "архитектура"],
            ["history", "история"],
            ["food", "еда"]
        ]
    },

    normalization: {
        kicker: "Normalization",
        title: "Нормализация критериев",
        formula: "x* = (x − x_min) / (x_max − x_min)",
        text:
            "Критерии имеют разные единицы измерения: часы, деньги, проценты и рейтинг. Нормализация приводит их к единой шкале от 0 до 1.",
        definitions: [
            ["x", "исходное значение"],
            ["x_min", "минимальное значение среди допустимых маршрутов"],
            ["x_max", "максимальное значение среди допустимых маршрутов"],
            ["x*", "нормализованное значение"]
        ]
    },

    alternatives: {
        kicker: "Alternative routes",
        title: "Зачем нужны альтернативные маршруты",
        formula: "R₁, R₂, ..., Rₙ",
        text:
            "Альтернативные маршруты показывают, что программа действительно сравнивает несколько вариантов, а не возвращает заранее заданный путь. Это усиливает математическую часть проекта.",
        definitions: [
            ["R₁", "лучший маршрут"],
            ["R₂", "второй по оценке маршрут"],
            ["Rₙ", "другой допустимый вариант"],
            ["Score", "критерий сортировки маршрутов"]
        ]
    }
};

const cityPositions = [
    { x: 16, y: 62 },
    { x: 34, y: 38 },
    { x: 52, y: 58 },
    { x: 70, y: 34 },
    { x: 84, y: 58 }
];

const resultModal = document.getElementById("resultModal");
const resultModalContent = document.getElementById("resultModalContent");
let closeTimer = null;

function getCityName(city) {
    return cityNamesRu[city] || city;
}

function formatMoneyDollars(value) {
    return `$${Math.round(value)}`;
}

function formatMoneyRubles(value) {
    const rubles = Math.round(value * 90);
    return `₽${rubles.toLocaleString("ru-RU")}`;
}

function renderRoutePath(route) {
    const routePath = document.getElementById("routePath");
    routePath.innerHTML = "";

    route.forEach((city, index) => {
        const cityElement = document.createElement("span");
        cityElement.className = "route-city";
        cityElement.textContent = getCityName(city);
        routePath.appendChild(cityElement);

        if (index < route.length - 1) {
            const arrow = document.createElement("span");
            arrow.className = "route-arrow";
            arrow.textContent = "→";
            routePath.appendChild(arrow);
        }
    });
}

function renderRouteVisual(route) {
    const routeNodes = document.getElementById("routeNodes");
    routeNodes.innerHTML = "";

    route.forEach((city, index) => {
        const position = cityPositions[index] || cityPositions[cityPositions.length - 1];

        const node = document.createElement("div");
        node.className = "visual-route-node";
        node.style.left = `${position.x}%`;
        node.style.top = `${position.y}%`;
        node.textContent = getCityName(city);

        routeNodes.appendChild(node);
    });
}

function renderWeights(weights) {
    const weightsList = document.getElementById("weightsList");

    const labels = {
        time: "Время",
        cost: "Стоимость",
        preferences: "Интересы",
        rating: "Рейтинг"
    };

    weightsList.innerHTML = "";

    Object.entries(weights).forEach(([key, value]) => {
        const item = document.createElement("div");
        item.className = "weight-item";

        item.innerHTML = `
            <span>${labels[key]}</span>
            <strong>${value}</strong>
        `;

        weightsList.appendChild(item);
    });
}

function renderAlternatives(alternatives) {
    const alternativesList = document.getElementById("alternativesList");
    alternativesList.innerHTML = "";

    if (!alternatives || alternatives.length === 0) {
        alternativesList.innerHTML = `
            <p class="empty-state">
                Альтернативные допустимые маршруты отсутствуют.
                Это может означать, что найден только один маршрут,
                удовлетворяющий ограничениям по бюджету и времени.
            </p>
        `;
        return;
    }

    alternatives.slice(0, 5).forEach((item, index) => {
        const routeText = item.route.map(getCityName).join(" → ");
        const metrics = item.metrics;
        const calculation = item.calculation;

        const element = document.createElement("div");
        element.className = "alt-route";

        element.innerHTML = `
            <strong>${index + 1}. ${routeText}</strong>
            <p>
                Score: ${calculation.score_percent}/100 ·
                Время: ${metrics.total_time} ч ·
                Стоимость: ${formatMoneyDollars(metrics.total_cost)} / ${formatMoneyRubles(metrics.total_cost)}
            </p>
        `;

        alternativesList.appendChild(element);
    });
}

function renderNoResult() {
    document.getElementById("routeTitle").textContent = "Маршрут ещё не рассчитан";
    document.getElementById("scorePercent").textContent = "—";
    document.getElementById("statusText").textContent = "empty";

    document.getElementById("routePath").innerHTML = `
        <p class="empty-state">
            Перейдите в планировщик, задайте параметры маршрута и нажмите
            «Рассчитать оптимальный маршрут».
        </p>
    `;
}

function renderResult() {
    const savedResult = localStorage.getItem("routeOptimizationResult");

    if (!savedResult) {
        renderNoResult();
        return;
    }

    const result = JSON.parse(savedResult);

    if (result.status !== "success") {
        document.getElementById("routeTitle").textContent = "Подходящий маршрут не найден";
        document.getElementById("scorePercent").textContent = "—";
        document.getElementById("statusText").textContent = "no solution";

        document.getElementById("routePath").innerHTML = `
            <p class="empty-state">
                Не найден маршрут, который укладывается в заданный бюджет и время.
                Вернитесь в планировщик и увеличьте бюджет или лимит времени.
            </p>
        `;

        return;
    }

    const best = result.best_route;
    const route = best.route;
    const metrics = best.metrics;
    const calculation = best.calculation;

    document.getElementById("routeTitle").textContent = route.map(getCityName).join(" → ");
    document.getElementById("scorePercent").textContent = `${calculation.score_percent}/100`;
    document.getElementById("statusText").textContent = "success";

    document.getElementById("resultExplanation").textContent =
        `Выбран маршрут с максимальной оценкой Score(R) = ${calculation.score}.
        Он удовлетворяет ограничениям по бюджету и времени и имеет итоговую оценку ${calculation.score_percent}/100.`;

    renderRoutePath(route);
    renderRouteVisual(route);

    document.getElementById("totalTime").textContent = `${metrics.total_time} ч`;
    document.getElementById("timeDetails").textContent =
        `переезды: ${metrics.travel_time} ч, посещение: ${metrics.visit_time} ч`;

    document.getElementById("totalCost").textContent =
        `${formatMoneyDollars(metrics.total_cost)} / ${formatMoneyRubles(metrics.total_cost)}`;

    document.getElementById("costDetails").textContent =
        `дорога: ${formatMoneyDollars(metrics.travel_cost)}, посещения: ${formatMoneyDollars(metrics.visit_cost)}`;

    document.getElementById("distance").textContent = `${metrics.distance} км`;
    document.getElementById("averageRating").textContent = metrics.average_rating;

    document.getElementById("timeNorm").textContent = calculation.time_norm;
    document.getElementById("costNorm").textContent = calculation.cost_norm;
    document.getElementById("preferenceNorm").textContent = calculation.preference_norm;
    document.getElementById("ratingNorm").textContent = calculation.rating_norm;

    renderWeights(calculation.weights);
    renderAlternatives(result.alternative_routes);
}

function openResultModal(key) {
    const data = resultModalData[key];

    if (!data) {
        return;
    }

    if (closeTimer) {
        clearTimeout(closeTimer);
        closeTimer = null;
    }

    const definitionsHtml = data.definitions
        .map(([term, description]) => {
            return `
                <div>
                    <strong>${term}</strong>
                    <span>${description}</span>
                </div>
            `;
        })
        .join("");

    resultModalContent.innerHTML = `
        <span class="modal-kicker">${data.kicker}</span>
        <h2>${data.title}</h2>

        <div class="modal-formula">
            ${data.formula}
        </div>

        <p>${data.text}</p>

        <div class="modal-definition-grid">
            ${definitionsHtml}
        </div>
    `;

    resultModal.classList.remove("is-closing");

    requestAnimationFrame(() => {
        resultModal.classList.add("active");
    });

    document.body.style.overflow = "hidden";
}

function closeResultModal() {
    if (!resultModal.classList.contains("active")) {
        return;
    }

    resultModal.classList.add("is-closing");
    resultModal.classList.remove("active");

    closeTimer = setTimeout(() => {
        resultModal.classList.remove("is-closing");
        document.body.style.overflow = "";
        closeTimer = null;
    }, 420);
}

document.querySelectorAll("[data-result-modal]").forEach((button) => {
    button.addEventListener("click", () => {
        openResultModal(button.dataset.resultModal);
    });
});

document.querySelectorAll("[data-close-result-modal]").forEach((element) => {
    element.addEventListener("click", closeResultModal);
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        closeResultModal();
    }
});

renderResult();