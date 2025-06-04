import uuid
from django.db import models
from django.utils.text import slugify 
from django.core.exceptions import ValidationError

class Categories(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Слаг", blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True, verbose_name="Изображение категории")

    class Meta:
        db_table = "category"
        verbose_name = "категорию"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) 

        super().save(*args, **kwargs)


class Products(models.Model):
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name="Категория", related_name="products") 
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Изображение товара")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Слаг", blank=True)  
    name = models.CharField(max_length=200, verbose_name="Название товара")
    article = models.CharField(max_length=20, blank=True, null=True, verbose_name="Артикул", unique=True) 
    height = models.FloatField(blank=True, null=True, verbose_name="Высота")
    width = models.FloatField(blank=True, null=True, verbose_name="Ширина")
    depth = models.FloatField(blank=True, null=True, verbose_name="Глубина")
    hardware = models.CharField(max_length=50, blank=True, null=True, verbose_name="Фурнитура")
    material = models.CharField(max_length=50, blank=True, null=True, verbose_name="Материал")
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name="Цвет")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    class Meta:
        db_table = "product"
        verbose_name = "товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} (Артикул: {self.article})" # Улучшено отображение

    def save(self, *args, **kwargs):
        # Автоматическое создание артикула
        if not self.article:
            self.article = self.generate_unique_article()

        # Автоматическое создание slug
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def generate_unique_article(self):
        """Генерирует уникальный артикул для продукта."""
        while True:
            article = str(uuid.uuid4())[:8].upper()  # UUID (8 символов)
            if not Products.objects.filter(article=article).exists():
                return article

    def clean(self):  # Валидация модели
        """Проверяет уникальность slug для каждой категории."""
        if self.slug:
            # Проверяем, существует ли уже продукт с таким slug в этой категории
            qs = Products.objects.filter(category=self.category, slug=self.slug)
            if self.pk:  # Исключаем текущий объект при обновлении
                qs = qs.exclude(pk=self.pk)

            if qs.exists():
                raise ValidationError({'slug': 'Товар с таким  "slug" уже существует в этой категории.'})
