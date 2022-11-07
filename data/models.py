from django.db import models


class Sewer(models.Model):
    IDN = models.CharField(max_length=8, verbose_name="고유번호")
    GUBN = models.CharField(max_length=4, verbose_name="구분코드")
    GUBN_NAM = models.CharField(max_length=4, verbose_name="구분명")
    MEA_YMD = models.DateTimeField(verbose_name="측정일자")
    MEA_WAL = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="측정수위")
    SIG_STA = models.CharField(max_length=8, verbose_name="통신상태")
    REMARK = models.CharField(max_length=255, verbose_name="위치정보")

    def __str__(self):
        return f"{self.IDN} {self.MEA_YMD}"
