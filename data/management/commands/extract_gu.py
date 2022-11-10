from django.core.management.base import BaseCommand
from data.models import Gu, Sewer, Rainguage


class Command(BaseCommand):
    help = "Separate gu from rainguage and sewer"

    """
    When the Sewer and Rainguage models are created,
    the Gu model doesn't exist yet.
    This command is needed to extract gu from sewer and rainguage.
    That makes it easier to link sewer and rainguage.
    """

    def handle(self, *args, **options):
        for rg in Rainguage.objects.all():
            gu, is_created = Gu.objects.get_or_create(
                name=rg.gu_name[:-1],  # ㅇㅇ구 -> ㅇㅇ
                defaults={
                    "code": rg.gu_code,
                },
            )
            if is_created:
                self.stdout.write(self.style.SUCCESS(f"Created {gu}"))
            rg.gu = gu
            rg.gu_code = None
            rg.gu_name = None
            rg.save()
        for sewer in Sewer.objects.all():
            gu, is_created = Gu.objects.update_or_create(
                name=sewer.gubn_nam,
                defaults={"gubn": sewer.gubn},
            )
            if is_created:
                self.stdout.write(self.style.SUCCESS(f"Created {gu}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Updated {gu}"))
            sewer.gu = gu
            sewer.gubn = None
            sewer.gubn_nam = None
            sewer.save()
