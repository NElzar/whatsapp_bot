from bot.models import Script, Step

scripts = {
    '1': {
        'title': 'Футболки',
        'steps': [
            {'id': 1, 'next': 2, 'text': 'Какого света?', 'answers': ['Белый', 'Черный']},
            {'id': 2, 'next': 3, 'text': 'Какой материал?', 'answers': ['Хлопок', 'Синтетика']},
            {'id': 3, 'next': 4, 'text': 'Какой размер?', 'answers': ['1-20', '20-40', '40-90']},
            {'id': 4, 'next': None, 'text': 'Все ок, гудбай америка'},
        ]
    },
    '2': {
        'title': 'Куртки',
        'steps': [
            {'id': 5, 'next': 6, 'text': 'Какого света?', 'answers': ['Белый', 'Черный']},
            {'id': 6, 'next': 7, 'text': 'Какой материал?', 'answers': ['Хлопок', 'Синтетика']},
            {'id': 7, 'next': 8, 'text': 'Какой размер?', 'answers': ['1-20', '20-40', '40-90']},
            {'id': 8, 'next': None, 'text': 'Все ок, гудбай америка'},
        ]
    },
}


def get_products_titles():
    return Script.objects.all().values_list('title', flat=True)


def get_step(product=None, step=None) -> Step:
    if step is None:
        script = Script.objects.filter(title=product).first()
        return script.steps.first()
    if step is not None:
        return Step.objects.get(id=step)


def get_answers_step(step_id=None):
    if step_id is None:
        return get_products_titles()
    step = Step.objects.get(id=step_id)
    return step.answers.all().values_list('text', flat=True)
