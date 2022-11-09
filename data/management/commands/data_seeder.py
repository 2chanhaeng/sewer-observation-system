import os
import csv
from pathlib import Path
from typing import Final
from django.core.management.base import BaseCommand
from data.models import Rainguage, Rainfall, Sewer, Sewage, Gu
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
    help = "Seed data from csv files"

    def handle(self, *args, **options):
        for data_csv in rainguage_csvs:  # 강수 데이터 불러오기
            with open(data_csv, "r", encoding="euc-kr") as f:
                reader = csv.reader(f)
                self.stdout.write(next(reader))  # skip header and print it
                prev_day = 0
                for rg_code, rg_name, gu_code, gu_name, rf, rt in reader:
                    try:  # 구 생성
                        gu, is_created = Gu.objects.get_or_create(
                            name=gu_name, defaults={"code": gu_code}
                        )
                        if is_created:
                            self.stdout.write(self.style.SUCCESS(f"Created {gu}."))
                    except Exception as e:
                        self.stdout.write(
                            f"Raised {self.style.ERROR(e)} while creating {gu_name}."
                        )
                    try:  # 강우량계 생성
                        rg, is_created = Rainguage.objects.get_or_create(
                            rainguage_code=rg_code,
                            defaults={
                                "gu": gu,
                                "rainguage_name": rg_name,
                            },
                        )
                        if is_created:
                            self.stdout.write(self.style.SUCCESS(f"Created {rg}"))
                    except Exception as e:
                        self.stdout.write(
                            f"Raised {self.style.ERROR(e)} while creating {rg_name}."
                        )
                    try:  # 강수 데이터 생성
                        if (
                            today := datetime.strptime(rt, "%Y-%m-%d %H:%M").day
                        ) != prev_day:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Start seeding data of day {prev_day}."
                                )
                            )
                            prev_day = today
                        Rainfall.objects.get_or_create(
                            rainguage=rg,
                            recieve_time=rt + KST,
                            defaults={
                                "rainfall10": rf,
                            },
                        )
                    except Exception as e:
                        self.stdout.write(
                            f"Raised {self.style.ERROR(e)} "
                            f"while creating {rg_name} at {rt}."
                        )
        for data_csv in [sewer_csvs[0]]:  # 하수 데이터 불러오기
            with open(data_csv, "r", encoding="euc-kr") as f:
                reader = csv.reader(f)
                print(" ".join(next(reader)))
                # 고유번호  구분코드 구분명 측정일자               측정일자              측정수위 통신상태
                # 17-0002 17    구로   2021-07-01 00:00:00 2021-07-01 00:00:00 0.10   통신양호

                prev_day = 0
                # 현재 DB서버상황으로 인하여 측정일자가 두 번 나오고 위치 정보가 나오지 않는 문제 발생
                # 따라서 일단 두번째 측정일자를 위치 정보 변수에 지정
                # 추후 DB서버 문제 해결시 다음으로 수정
                # for idn, gubn, gubn_nam, mea_ymd, mea_wal, sig_sta, remark in reader:
                for idn, gubn, gubn_nam, mea_ymd, remark, mea_wal, sig_sta in reader:
                    try:  # 구 생성 혹은 gubn 추가
                        gu, is_created = Gu.objects.get_or_create(
                            name=gubn_nam, defaults={"gubn": gubn}
                        )
                        if is_created:
                            self.stdout.write(self.style.SUCCESS(f"Created {gu}."))
                    except Exception as e:
                        self.stdout.write(
                            f"Raised {self.style.ERROR(e)} while creating {gubn_nam}."
                        )
                    try:  # 하수구 생성
                        sewer, is_created = Sewer.objects.get_or_create(
                            idn=idn,
                            defaults={
                                "gu": gu,
                                "remark": "",  # 상기한 오류 해결 시 remark로 수정
                            },
                        )
                        if is_created:
                            self.stdout.write(self.style.SUCCESS(f"Created {sewer}."))
                    except Exception as e:
                        self.stdout.write(
                            f"Raised {self.style.ERROR(e)} while creating {idn}."
                        )
                    try:  # 하수 데이터(하수구 수위) 생성
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
                        self.stdout.write(
                            f"Raised {self.style.ERROR(e)} "
                            f"while creating {idn} at {mea_ymd}."
                        )
