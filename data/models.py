from django.db import models


class Sewer(models.Model):
    idn = models.CharField(max_length=8, verbose_name="고유번호")
    gubn = models.CharField(max_length=4, verbose_name="구분코드")
    gubn_nam = models.CharField(max_length=4, verbose_name="구분명")
    remark = models.CharField(max_length=255, verbose_name="위치정보")

    def __str__(self):
        return f"Sewer {self.gubn_nam} ({self.remark})"


class Sewage(models.Model):
    sewer = models.ForeignKey(Sewer, on_delete=models.CASCADE)
    mea_ymd = models.DateTimeField(verbose_name="측정일자")
    mea_wal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="측정수위")
    sig_sta = models.CharField(max_length=8, verbose_name="통신상태")

    def __str__(self):
        return f"Sewage data of {self.sewer} at {self.mea_ymd}"


class Rainguage(models.Model):
    rainguage_code = models.SmallIntegerField(verbose_name="강우량계 코드")
    rainguage_name = models.CharField(max_length=8, verbose_name="강우량계명")
    gu_code = models.SmallIntegerField(verbose_name="구청 코드")
    gu_name = models.CharField(max_length=8, verbose_name="구청명")

    def __str__(self):
        return f"Rainguage {self.rainguage_code} ({self.rainguage_name})"


class Rainfall(models.Model):
    rainguage = models.ForeignKey(
        Rainguage, on_delete=models.CASCADE, verbose_name="강우량계"
    )
    rainfall10 = models.FloatField(verbose_name="10분우량")
    recieve_time = models.DateTimeField(verbose_name="자료수집 시각")

    def __str__(self):
        return f"Rainfall data of {self.rainguage} at {self.recieve_time}"
