import csv

from django.db import migrations, transaction


def import_csv(apps, file, model):
    Model = apps.get_model('dress', model)
    with open(file, 'r') as f:
        reader = csv.DictReader(f)

        with transaction.atomic():
            for row in reader:
                model = Model()
                for key in row.keys():
                    setattr(model, key, row[key])
                model.save()


def reverse_csv(apps, file, model):
    Model = apps.get_model('dress', model)
    with open(file, 'r') as f:
        reader = csv.DictReader(f)

        with transaction.atomic():
            for row in reader:
                model = Model.objects.all().filter(**dict(row))
                if model:
                    model[0].delete()