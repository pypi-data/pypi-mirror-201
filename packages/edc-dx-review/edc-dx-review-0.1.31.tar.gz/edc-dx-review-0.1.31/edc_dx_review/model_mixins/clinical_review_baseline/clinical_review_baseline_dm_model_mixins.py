from django.db import models
from django.utils.html import format_html
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models
from edc_model.utils import estimated_date_from_ago
from edc_model.validators import date_not_future


class ClinicalReviewBaselineDmModelMixin(models.Model):
    dm_test = models.CharField(
        verbose_name="Has the patient ever tested for Diabetes?",
        max_length=15,
        choices=YES_NO,
    )

    dm_test_ago = edc_models.DurationYMDField(
        verbose_name="If YES, how long ago was the patient's most recent test for Diabetes?",
        null=True,
        blank=True,
    )

    dm_test_estimated_date = models.DateField(
        null=True,
        blank=True,
        help_text="calculated by the EDC using `dm_test_ago`",
    )

    dm_test_date = models.DateField(
        verbose_name="Date of patient's most recent Diabetes test?",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    dm_dx = models.CharField(
        verbose_name=format_html("Have you ever been diagnosed with Diabetes"),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If YES, complete form `Diabetes Initial Review`",
    )

    def save(self, *args, **kwargs):
        self.dm_test_estimated_date = estimated_date_from_ago(
            instance=self, ago_field="dm_test_ago"
        )
        super().save(*args, **kwargs)  # type: ignore

    class Meta:
        abstract = True
