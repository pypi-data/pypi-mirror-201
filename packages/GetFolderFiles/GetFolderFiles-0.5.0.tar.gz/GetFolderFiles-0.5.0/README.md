# GetFileListFromFolder

This is a python wrapper library for the get file list in a folder


How to install:

    pip install get-folder-file


How to use:

    from get_folder_file import GetFilesFromFolder

    lists = GetFilesFromFolder(path=r"C:\Users\sha-gregh\Desktop\edoc_Auto-Index", exts="pdf,jpg").file_list()
    print(lists)






