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

    Manufacturer.objects.all().delete()
    Operator.objects.all().delete()
    Aircraft.objects.all().delete()

    with transaction.atomic():
        for row in data:
            manufacturer, _ = Manufacturer.objects.get_or_create(
                full_name=row[7]
            )
            try:
                address, _ = Address.objects.get_or_create(
                    address_line_1=row[4],
                    address_line_2=row[4],
                    address_line_3=row[4],
                )
            except Exception as e:
                print("okoko error", str(e))
            try:
                operator, _ = Operator.objects.get_or_create(
                    company_name=row[3], address=address,
                    phone_number=row[5], email=row[6]
                )
            except Exception as e:
                print("operatoroperatoroperator error", str(e))
            # print("operator", operator)
            try:
                aircraft = Aircraft(
                    color=row[9],
                    manufacturer=manufacturer,
                    operator=operator,
                    unid=row[2], mass=row[12]
                )
                aircraft.save()
            except Exception as e:
                print("aircraft error", str(e))
            # print("aircraft", aircraft)
        return True, None
