from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import ListView

from service.models import Service, Category


class HomePage(ListView):
    template_name = 'service/index.html'
    context_object_name = 'services'
    title_page = 'Главная страница'

    def get_queryset(self):
        category_id = self.request.GET.get('category')  # Получаем id категории из запроса
        if category_id:
            return Service.objects.filter(category_id=category_id).select_related('category').prefetch_related('details')
        return Service.objects.all().select_related('category').prefetch_related('details')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Добавляем категории в контекст
        context['selected_category_id'] = self.request.GET.get('category')  # Добавляем id выбранной категории
        return context

def load_services(request):
    category_id = request.GET.get('category')
    services = Service.objects.filter(category_id=category_id).select_related('category').prefetch_related('details') if category_id else Service.objects.all().select_related('category').prefetch_related('details')
    html = render_to_string('service/_services_list.html', {'services': services})
    return JsonResponse({'html': html})




def about(request):
    return render(
        request,
        'service/about.html',
    )
