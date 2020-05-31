from generative_model import get_answer_by_generative_model
from intents import (
    get_response_by_intent, get_failure_phrase, get_intent)


stats = {
    'requests': 0,
    'byscript': 0,
    'bygenerative': 0,
    'stub': 0
}


def generate_answer(text):
    stats['requests'] += 1

    # NLU
    intent = get_intent(text)

    # Make answer
    # by script
    if intent:
        stats['byscript'] += 1
        response = get_response_by_intent(intent)
        return response

    # use generative model
    answer = get_answer_by_generative_model(text)
    if answer:
        stats['bygenerative'] += 1
        return answer

    # use stub
    stats['stub'] += 1
    failure_phrase = get_failure_phrase()
    return failure_phrase


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def text(update, context):
    """Echo the user message."""
    answer = generate_answer(update.message.text)
    print(update.message.text, '->', answer)
    print(stats)
    print()
    update.message.reply_text(answer.capitalize())


def error(update, context):
    """Log Errors caused by Updates."""
    update.message.reply_text('Я работаю только с текстом')
