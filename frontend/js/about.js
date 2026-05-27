const liquidUpgradeLink = document.createElement("link");
liquidUpgradeLink.rel = "stylesheet";
liquidUpgradeLink.href = "css/liquid-upgrade.css";
document.head.appendChild(liquidUpgradeLink);

const modalData = {
    graph: {
        kicker: "01 / Graph model",
        title: "Графовая модель маршрута",
        formula: "G = (V, E)",
        text:
            "Маршрут представлен в виде взвешенного графа. Вершины графа — города или точки маршрута, а рёбра — возможные перемещения между ними. Каждое ребро хранит расстояние, время и стоимость.",
        definitions: [
            ["V", "множество вершин: города и туристические точки"],
            ["E", "множество рёбер: возможные переходы между точками"],
            ["tᵢⱼ", "время перемещения между вершинами i и j"],
            ["cᵢⱼ", "стоимость перемещения между вершинами i и j"]
        ]
    },

    objective: {
        kicker: "02 / Objective function",
        title: "Целевая функция Score(R)",
        formula: "Score(R) = w₁ · (1 − T*) + w₂ · (1 − C*) + w₃ · P* + w₄ · Q*",
        text:
            "Целевая функция объединяет несколько критериев в одну итоговую оценку маршрута. Время и стоимость минимизируются, поэтому используются выражения 1 − T* и 1 − C*. Предпочтения и рейтинг максимизируются.",
        definitions: [
            ["T*", "нормализованное время маршрута"],
            ["C*", "нормализованная стоимость маршрута"],
            ["P*", "совпадение маршрута с интересами пользователя"],
            ["Q*", "нормализованный средний рейтинг точек маршрута"]
        ]
    },

    constraints: {
        kicker: "03 / Constraints",
        title: "Ограничения допустимого маршрута",
        formula: "T(R) ≤ Tₘₐₓ,  C(R) ≤ B",
        text:
            "Перед выбором лучшего маршрута программа отбрасывает варианты, которые не удовлетворяют ограничениям. Если маршрут превышает бюджет или лимит времени, он не участвует в сравнении по целевой функции.",
        definitions: [
            ["T(R)", "суммарное время маршрута"],
            ["Tₘₐₓ", "максимально допустимое время"],
            ["C(R)", "суммарная стоимость маршрута"],
            ["B", "бюджет пользователя"]
        ]
    },

    algorithm: {
        kicker: "04 / Optimization algorithm",
        title: "Алгоритм поиска маршрута",
        formula: "R* = arg max Score(R)",
        text:
            "Система генерирует все перестановки промежуточных точек, формирует возможные маршруты, рассчитывает показатели каждого маршрута, фильтрует недопустимые варианты и выбирает маршрут с максимальной оценкой.",
        definitions: [
            ["1", "получить старт, финиш и промежуточные точки"],
            ["2", "сформировать перестановки промежуточных точек"],
            ["3", "рассчитать время, стоимость, расстояние и рейтинг"],
            ["4", "выбрать максимум целевой функции Score(R)"]
        ]
    },

    weights: {
        kicker: "05 / Criteria weights",
        title: "Веса критериев",
        formula: "w₁ + w₂ + w₃ + w₄ = 1",
        text:
            "Веса задают важность критериев. Если пользователь выбирает режим «минимум времени», увеличивается вес времени. Если выбирает «минимум стоимости», увеличивается вес стоимости.",
        definitions: [
            ["balanced", "0.30 / 0.25 / 0.25 / 0.20"],
            ["fast", "0.50 / 0.15 / 0.20 / 0.15"],
            ["cheap", "0.15 / 0.50 / 0.20 / 0.15"],
            ["preferences", "0.15 / 0.15 / 0.50 / 0.20"]
        ]
    },

    normalization: {
        kicker: "06 / Normalization",
        title: "Нормализация критериев",
        formula: "x* = (x − xₘᵢₙ) / (xₘₐₓ − xₘᵢₙ)",
        text:
            "Поскольку время, стоимость, рейтинг и предпочтения измеряются в разных единицах, их нужно привести к единой шкале от 0 до 1. После этого критерии можно корректно объединять в одной функции.",
        definitions: [
            ["x", "исходное значение критерия"],
            ["xₘᵢₙ", "минимальное значение среди допустимых маршрутов"],
            ["xₘₐₓ", "максимальное значение среди допустимых маршрутов"],
            ["x*", "нормализованное значение критерия"]
        ]
    }
};

const modelModal = document.getElementById("modelModal");
const modalContent = document.getElementById("modalContent");

let closeTimer = null;

function openModal(key) {
    const data = modalData[key];

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

    modalContent.innerHTML = `
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

    modelModal.classList.remove("is-closing");

    requestAnimationFrame(() => {
        modelModal.classList.add("active");
    });

    document.body.style.overflow = "hidden";
}

function closeModal() {
    if (!modelModal.classList.contains("active")) {
        return;
    }

    modelModal.classList.add("is-closing");
    modelModal.classList.remove("active");

    closeTimer = setTimeout(() => {
        modelModal.classList.remove("is-closing");
        document.body.style.overflow = "";
        closeTimer = null;
    }, 420);
}

document.querySelectorAll("[data-modal]").forEach((button) => {
    button.addEventListener("click", () => {
        openModal(button.dataset.modal);
    });
});

document.querySelectorAll("[data-close-modal]").forEach((element) => {
    element.addEventListener("click", closeModal);
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        closeModal();
    }
});