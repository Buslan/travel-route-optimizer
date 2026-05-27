const cityTranslations = {
    ru: {
        Moscow: "Москва",
        "Saint Petersburg": "Санкт-Петербург",
        Smolensk: "Смоленск",
        Paris: "Париж",
        "New York": "Нью-Йорк",
        Sochi: "Сочи",
        Tambov: "Тамбов",
        Berlin: "Берлин",
        Gelendzhik: "Геленджик",
        Istanbul: "Стамбул",
        Magadan: "Магадан"
    },

    en: {
        Moscow: "Moscow",
        "Saint Petersburg": "Saint Petersburg",
        Smolensk: "Smolensk",
        Paris: "Paris",
        "New York": "New York",
        Sochi: "Sochi",
        Tambov: "Tambov",
        Berlin: "Berlin",
        Gelendzhik: "Gelendzhik",
        Istanbul: "Istanbul",
        Magadan: "Magadan"
    }
};

const translations = {
    ru: {
        nav_home: "Главная",
        nav_planner: "Планировщик",
        nav_result: "Результат",
        nav_model: "Модель",

        hero_eyebrow: "Математическое планирование путешествий",
        hero_title: "Постройте оптимальный маршрут <span>через несколько точек</span>",
        hero_description:
            "Веб-приложение подбирает маршрут путешествия на основе графовой модели, ограничений по времени и бюджету, а также личных предпочтений пользователя.",
        hero_start: "Начать планирование",
        hero_model: "Посмотреть модель",

        stat_criteria_label: "Критерии",
        stat_criteria_text: "время, стоимость, интересы, рейтинг",
        stat_model_label: "Модель",
        stat_model_text: "взвешенный граф маршрута",
        stat_score_label: "Оценка",
        stat_score_text: "целевая функция маршрута",

        route_preview_title: "Москва → Санкт-Петербург",
        summary_time: "Время",
        summary_cost: "Стоимость",
        summary_stops: "Остановки",
        summary_interests: "Интересы",

        planner_eyebrow: "Параметры оптимизации",
        planner_title: "Настройте маршрут <span>по вашим ограничениям</span>",
        planner_description:
            "Выберите начальную точку, конечный город, промежуточные остановки, бюджет, лимит времени и приоритет оптимизации.",
        field_start: "Начальная точка",
        field_finish: "Конечная точка",
        field_stops: "Промежуточные точки",
        field_budget: "Бюджет, $",
        field_time: "Максимальное время, ч",
        field_preferences: "Интересы пользователя",
        field_priority: "Приоритет оптимизации",

        pref_culture: "Культура",
        pref_architecture: "Архитектура",
        pref_food: "Еда",
        pref_history: "История",
        pref_sea: "Море",
        pref_modern: "Современность",
        pref_nature: "Природа",
        pref_art: "Искусство",

        priority_balanced: "Сбалансированный",
        priority_fast: "Минимум времени",
        priority_cheap: "Минимум стоимости",
        priority_preferences: "Максимум интересов",

        button_optimize: "Рассчитать оптимальный маршрут",
        preview_title: "Графовая модель маршрута",
        formula_label: "Целевая функция",
        summary_budget: "Бюджет",
        summary_limit: "Лимит времени",
        summary_method: "Метод",
        summary_method_value: "Перебор перестановок"
    },

    en: {
        nav_home: "Home",
        nav_planner: "Planner",
        nav_result: "Result",
        nav_model: "Model",

        hero_eyebrow: "Mathematical travel planning",
        hero_title: "Build an optimal route <span>through multiple points</span>",
        hero_description:
            "The web application selects a travel route based on a graph model, time and budget constraints, and personal user preferences.",
        hero_start: "Start planning",
        hero_model: "View model",

        stat_criteria_label: "Criteria",
        stat_criteria_text: "time, cost, interests, rating",
        stat_model_label: "Model",
        stat_model_text: "weighted route graph",
        stat_score_label: "Score",
        stat_score_text: "route objective function",

        route_preview_title: "Moscow → Saint Petersburg",
        summary_time: "Time",
        summary_cost: "Cost",
        summary_stops: "Stops",
        summary_interests: "Interests",

        planner_eyebrow: "Optimization parameters",
        planner_title: "Set up your route <span>by your constraints</span>",
        planner_description:
            "Choose the starting point, destination, intermediate stops, budget, time limit, and optimization priority.",
        field_start: "Starting point",
        field_finish: "Destination",
        field_stops: "Intermediate stops",
        field_budget: "Budget, $",
        field_time: "Maximum time, h",
        field_preferences: "User interests",
        field_priority: "Optimization priority",

        pref_culture: "Culture",
        pref_architecture: "Architecture",
        pref_food: "Food",
        pref_history: "History",
        pref_sea: "Sea",
        pref_modern: "Modern",
        pref_nature: "Nature",
        pref_art: "Art",

        priority_balanced: "Balanced",
        priority_fast: "Minimum time",
        priority_cheap: "Minimum cost",
        priority_preferences: "Maximum interests",

        button_optimize: "Calculate optimal route",
        preview_title: "Route graph model",
        formula_label: "Objective function",
        summary_budget: "Budget",
        summary_limit: "Time limit",
        summary_method: "Method",
        summary_method_value: "Permutation search"
    }
};

function updateCursorGlassEffect(event) {
    const x = `${event.clientX}px`;
    const y = `${event.clientY}px`;

    document.documentElement.style.setProperty("--cursor-x", x);
    document.documentElement.style.setProperty("--cursor-y", y);
}

function translateCities(language) {
    const dictionary = cityTranslations[language];

    document.querySelectorAll("[data-city]").forEach((element) => {
        const cityKey = element.dataset.city;

        if (dictionary[cityKey]) {
            element.textContent = dictionary[cityKey];
        }
    });
}

function setLanguage(language) {
    const dictionary = translations[language];

    document.documentElement.lang = language;

    document.querySelectorAll("[data-i18n]").forEach((element) => {
        const key = element.dataset.i18n;

        if (dictionary[key]) {
            element.innerHTML = dictionary[key];
        }
    });

    translateCities(language);

    document.querySelectorAll("[data-lang]").forEach((button) => {
        button.classList.toggle("active", button.dataset.lang === language);
    });

    localStorage.setItem("travelRouteLanguage", language);
    window.dispatchEvent(new CustomEvent("languageChanged", { detail: { language } }));
}

document.addEventListener("mousemove", updateCursorGlassEffect);

document.querySelectorAll("[data-lang]").forEach((button) => {
    button.addEventListener("click", () => {
        setLanguage(button.dataset.lang);
    });
});

const savedLanguage = localStorage.getItem("travelRouteLanguage") || "ru";
setLanguage(savedLanguage);

console.log("Travel Route frontend loaded");