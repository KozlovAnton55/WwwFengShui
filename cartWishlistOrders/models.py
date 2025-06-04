from django.db import models
from django.conf import settings
from goods.models import Products


class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name="Пользователь",
    )
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} в корзине пользователя {self.user.username}"

    def total_price(self):
        return self.quantity * self.product.price

    class Meta:
        verbose_name = "Корзина товаров"
        verbose_name_plural = "Корзины товаров"


class WishlistItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist_items",
        verbose_name="Пользователь",
    )
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, verbose_name="Товар"
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.product.name} в избранных пользователя {self.user.username}"

    class Meta:
        verbose_name = "Избранные товары"
        verbose_name_plural = "Избранные товары"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Пользователь",
    )
    order_number = models.CharField(
        max_length=20, unique=True, verbose_name="Номер заказа"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Номер заказа")
    delivery_address = models.TextField(verbose_name="Адрес доставки")
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Общая сумма"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "В ожидании"),
            ("processing", "В обработке"),
            ("shipped", "Отправлен"),
            ("delivered", "Доставлен"),
            ("cancelled", "Отменен"),
        ],
        default="pending",
    )

    def __str__(self):
        return f"Заказ №{self.order_number} пользователя {self.user.username}"

    class Meta:
        verbose_name = "Текущий заказ"
        verbose_name_plural = "Текущие заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="Заказ",
    )
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return (
            f"{self.quantity} x {self.product.name} в заказе {self.order.order_number}"
        )

    class Meta:
        verbose_name = "Элементы заказа"
        verbose_name_plural = "Элементы заказов"
