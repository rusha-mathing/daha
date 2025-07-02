import pytest
from unittest.mock import Mock, patch, MagicMock
from telegram import Update, Message, Chat, User
from main import start, show_courses  # Импортируем из main.py


# Фикстуры для тестов
@pytest.fixture
def update_start():
    update = Mock(spec=Update)
    message = Mock(spec=Message)
    chat = Mock(spec=Chat)
    user = Mock(spec=User)

    user.id = 123
    user.first_name = "TestUser"
    chat.id = 456
    message.chat = chat
    message.from_user = user
    update.message = message

    return update


@pytest.fixture
def update_callback():
    update = Mock(spec=Update)
    query = Mock()
    message = Mock(spec=Message)
    user = Mock(spec=User)

    user.id = 123
    message.chat_id = 456
    query.message = message
    query.from_user = user
    query.data = 'show_courses'
    update.callback_query = query

    return update


@pytest.fixture
def context():
    context = MagicMock()
    context.bot = Mock()
    context.user_data = {}
    context.chat_data = {}
    context.job_queue = Mock()
    return context


# Тесты для команды /start
def test_start_command(update_start, context):
    start(update_start, context)

    # Проверяем отправку сообщения
    update_start.message.reply_text.assert_called_once()

    # Исправленная проверка текста сообщения
    actual_text = update_start.message.reply_text.call_args[0][0]
    assert "Hello! I am a bot for selecting courses from daha.pro." in actual_text

# Тесты для callback show_courses
@patch('main.requests.get')
def test_show_courses_success(mock_get, update_callback, context):
    # Мокируем ответ API с правильной структурой данных
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"title": "Python Basics", "url": "https://daha.pro/python"},
        {"title": "Advanced Django", "url": "https://daha.pro/django"}
    ]
    mock_get.return_value = mock_response

    show_courses(update_callback, context)

    # Проверяем вызовы
    update_callback.callback_query.answer.assert_called_once()
    update_callback.callback_query.edit_message_text.assert_called_once()

    # Получаем аргументы вызова
    call_args = update_callback.callback_query.edit_message_text.call_args

    # Проверяем текст сообщения
    assert call_args[1]['text'] == "📚 Available courses:"

    # Проверяем наличие кнопок с курсами
    reply_markup = call_args[1]['reply_markup']
    assert len(reply_markup.inline_keyboard) == 2  # Должно быть 2 кнопки (по числу курсов)
    assert reply_markup.inline_keyboard[0][0].text == "Python Basics"
    assert reply_markup.inline_keyboard[0][0].url == "https://daha.pro/python"
    assert reply_markup.inline_keyboard[1][0].text == "Advanced Django"
    assert reply_markup.inline_keyboard[1][0].url == "https://daha.pro/django"

@patch('main.requests.get')
def test_show_courses_api_error(mock_get, update_callback, context):
    # Мокируем ошибку API
    mock_response = Mock()
    mock_response.status_code = 403
    mock_get.return_value = mock_response

    show_courses(update_callback, context)

    update_callback.callback_query.edit_message_text.assert_called_once_with(
        "API access error. Please check your key."
    )


@patch('main.requests.get')
def test_show_courses_empty_response(mock_get, update_callback, context):
    # Мокируем пустой ответ
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    show_courses(update_callback, context)

    update_callback.callback_query.edit_message_text.assert_called_once_with(
        "No courses found."
    )


@patch('main.requests.get')
def test_show_courses_exception(mock_get, update_callback, context):
    mock_get.side_effect = Exception("API error")
    show_courses(update_callback, context)
    update_callback.callback_query.edit_message_text.assert_called_once_with(
        "⚠️ API is not responding. Please try again later."
    )