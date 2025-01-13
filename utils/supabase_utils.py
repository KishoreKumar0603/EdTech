# utils/supabase_utils.py
import os
import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
supabase_url = os.getenv('SUPABASE_STORAGE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY is missing")

supabase = create_client(supabase_url, supabase_key)

def get_profile_path(file_name):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    sanitized_name = file_name.replace(" ", "_")  # Remove spaces
    return f"{now_time}_{sanitized_name}"

# def upload_to_supabase(file, bucket_name):
#     file_path = get_profile_path(file.name)
#     file_content = file.read()

#     try:
#         # Upload the file to Supabase storage
#         response = supabase.storage.from_(bucket_name).upload(file_path, file_content)

#         # Log the response structure for clarity
#         print(f"Supabase response: {response}")
#         print(f"Response attributes: {dir(response)}")

#         # Check if the 'path' attribute exists in the response, indicating success
#         if response.path:
#             # Construct the full URL to the uploaded image
#             full_url = f"{supabase_url}/storage/v1/object/public/userProfilePic/{response.path}"
#             print(f"File uploaded successfully at URL: {full_url}")
#             return full_url
#         else:
#             raise Exception("Unexpected response structure from Supabase.")

#     except Exception as e:
#         print(f"Error during upload: {e}")
#         raise

# def upload_profile_image(file):
#     file_path = get_profile_path(file.name)
#     file_url = upload_to_supabase(file, bucket_name="userProfilePic") 
#     return file_url


def upload_to_supabase(file, bucket_name, old_file_path=None):
    file_path = get_profile_path(file.name)
    file_content = file.read()

    try:
        # Upload the new file to Supabase storage
        response = supabase.storage.from_(bucket_name).upload(file_path, file_content)

        # Log the response structure for clarity
        print(f"Supabase response: {response}")
        print(f"Response attributes: {dir(response)}")
        if response.path:
            if old_file_path:
                print(f"Attempting to delete old file: {old_file_path}")
                delete_response = supabase.storage.from_(bucket_name).remove([old_file_path])
                print(f"Old profile picture deletion response: {delete_response}")

            full_url = f"{supabase_url}/storage/v1/object/public/{bucket_name}/{response.path}"
            print(f"File uploaded successfully at URL: {full_url}")
            return full_url
        else:
            raise Exception("Unexpected response structure from Supabase.")

    except Exception as e:
        print(f"Error during upload: {e}")
        raise

def upload_profile_image(file, student, bucket_name="userProfilePic"):
    old_file_path = student.profile_picture if student.profile_picture else None
    file_url = upload_to_supabase(file, bucket_name, old_file_path)
    student.profile_picture = file_url
    student.save()
    
    return file_url


