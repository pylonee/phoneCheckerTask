import os.path
import requests
import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from check_phone_api.models import PhoneRange

class Command(BaseCommand):
    def handle(self, *args, **options):

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        FILES_DIR = os.path.join(BASE_DIR, 'files')

        files = [
            os.path.join(FILES_DIR, 'ABC-3xx.csv'),
        ]

        self.stdout.write('check_phones parser start update')

        for uFile in files:
            self.stdout.write(f"file: {uFile}")

            try:

                with open(uFile, 'r', encoding='utf-8-sig') as file:
                    data = csv.DictReader(file, delimiter=';')
                    rowCount = 0

                    with transaction.atomic():
                        for row in data:
                            try:
                                startNum = self.formatNum(row['АВС/ DEF'], row['От'])
                                endNum = self.formatNum(row['АВС/ DEF'], row['До'])

                                PhoneRange.objects.update_or_create(
                                    code=f'{row["АВС/ DEF"]}_{startNum}_{endNum}',
                                    defaults={
                                        'startRange': startNum,
                                        'endRange': endNum,
                                        'capacity': int(row['Емкость']),
                                        'operator': row['Оператор'],
                                        'region': row['Регион'],
                                        'inn': row.get('ИНН', ''),
                                    }
                                )
                                rowCount += 1

                                if rowCount >= 100:
                                    break

                            except (ValueError, KeyError) as e:
                                self.stdout.write((self.style.WARNING(f'Errow in row: {e}')))

                    self.stdout.write(self.style.SUCCESS(f'Parce {rowCount} from {uFile}'))

            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Error file {uFile}: {e}'))
            except Exception as e:
                self.stdout.write((self.style.ERROR(f'Error {uFile}: {e}')))

        self.stdout.write(self.style.SUCCESS(f'check_phones parser successfully end update'))

    def formatNum(self, code, num):
        code = code.replace('-', '')
        fullNum = '7' + code + num

        return int(fullNum)