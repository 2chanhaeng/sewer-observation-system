from django.db import models


class Sewer(models.Model):
    idn = models.CharField(max_length=8, verbose_name="고유번호")
    gubn = models.CharField(max_length=4, verbose_name="구분코드")
    gubn_nam = models.CharField(max_length=4, verbose_name="구분명")
    remark = models.CharField(max_length=255, verbose_name="위치정보")

    def __str__(self):
        return f"Sewer {self.idn} ({self.remark})"


class Sewage(models.Model):
    sewer = models.ForeignKey(Sewer, on_delete=models.CASCADE)
    mea_ymd = models.DateTimeField(verbose_name="측정일자")
    mea_wal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="측정수위")
    sig_sta = models.CharField(max_length=8, verbose_name="통신상태")

    def __str__(self):
        return f"Sewage data of {self.sewer.idn} at {self.mea_ymd}"
