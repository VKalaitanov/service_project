from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CreateOrderForm
from django.contrib.auth.mixins import LoginRequiredMixin


class OrderView(LoginRequiredMixin, CreateView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        replenishment_balance = form.save(commit=False)
        replenishment_balance.user = self.request.user
        replenishment_balance.save()
        return super().form_valid(form)
