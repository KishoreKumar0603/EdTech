import os
import datetime
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
supabase_url = os.getenv('SUPABASE_STORAGE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY is missing")

supabase = create_client(supabase_url, supabase_key)

def get_profile_path(file_name):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    sanitized_name = file_name.replace(" ", "_")  # Sanitize the file name
    return f"{now_time}_{sanitized_name}"

def delete_old_file_from_supabase(bucket_name, old_file_url):
    try:
        # Extract the file path from the full URL
        file_path = old_file_url.split(f"{bucket_name}/")[-1]
        response = supabase.storage.from_(bucket_name).remove([file_path])
        print(f"Old profile picture deletion response: {response}")
    except Exception as e:
        print(f"Error during old file deletion: {e}")

def upload_to_supabase(file, bucket_name, old_file_url=None):
    file_path = get_profile_path(file.name)
    file_content = file.read()

    try:
        response = supabase.storage.from_(bucket_name).upload(file_path, file_content)
        print(f"Supabase response: {response}")
        if hasattr(response, 'path') and response.path:
            if old_file_url:
                print(f"Attempting to delete old file: {old_file_url}")
                delete_old_file_from_supabase(bucket_name, old_file_url)

            full_url = f"{supabase_url}/storage/v1/object/public/{bucket_name}/{response.path}"
            print(f"File uploaded successfully at URL: {full_url}")
            return full_url
        else:
            raise Exception("Unexpected response structure from Supabase.")

    except Exception as e:
        print(f"Error during upload: {e}")
        raise

def upload_profile_image(file, student, bucket_name="userProfilePic"):
    old_file_url = student.profile_picture if student.profile_picture else None
    file_url = upload_to_supabase(file, bucket_name, old_file_url)
    student.profile_picture = file_url
    student.save()
    return file_url
