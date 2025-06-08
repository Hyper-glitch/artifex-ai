from http import HTTPStatus

SUCCESS_SIGN_UP = "Вы успешно зарегистрированы в системе 🎉"
ALREADY_SIGN_UP = "Вы уже зарегистрированны в системе"
START_MESSAGE = (
    "👋 Привет! Я бот Artifex-AI.\n\n"
    "Для начала работы Вам необходимо зарегистрироваться в системе."
)
START_TO_GENERATE_MESSAGE = "Для старта генерации изображения нажмите команду /generate"
AWAITING_PROMPT_MESSAGE = "Пожалуйста, опишите изображение, которое вы хотите создать (in English):"
PROCESSING_MESSAGE = "⏳ Добавил в очередь на генерацию.\nБудет готово примерно через 10 секунд."
ACCEPTED_MESSAGE = "Супер! Изображение принято ✅"
RATE_PROMPT_MESSAGE = "Пожалуйста, оцените сгенерированное изображение по шкале от 1 до 5 ⭐"
RATE_THANKS_MESSAGE = "Спасибо за вашу оценку! 🙏"
ASK_NEW_PROMPT_MESSAGE = "Если нужно новое изображение — просто напиши описание."

ERROR_MESSAGE = "⚠️ Упс, произошла ошибка. Попробуйте еще раз."
NOT_AUTH_MESSAGE = "❌ Вам необходимо зарегистрироваться в системе."
ERROR_TASK_MESSAGE = "❌ Error creating task."

STATUS_MESSAGES = {
    HTTPStatus.CREATED: SUCCESS_SIGN_UP,
    HTTPStatus.CONFLICT: ALREADY_SIGN_UP,
}
