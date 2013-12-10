import os
from prescription.web import DoctorPrescribesApp


if __name__ == "__main__":
    config_file_path = os.path.join(os.path.dirname(__file__), "config/config.yml")
    application = DoctorPrescribesApp(config_file_path)
    application.start()
