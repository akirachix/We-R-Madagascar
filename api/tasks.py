from celery import shared_task
from registry.models import CeleryTasks, SheetRegister
from registry.utils.preprocessor import Preprocessor


@shared_task
def parse_sheet(task_id, sheet_id):
    course_sheet = SheetRegister.objects.get(pk=sheet_id)
    try:
        excel_processor = Preprocessor(
            course_sheet.upload_sheet,
            course_sheet.created_by, course_sheet.name)
        excel_processor.parse()
        CeleryTasks.objects.filter(pk=task_id).update(status=2)
    except Exception as e:
        print("error", str(e))
        CeleryTasks.objects.filter(pk=task_id).update(status=3)
