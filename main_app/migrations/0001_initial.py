

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='doctor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_patient', models.BooleanField(default=False)),
                ('is_doctor', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('img', models.ImageField(blank=True, upload_to='pics')),
                ('address', models.CharField(max_length=100)),
                ('mobile_no', models.CharField(max_length=15)),
                ('gender', models.CharField(max_length=10)),
                ('registration_no', models.CharField(max_length=20)),
                ('year_of_registration', models.DateField()),
                ('qualification', models.CharField(max_length=20)),
                ('State_Medical_Council', models.CharField(max_length=30)),
                ('specialization', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='patient',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_patient', models.BooleanField(default=True)),
                ('is_doctor', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('img', models.ImageField(blank=True, upload_to='pics')),
                ('address', models.CharField(max_length=100)),
                ('mobile_no', models.CharField(max_length=15)),
                ('gender', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='diseaseinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diseasename', models.CharField(max_length=200)),
                ('no_of_symp', models.IntegerField()),
                ('symptomsname', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None)),
                ('confidence', models.DecimalField(decimal_places=2, max_digits=5)),
                ('consultdoctor', models.CharField(max_length=200)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.patient')),
            ],
        ),
        migrations.CreateModel(
            name='consultation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consultation_date', models.DateField()),
                ('messages', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, size=None)),
                ('status', models.CharField(max_length=20)),
                ('diseaseinfo', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.diseaseinfo')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.patient')),
            ],
        ),
    ]
