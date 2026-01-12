from pydoc_data.topics import topics
import random
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from .models import Words, Symbol_alphabet


def index(request):
    topics = []
    topics = Words.objects.values_list('word_topic', flat=True).distinct()
    return render(request,'LearnCard/index.html', {'topics': topics})

def about(request):
    return render(request,'LearnCard/about.html')

def alphabet(request):
    symbols = []
    symbols  = Symbol_alphabet.objects.all()
    grouped_symbols = [symbols[i:i + 8] for i in range(0, len(symbols), 8)]
    return render(request, 'LearnCard/alphabet.html', {'grouped_symbols': grouped_symbols})

def start_session(request):
    if request.method != 'POST':
        return redirect('LearnCard: index')

    topic_name = request.POST.get('topic')
    mode = request.POST.get('training_mode')
    try:
        count = int(request.POST.get('count', 5))
        count = min(max(count,1), 15)
    except (ValueError, TypeError):
        count = 5

    words = Words.objects.filter(word_topic=topic_name) if topic_name else Words.objects.all()
    word_list=list(words)

    if len(word_list) < count:
        count = len(word_list)

    selected_words = random.sample(word_list, count) if len(word_list) >= count else word_list

    request.session['word_ids'] = [w.id for w in selected_words]
    request.session['current_index']=0
    request.session['score']=0
    request.session['topic_name']=topic_name
    request.session['mode'] = mode

    if selected_words:
        return redirect('LearnCard:card_view', word_id=selected_words[0].id)
    else:
        return render(request, 'LearnCard/index.html',{
            'topics': Words.objects.values_list('word_topic',flat=True).distinct(),
            'error': 'Нет слов для выбранной темы.'
        })

def card_view(request, word_id):
    word_ids = request.session.get('word_ids')
    mode = request.session.get('mode')
    current_index = request.session.get('current_index', 0)

    if not word_ids or current_index >= len(word_ids) or word_id not in word_ids:
        return redirect('LearnCard:training_done')

    current_word = get_object_or_404(Words, id=word_id)

    all_words = Words.objects.exclude(id=current_word.id)
    other_translations = list(all_words.values_list('word_rus', flat=True))[:10]
    options = [current_word.word_rus]

    while len(options)<4:
        if other_translations:
            word_wrong_choice = random.choice(other_translations)
            options.append(word_wrong_choice)
            other_translations.remove(word_wrong_choice)
        else:
            break

    random.shuffle(options)
    if request.method=='POST':
        #selected = request.POST.get('answer')
        #is_correct = selected == current_word.word_rus

        # if is_correct:
        #     request.session['score'] += 1

        request.session['current_index']+=1
        next_index = request.session['current_index']
        if next_index >= len(word_ids):
            return redirect('LearnCard:training_done')

        next_word_id = word_ids[next_index]
        return redirect('LearnCard:card_view', word_id=next_word_id)
    if mode == "with_img":
        return render(request, 'LearnCard/word_card.html',{
            'word': current_word.word_foreign,
            'word_img': current_word.word_image.url if current_word.word_image else None,
            'options': options,
            'current_answer': current_word.word_rus,
            'topic_name': request.session.get('topic_name'),
            'progress': current_index+1,
            'total': len(word_ids),
            'mode':mode,
        })
    else:
        return render(request, 'LearnCard/word_card.html', {
            'word': current_word.word_foreign,
            'options': options,
            'current_answer': current_word.word_rus,
            'topic_name': request.session.get('topic_name'),
            'progress': current_index + 1,
            'total': len(word_ids),
            'mode': mode,
        })

def training_done(request):
    score = request.session.get('score', 0)
    total = len(request.session.get('word_ids', []))
    topic_name = request.session.get('topic_name')

    request.session.flush()

    return render(request, 'LearnCard/done.html',{
        'score': score,
        'total': total,
        'topic_name': topic_name
    })
