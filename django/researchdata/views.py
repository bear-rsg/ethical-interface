from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from . import models


def prompt_get(request):
    """
    Function-based view to return JSON data for a single Prompt data object
    """

    user_search_query = request.GET.get('user_search_query', '')
    search_exact = int(request.GET.get('search_exact', '0'))
    topics_exclude_get = request.GET.get('topics_exclude', '')
    topics_exclude = []
    if len(topics_exclude_get):
        for topic in topics_exclude_get.split(','):
            if topic:
                topics_exclude.append(int(topic))
    if len(user_search_query):
        # If user has requested an exact search, include the full search term
        # Otherwise, do a search for each individual word in the search query
        search_terms = [user_search_query] if search_exact == 1 else user_search_query.split(' ')
        for search_term in search_terms:
            # Clean search term, if user hasn't asked for an exact search
            # e.g. if user searches "walking" or "walks" remove the extra chars to just get "walk"
            if search_exact == 0:
                # Remove 's' from end, as this is likely plural
                if len(search_term) > 2 and search_term.endswith('s'):
                    search_term = search_term[:-1]
                # Remove 'ing' and 'ies' from end
                elif len(search_term) > 4 and search_term.endswith('ing') or search_term.endswith('ies'):
                    search_term = search_term[:-3]
            # Find a prompt that matches the search term
            prompts = models.Prompt.objects.all()
            if len(topics_exclude):
                prompts = prompts.exclude(id__in=topics_exclude)
            prompt = prompts.filter(triggers__trigger_text__icontains=search_term).order_by('-priority').first()
            # Build the response data dict, with a list of available topics
            response_data = {
                'topics': [
                    {**model_to_dict(topic), **{'excluded': 1 if topic.id in topics_exclude else 0}}
                    for topic in models.TopicGroup.objects.all()
                ]
            }
            # If a prompt is found, add it to the response dict
            if prompt:
                response_data['prompt'] = {
                    'id': prompt.id,
                    'topic': str(prompt.topic),
                    'prompt_content': prompt.prompt_content.replace('\n', '<br>'),
                    'response_required': prompt.response_required
                }
            return JsonResponse(response_data)

    # If a matching prompt can't be found then return a False prompt to client
    return JsonResponse({'prompt': False})


@csrf_exempt
def response_post(request):
    """
    Function-based view to create a new Response data object
    """

    user_response_content = request.POST.get('user_response_content', '')
    active_prompt_id = request.POST.get('active_prompt_id', '')
    response = None
    if len(user_response_content) and len(active_prompt_id):
        response = models.Response.objects.create(
            prompt=models.Prompt.objects.get(id=active_prompt_id),
            response_content=user_response_content
        )
    data = {'response_saved': 1 if response else 0}
    return JsonResponse(data)


@csrf_exempt
def notrelevantreport_post(request):
    """
    Function-based view to create a new NotRelevantReport data object
    """

    active_prompt_id = request.POST.get('active_prompt_id', '')
    user_search_query = request.POST.get('user_search_query', '')
    report = None
    if len(user_search_query) and len(active_prompt_id):
        report = models.NotRelevantReport.objects.create(
            prompt=models.Prompt.objects.get(id=active_prompt_id),
            user_search_query=user_search_query
        )
    data = {'report_saved': 1 if report else 0}
    return JsonResponse(data)
