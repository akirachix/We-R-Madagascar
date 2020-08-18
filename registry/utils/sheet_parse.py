import pandas as pd
from django.db import transaction
import datetime as dt
from django.utils import timezone
from django.db.models import Q

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
            error = ''
            if row[2] != '':
                try:
                    getAircraft = Aircraft.objects.get(unid=row[2])
                except Aircraft.DoesNotExist:
                    getAircraft = ''
            else:
                getAircraft = ''
            try:
                if row[4] == '' and getAircraft == '':
                    error = "Address empty for row {}".format(row)
                else:
                    getAddress = Address.objects.filter(
                        address_line_1__contains=row[4])
                    if getAddress:
                        address = getAddress
                    else:
                        address = Address.objects.create(
                            address_line_1=row[4],
                            address_line_2=row[4],
                            address_line_3=row[4])
            except Exception as e:
                error = "Error while creating Address [{}] in row {}".format(
                    str(e), row)
            try:
                if row[7] == '' and getAircraft == '':
                    error = "Manufacturer empty for row {}".format(row)
                else:
                    getManufacturer = Manufacturer.objects.filter(full_name=row[7])
                    if getManufacturer:
                        manufacturer = getManufacturer[0]
                    else:
                        manufacturer = Manufacturer.objects.create(
                            full_name=row[7])
            except Exception as e:
                error = "Error while creating Manufacturer [{}] in row {}".format(
                    str(e), row)
            try:
                if row[3] == '' and row[5] == '' and getAircraft == '':
                    error = "Manufacturer empty for row {}".format(row)
                else:
                    getOperator = Operator.objects.filter(
                        Q(company_name=row[3]) | Q(phone_number=row[5]))
                    if getOperator:
                        operator = getOperator[0]
                    else:
                        Operator.objects.create(company_name=row[3],
                                                address=address,
                                                phone_number=row[5],
                                                email=row[6])
            except Exception as e:
                error = "Error while creating Operator [{}] in row {}".format(
                    str(e), row)
            if row[2] != '':
                try:
                    try:
                        getAircraft = Aircraft.objects.get(unid=row[2])
                        aircraft = getAircraft
                        aircraft = Aircraft.objects.filter(unid=row[2]).update(
                            unid=row[2],
                            color=row[9],
                            manufacturer=manufacturer,
                            operator=operator,
                            mass=row[12],
                            registration_mark=row[8].upper(
                            ) if row[8] != "" else None,
                            category=row[11].upper() if row[11] != "" else None,
                            certification_number=int(
                                row[1]) if row[1] != "" else None,
                            validity=int(row[15]) if row[15] != "" else None,
                            remarks=row[16] if row[16] != "" else None,
                        popular_name=row[7] if row[7] != "" else None)
                    except Aircraft.DoesNotExist:
                        aircraft = Aircraft.objects.create(
                            unid=row[2],
                            color=row[9],
                            manufacturer=manufacturer,
                            operator=operator,
                            mass=row[12],
                            registration_mark=row[8].upper(
                            ) if row[8] != "" else None,
                            category=row[11].upper() if row[11] != "" else None,
                            certification_number=int(
                                row[1]) if row[1] != "" else None,
                            validity=int(row[15]) if row[15] != "" else None,
                            remarks=row[16] if row[16] != "" else None,
                        popular_name=row[7] if row[7] != "" else None)
                except Exception as e:
                    error = "Error while creating Aircraft [{}] in row {}".format(
                        str(e), row)
            else:
                error = "UNID emppty for row {}".format(row)
            if error == '':
                return 200, None
            else:
                return 400, error
