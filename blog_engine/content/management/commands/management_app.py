from pathlib import Path

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QInputDialog, QLineEdit
from django.core.management.base import AppCommand
from django.conf import settings
from django.utils import timezone


class Command(AppCommand):
    help = 'Creates read only default permission groups for users'

    def handle_app_config(self, app_config, **options):
        app = QApplication([])
        window = QWidget()
        layout = QVBoxLayout()
        backup_button = QPushButton('Backup')
        layout.addWidget(backup_button)

        def get_login(database_name):
            username, ok = QInputDialog.getText(None, "Attention", f"Enter user name for {database_name}",
                                                QLineEdit.Normal)
            if ok and username:
                password, ok = QInputDialog.getText(None, "Attention", f"Enter password for {username}",
                                                    QLineEdit.Password)
                if ok and password:
                    return username, password

        def backup():
            backup_path = Path('backups')
            if not backup_path.exists():
                backup_path.mkdir()
            import subprocess
            database_name = settings.DATABASES['default']['NAME']
            self.stdout.write(self.style.WARNING(f'doing backup. {database_name}'))
            login = get_login(database_name)
            if login:
                username, password = login
                data = subprocess.check_output(f"mysqldump -u {username} --password={password} --databases "
                                               f"{database_name}", shell=True)
                file = backup_path / (str(timezone.now().strftime('%Y-%m-%dT%H.%M.%S')) + ".sql")
                file.write_bytes(data)

        backup_button.clicked.connect(backup)
        restore_button = QPushButton('Restore')

        def restore():
            backup_path = Path("backups")
            item, ok = QInputDialog.getItem(None, "Attention", "Choose backup file",
                                            map(str, filter(lambda p: p.name.endswith(".sql"), backup_path.iterdir())))
            if ok and item:
                self.stdout.write(str(item))
                login = get_login("a privileged user")
                if login:
                    username, password = login
                    import subprocess
                    backup_file = Path(item)
                    subprocess.run(f"type",  # -u {username} --password={password}",
                                   input=backup_file.read_bytes(), shell=True)

        restore_button.clicked.connect(restore)
        layout.addWidget(restore_button)
        window.setLayout(layout)
        window.show()
        app.exec_()
