# your_app/management/commands/create_users_from_excel.py
import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create regular users from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        excel_file_path = options['file_path']

        # Convert to absolute path if it's a relative path
        if not os.path.isabs(excel_file_path):
            excel_file_path = os.path.join(os.path.dirname(__file__), excel_file_path)

        # Read Excel file into a DataFrame
        try:
            df = pd.read_excel(excel_file_path)
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.ERROR('Empty Excel file'))
            return

        # Create users based on the Excel data
        for index, row in df.iterrows():
            username = row['Username']
            parol = str(row['password'])  # Convert to string
            tabel = str(row['ТableNumber'])

            # Check if the user already exists
            if not get_user_model().objects.filter(username=username).exists():
                get_user_model().objects.create_user(
                    username=username,
                    password=parol,
                    table_number=tabel
                )

                self.stdout.write(self.style.SUCCESS(f'Successfully created user: {username}'))
