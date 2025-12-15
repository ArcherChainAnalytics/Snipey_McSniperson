# src/core/config.py

class Config:
    def __init__(self):
        self.env = "dev"
        self.storage_path = "storage"

CFG = Config()
