from django.views.generic import DetailView, ListView

from .models import BlogPost, GalleryImage, Testimonial


class BlogListView(ListView):
    model = BlogPost
    template_name = "content/blog_list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        return BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "content/blog_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_posts"] = (
            BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)
            .exclude(pk=self.object.pk)[:3]
        )
        return context


class TestimonialListView(ListView):
    model = Testimonial
    template_name = "content/testimonials.html"
    context_object_name = "testimonials"

    def get_queryset(self):
        return Testimonial.objects.filter(is_active=True)


class GalleryListView(ListView):
    model = GalleryImage
    template_name = "content/gallery.html"
    context_object_name = "gallery_items"

    def get_queryset(self):
        return GalleryImage.objects.filter(is_active=True)
