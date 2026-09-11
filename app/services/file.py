from uuid import uuid4
from fastapi import UploadFile
from pathlib import Path
from app.core.config import settings


async def save_upload_file(file: UploadFile):
    if file.content_type not in settings.allowed_types:
        raise ValueError("Unsupported file type")

    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    # | ذخیره فایل   

    extension = Path(file.filename).suffix
    filename = f"{uuid4()}{extension}" # ? اگر کاربر بفرسته: my_cat.png ---> 7f3a8d2e-1c44-4e2b-91d2-abc123.png
    
    # ! contents = await file.read() برای فایل بزرگ رم زیادی مصرف میشه
    # ? بهتره فایل رو تکه‌تکه بخونیم (chunks)
    
    file_path = upload_dir / filename

    # with open(file_path, "wb") as f:
    #     f.write(contents)

    total_size = 0
    try:
        with open(file_path, "wb") as f:

            while chunk := await file.read(settings.chunk_size): # @ خواندن یک تکه از فایل

                total_size += len(chunk)

                if total_size > settings.max_file_size:
                    raise ValueError("File too large")

                f.write(chunk)

    except ValueError:
        if file_path.exists():
            file_path.unlink() # @ فایل ناقص را از دیسک حذف می‌کند

        raise

    return {
        "filename": filename,
        "original_filename": file.filename,
        "content_type": file.content_type,
        "size": total_size,
        "status": "uploaded"
    }