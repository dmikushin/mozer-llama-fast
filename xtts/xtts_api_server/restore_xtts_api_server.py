import os, time, shutil
import patch_xtts_api_server


def restore_files(file_paths_with_replacements):
    for file_path_with_replacement in file_paths_with_replacements:
        file_path = file_path_with_replacement[0]
        bkp_file_path = file_path + '.bkp'
        
        # Check if backup file exists
        if os.path.exists(bkp_file_path):
            # Restore and overwrite original file from backup
            shutil.move(bkp_file_path, file_path)
            print(file_path+" is restored.")
        else: print(bkp_file_path+" is not found, skipping.")
    
if __name__ == "__main__":
    
    
    restore_files(patch_xtts_api_server.return_patch_files())
    print ("\n\nSuccess. closing this window in 60 seconds.")
    time.sleep(60)