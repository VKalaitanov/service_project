from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import ListView

from service.models import Service, Category, Tag


class HomePage(ListView):
    template_name = 'service/index.html'
    context_object_name = 'services'
    title_page = 'Главная страница'

    def get_queryset(self):
        category_id = self.request.GET.get('category')  # Получаем id категории из запроса
        tag_id = self.request.GET.get('tag')  # Получаем id выбранного тега
        queryset = Service.objects.all().select_related('category').prefetch_related('details')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)  # Фильтруем по тегам

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Добавляем категории в контекст
        context['tags'] = Tag.objects.all()  # Добавляем теги в контекст
        context['selected_category_id'] = self.request.GET.get('category')  # Добавляем id выбранной категории
        context['selected_tag_id'] = self.request.GET.get('tag')  # Добавляем id выбранного тега
        return context


def load_services(request):
    category_id = request.GET.get('category')
    tag_id = request.GET.get('tag')  # Получаем id тега

    services = Service.objects.all().select_related('category').prefetch_related('details')

    if category_id:
        services = services.filter(category_id=category_id)
    if tag_id:
        services = services.filter(tags__id=tag_id)  # Фильтруем услуги по тегам

    html = render_to_string('service/_services_list.html', {'services': services})
    return JsonResponse({'html': html})





def about(request):
    return render(
        request,
        'service/about.html',
    )
