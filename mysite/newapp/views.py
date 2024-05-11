from django.shortcuts import render
from .models import Movie
from django.views.generic import ListView
from django.core.paginator import Paginator

# Create your views here.


def movie_list(request):
    movies = Movie.objects.all()
    movie_title = request.GET.get('movie_title')
    if movie_title is not None and movie_title != "":
        movies = Movie.objects.filter(title__icontains=movie_title)
        # icontains大小寫都會進，contains對大小寫敏感

    paginator = Paginator(movies, 2)
    page = request.GET.get('page')
    movies = paginator.get_page(page)
    return render(request, 'newapp/movie_list.html', {'movies': movies})


class MovieListView(ListView):
    model = Movie
    
    template_name = 'newapp/movie_list.html'
    paginate_by = 2
    # 普通寫法的2-4行濃縮成上面這行
    context_object_name = 'movies'
    # 普通寫法，的 movies = paginator.get_page(page)可以設定分頁器的object名稱，
    # 下面這種會直接設定為【page_obj】，
    # 在html所有有關分頁器的object名稱都要用page_obj，
    # 不能用context_object_name(movies)

    def get_queryset(self):
        queryset = super().get_queryset()
        movie_title = self.request.GET.get('movie_title')
        if movie_title:
            queryset = queryset.filter(title__icontains=movie_title)
        return queryset


