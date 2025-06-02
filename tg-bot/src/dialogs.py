from http import HTTPStatus

WELCOME_MESSAGE = "Добро пожаловать! Нажмите кнопку ниже для регистрации:"
SUCCESS_SIGN_UP = "Вы успешно зарегистрированы в системе 🎉"
ALREADY_SIGN_UP = "Вы уже зарегистрированны в системе"
START_MESSAGE = (
    "👋 Привет! Я бот Artifex-AI.\n\n"
    "Опиши, что ты хочешь сгенерировать, и я создам визуал в фирменном стиле."
)
PROCESSING_MESSAGE = "⏳ Добавил в очередь на генерацию.\nБудет готово примерно через 10 секунд."
ACCEPTED_MESSAGE = "Супер! Изображение принято ✅"
RATE_PROMPT_MESSAGE = "Пожалуйста, оцените сгенерированное изображение по шкале от 1 до 5 ⭐"
RATE_THANKS_MESSAGE = "Спасибо за вашу оценку! 🙏"
ASK_NEW_PROMPT_MESSAGE = "Если нужно новое изображение — просто напиши описание."
REGENERATING_MESSAGE = "Перегенерирую 🔁"
ERROR_MESSAGE = "⚠️ Упс, произошла ошибка. Попробуйте еще раз."
NOT_AUTH_MESSAGE = "❌ Вы не зарегистрированы в системе. Обратитесь к администратору."

STATUS_MESSAGES = {
    HTTPStatus.CREATED: SUCCESS_SIGN_UP,
    HTTPStatus.CONFLICT: ALREADY_SIGN_UP,
}
