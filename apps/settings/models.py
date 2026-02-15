from django.db import models
from core.mixins import TimeStampedMixin, SoftDeleteMixin


class Branch(TimeStampedMixin, SoftDeleteMixin):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("onboarding", "Onboarding"),
        ("inactive", "Inactive"),
    )

    name = models.CharField(max_length=200, unique=True, verbose_name="Filial nomi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    address = models.TextField(null=True, blank=True, verbose_name="Manzil")

    class Meta:
        db_table = "branches"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Location(TimeStampedMixin, SoftDeleteMixin):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    name = models.CharField(max_length=200, verbose_name="Joylashuv nomi")
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="locations"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    class Meta:
        db_table = "locations"
        ordering = ["name"]
        unique_together = ["name", "branch"]

    def __str__(self):
        return f"{self.name} - {self.branch.name}"


class Department(TimeStampedMixin, SoftDeleteMixin):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("onboarding", "Onboarding"),
        ("inactive", "Inactive"),
    )

    name = models.CharField(max_length=200, verbose_name="Bo'lim nomi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    class Meta:
        db_table = "departments"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ReportType(TimeStampedMixin, SoftDeleteMixin):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )
    TYPE_CHOICES = (
        ("nearmiss", "Near Miss"),
        ("observation", "Observation"),
        ("accident", "Accident"),
        ("incident", "Incident"),
    )

    name = models.CharField(max_length=200, verbose_name="Hisobot turi nomi")
    type_code = models.CharField(max_length=20, choices=TYPE_CHOICES, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")

    class Meta:
        db_table = "report_types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class RiskCategory(TimeStampedMixin, SoftDeleteMixin):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )
    SEVERITY_CHOICES = (
        ("high", "Yuqori"),
        ("medium", "O'rta"),
        ("low", "Past"),
    )

    name = models.CharField(max_length=200, verbose_name="Xavf toifasi nomi")
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")

    class Meta:
        db_table = "risk_categories"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_severity_display()})"
