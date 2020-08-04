import pandas as pd
from django.db import transaction
import datetime as dt
from django.utils import timezone

from registry.models import Manufacturer, Operator, Aircraft, TypeCertificate,\
    Address


def parse_sheet(file_obj, institute, user_id):
    status, error = parse_items_content(file_obj, institute, user_id)
    return status, error


def get_clean_data_frame(file_obj, sheet_name):
    df = pd.read_excel(file_obj, sheet_name=sheet_name, headers=1)
    return df


def parse_items_content(file_obj, institute, user_id):
    df = get_clean_data_frame(file_obj, 'sheet')
    clean_df = df[df["UIN"].notnull()].iloc[:, 0:80]
    na_to_zero_df = clean_df.fillna(0)
    data = na_to_zero_df.values.tolist()

    # Manufacturer.objects.all().delete()
    # Operator.objects.all().delete()
    # Aircraft.objects.all().delete()

    with transaction.atomic():
        for row in data:
            try:
                address, _ = Address.objects.update_or_create(
                    address_line_1=row[4],
                    address_line_2=row[4],
                    address_line_3=row[4],
                    defaults={
                        'address_line_1': row[4],
                        'address_line_2': row[4],
                        'address_line_3': row[4],
                    }
                )
            except Exception as e:
                print("address error", str(e))
            try:
                manufacturer, _ = Manufacturer.objects.update_or_create(
                    full_name=row[7],
                    defaults={
                        'full_name': row[7]
                    }
                )
            except Exception as e:
                print("manufacturer error", str(e))
            try:
                operator, _ = Operator.objects.update_or_create(
                    company_name=row[3],
                    phone_number=row[5],
                    defaults={
                        'company_name': row[3],
                        'address': address,
                        'phone_number': row[5],
                        'email': row[6]
                    }
                )
            except Exception as e:
                print("operator error", str(e))
            # print("operator", operator)
            try:
                aircraft = Aircraft.objects.update_or_create(
                    unid=row[2],
                    defaults={
                        'unid': row[2],
                        'color': row[9],
                        'manufacturer': manufacturer,
                        'operator': operator,
                        'mass': row[12],
                        'registration_mark': row[8].upper() if row[8] != "" else None,
                        'category': row[11].upper() if row[11] != "" else None,
                        'certification_number': int(row[1]) if row[1] != "" else None,
                        'validity': int(row[15]) if row[15] != "" else None,
                        'remarks': row[16] if row[16] != "" else None,
                        'popular_name': row[7] if row[7] != "" else None
                    }
                )
            except Exception as e:
                print("aircraft error", str(e))
        return True, None
