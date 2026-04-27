import requests
import uuid
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

@deconstructible
class SupabaseStorage(Storage):
    def __init__(self, bucket=None):
        self.bucket = bucket or getattr(settings, 'SUPABASE_BUCKET', '')
        # URL'dan /rest/v1/ ni olib tashlash (agar bo'lsa)
        url = getattr(settings, 'SUPABASE_URL', '')
        self.base_url = url.replace('/rest/v1/', '').rstrip('/')
        self.key = getattr(settings, 'SUPABASE_KEY', '')


    def _open(self, name, mode='rb'):
        return None

    def _save(self, name, content):
        # Fayl nomini noyob (unique) qilish
        ext = name.split('.')[-1]
        file_name = f"{uuid.uuid4()}.{ext}"
        
        # Yuklash uchun URL
        upload_url = f"{self.base_url}/storage/v1/object/{self.bucket}/{file_name}"
        
        headers = {
            "Authorization": f"Bearer {self.key}",
            "apikey": self.key,
            "Content-Type": getattr(content, 'content_type', 'application/octet-stream')
        }

        # Faylni yuborish
        content.seek(0)
        response = requests.post(upload_url, headers=headers, data=content.read())

        if response.status_code == 200:
            return file_name
        else:
            print(f"Supabase upload error: {response.text}")
            return name

    def exists(self, name):
        return False

    def url(self, name):
        return f"{self.base_url}/storage/v1/object/public/{self.bucket}/{name}"

    def delete(self, name):
        """Supabase'dan faylni o'chirish"""
        url = f"{self.base_url}/storage/v1/object/{self.bucket}/{name}"
        headers = {
            "Authorization": f"Bearer {self.key}",
            "apikey": self.key,
        }
        response = requests.delete(url, headers=headers)
        if response.status_code != 200:
            print(f"Supabase delete error: {response.text}")



def supabase_upload(file_obj):
    if not file_obj:
        return None
    storage = SupabaseStorage()
    try:
        file_name = storage._save(file_obj.name, file_obj)
        return storage.url(file_name)
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return None

