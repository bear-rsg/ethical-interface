from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import models


def prompt_get(request):
    """
    Function-based view to return JSON data for a single Prompt data object
    """

    user_search_query = request.GET.get('user_search_query', '')
    if len(user_search_query):
        # Try to find a match for each word in user search query
        # E.g. if user searches "the ukraine war" then match "ukraine" and return prompt data
        # If multiple found, return the highest priority prompt
        for word in user_search_query.split(' '):
            prompt = models.Prompt.objects.filter(triggers__trigger_text__icontains=word).order_by('-priority').first()
            if prompt:
                return JsonResponse({
                    'prompt': {
                        'id': prompt.id,
                        'topic': str(prompt.topic),
                        'prompt_content': prompt.prompt_content.replace('\n', '<br>'),
                        'response_required': prompt.response_required
                    }
                })

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
