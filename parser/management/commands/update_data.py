import requests
import csv
from io import StringIO
from django.core.management.base import BaseCommand
from django.db import transaction
from check_phone_api.models import PhoneRange

class Command(BaseCommand):
    def handle(self, *args, **options):
        urls = [
            'https://opendata.digital.gov.ru/downloads/ABC-3xx.csv',
            'https://opendata.digital.gov.ru/downloads/ABC-4xx.csv',
            'https://opendata.digital.gov.ru/downloads/ABC-8xx.csv',
            'https://opendata.digital.gov.ru/downloads/DEF-9xx.csv',
        ]

        self.stdout.write('check_phones parser start update')

        for url in urls:
            self.stdout.write(f"file: {url}")

            try:
                resp = requests.get(url, timeout=30)
                resp.encoding = 'utf-8-sig'

                if resp.status_code != 200:
                    self.stdout.write(self.style.WARNING(f'file {url} error: {resp.status_code} - {resp.text}'))
                    continue

                csvData = StringIO(resp.text)

                data = csv.DictReader(csvData, delimiter=';')

                rowCount=0

                with transaction.atomic():
                    for row in data:
                        try:
                            startNum = self.formatNum(row['ABC/ DEF'], row['От'])
                            endNum = self.formatNum(row['ABC/ DEF'], row['До'])

                            PhoneRange.objects.update_or_create(
                                code=f'{row["АВС/ DEF"]}_{startNum}_{endNum}',
                                defaults={
                                    'startRange': startNum,
                                    'endRange': endNum,
                                    'capacity': int(row['Емкость']),
                                    'operator': row['Оператор'],
                                    'region': row['Регион'],
                                    'inn': row['ИНН', ''],
                                }
                            )
                            rowCount+=1

                        except (ValueError, KeyError) as e:
                            self.stdout.write((self.style.WARNING(f'Errow in row: {e}')))

                self.stdout.write(self.style.SUCCESS(f'Parce {rowCount} from {url}'))

            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Error file {url}: {e}'))
            except Exception as e:
                self.stdout.write((self.style.ERROR(f'Error {url}: {e}')))

        self.stdout.write(self.style.SUCCESS(f'check_phones parser successfully end update'))

    def formatNum(self, code, num):
        code = code.replace('-', '')
        fullNum = '7' + code + num

        return int(fullNum)