from django.db import models
from django.utils.html import format_html
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models
from edc_model.utils import estimated_date_from_ago
from edc_model.validators import date_not_future


class ClinicalReviewBaselineHivModelMixin(models.Model):
    hiv_test = models.CharField(
        verbose_name="Has the patient ever tested for HIV infection?",
        max_length=15,
        choices=YES_NO,
    )

    hiv_test_ago = edc_models.DurationYMDField(
        verbose_name="If YES, how long ago was the patient's most recent HIV test?",
        null=True,
        blank=True,
        help_text="IF HIV(+), ESTIMATE WHEN FIRST TESTED POSITIVE. ",
    )

    hiv_test_estimated_date = models.DateField(
        null=True,
        blank=True,
        editable=False,
        help_text="calculated by the EDC using `hiv_test_ago`",
    )

    hiv_test_date = models.DateField(
        verbose_name="Date of patient's most recent HIV test?",
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text="IF HIV(+), DATE PATIENT FIRST TESTED POSITIVE. ",
    )

    hiv_dx = models.CharField(
        verbose_name=format_html(
            "Has the patient ever tested <U>positive</U> for HIV infection?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If YES, complete form `HIV Initial Review`",
    )

    def save(self, *args, **kwargs):
        self.hiv_test_estimated_date = estimated_date_from_ago(
            instance=self, ago_field="hiv_test_ago"
        )
        super().save(*args, **kwargs)  # type: ignore

    class Meta:
        abstract = True
