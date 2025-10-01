from django.core.exceptions import ValidationError
from django.db import models


class Product(models.Model):
    """Продукт: название, модель, дата выхода на рынок."""

    name = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    release_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.name} ({self.model})"


class NetworkUnit(models.Model):
    """
    Звено сети (завод / розничная сеть / ИП).
    Уровень определяется глубиной по цепочке поставщиков:
      - уровень 0: supplier = None (завод)
      - уровень 1: supplier -> уровень 0
      - уровень 2: supplier -> уровень 1
    Глубина > 2 запрещена. Циклы запрещены.
    """

    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)

    supplier = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="clients",
        help_text="Поставщик (предыдущий по иерархии объект сети). Для уровня 0 оставьте пустым.",
    )
    products = models.ManyToManyField(
        Product, blank=True, related_name="suppliers", help_text="Продукты, продающиеся через данное звено."
    )

    debt = models.DecimalField("Задолженность перед поставщиком", max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"

    def __str__(self) -> str:
        return f"{self.name} (уровень {self.level})"

    @property
    def level(self) -> int:
        """Вычисляемый уровень по цепочке поставщиков (0..2)."""
        depth = 0
        parent = self.supplier
        while parent is not None:
            depth += 1
            parent = parent.supplier
        return depth

    def clean(self):
        """Запрещаем самоссылку, циклы и глубину > 2."""
        if self.pk and self.supplier_id == self.pk:
            raise ValidationError("Поставщик не может ссылаться сам на себя.")

        depth = 0
        seen = set()
        parent = self.supplier
        while parent is not None:
            if parent.pk in seen:
                raise ValidationError("Обнаружен цикл в иерархии поставщиков.")
            seen.add(parent.pk)
            depth += 1
            if depth > 2:
                raise ValidationError("Глубина иерархии не может превышать 2 (уровни 0, 1, 2).")
            parent = parent.supplier

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
