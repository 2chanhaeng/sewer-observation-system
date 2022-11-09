import os
import csv
from pathlib import Path
from typing import Final
from django.core.management.base import BaseCommand
from data.models import Rainguage, Rainfall, Sewer, Sewage
from datetime import datetime

KST = " +09:00"
rainguage_dir = Path("./seed_data/rainguage").absolute()
sewer_dir = Path("./seed_data/sewer").absolute()


def get_csv_data(dir: Path | str = rainguage_dir) -> list:
    files: Final = os.listdir(dir)
    fns: Final = filter(lambda x: x.endswith(".csv"), files)
    csvs: Final = [dir / fn for fn in fns]
    return csvs


rainguage_csvs = get_csv_data(rainguage_dir)
sewer_csvs = get_csv_data(sewer_dir)


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        for data_csv in rainguage_csvs:
            with open(data_csv, "r", encoding="euc-kr") as f:
                reader = csv.reader(f)
                print(next(reader))
                prev_day = 0
                for rg_code, rg_name, gu_code, gu_name, rf, rt in reader:
                    try:
                        if prev_day == 0:
                            row = [rg_code, rg_name, gu_code, gu_name, rf, rt]
                            self.stdout.write(" ".join(row))
                        rg, is_created = Rainguage.objects.get_or_create(
                            rainguage_code=rg_code,
                            rainguage_name=rg_name,
                            gu_code=gu_code,
                            gu_name=gu_name,
                        )
                        if is_created:
                            self.stdout.write(self.style.SUCCESS(f"Created {rg}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error: {e}"))
                    try:
                        Rainfall.objects.create(
                            rainguage=rg,
                            rainfall10=rf,
                            recieve_time=rt + " +09:00",
                        )
                        if (
                            today := datetime.strptime(rt, "%Y-%m-%d %H:%M").day
                        ) != prev_day:
                            self.stdout.write(self.style.SUCCESS(f"{prev_day}"))
                            prev_day = today
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"error: {e}"))
        for data_csv in [sewer_csvs[0]]:
            with open(data_csv, "r", encoding="euc-kr") as f:
                reader = csv.reader(f)
                print(" ".join(next(reader)))
                # 고유번호  구분코드 구분명 측정일자               측정일자              측정수위 통신상태
                # 17-0002 17    구로   2021-07-01 00:00:00 2021-07-01 00:00:00 0.10   통신양호

                prev_day = 0
                # 현재 DB서버상황으로 인하여 측정일자가 두번 나오고 위치 정보가 나오지 않는 문제 발생
                # 따라서 일단 두번째 측정일자를 위치 정보 변수에 지정
                # 추후 DB서버 문제 해결시 다음으로 수정
                # for idn, gubn, gubn_nam, mea_ymd, mea_wal, sig_sta, remark in reader:
                for idn, gubn, gubn_nam, mea_ymd, remark, mea_wal, sig_sta in reader:
                    try:
                        if prev_day == 0:
                            row = [idn, gubn, gubn_nam, mea_ymd, remark, mea_wal, sig_sta]
                            self.stdout.write(" ".join(row))
                        sewer, is_created = Sewer.objects.get_or_create(
                            idn=idn,
                            gubn=gubn,
                            gubn_nam=gubn_nam,
                            remark="",  # remark,
                        )
                        if is_created:
                            self.stdout.write(self.style.SUCCESS(f"Created {sewer}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error: {e}"))
                    try:
                        Sewage.objects.create(
                            sewer=sewer,
                            mea_ymd=mea_ymd + KST,
                            mea_wal=mea_wal,
                            sig_sta=sig_sta,
                        )
                        if (
                            today := datetime.strptime(mea_ymd, "%Y-%m-%d %H:%M:%S").day
                        ) != prev_day:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Start seeding data of day {prev_day}."
                                )
                            )
                            prev_day = today
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"error: {e}"))
                        raise e
