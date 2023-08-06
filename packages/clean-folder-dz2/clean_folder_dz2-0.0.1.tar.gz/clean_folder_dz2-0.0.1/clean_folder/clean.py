from pathlib import Path
import shutil
import sys
import clean_folder.file_parser as parser
from clean_folder.normalize import normalize


def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_document(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()),
                              str(folder_for_file.resolve()))
    except shutil.ReadError:
        print(f'Це не архів {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Помилка видалення папки {folder}')


def main_scan(folder: Path):
    parser.scan(folder)
    for file in parser.JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in parser.JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in parser.PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in parser.SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')

    for file in parser.MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in parser.OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in parser.WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')
    for file in parser.AMR_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR')

    for file in parser.MY_OTHER:
        handle_other(file, folder / 'MY_OTHER')
    for file in parser.ZIP_ARCHIVES:
        handle_archive(file, folder / 'zip_archives')
    for file in parser.GZ_ARCHIVES:
        handle_archive(file, folder / 'gz_archives')
    for file in parser.TAR_ARCHIVES:
        handle_archive(file, folder / 'tar_archives')

    for file in parser.MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in parser.MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')
    for file in parser.MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')
    for file in parser.AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')

    for file in parser.DOC_DOCUMENT:
        handle_document(file, folder / 'document' / 'DOC')
    for file in parser.DOCX_DOCUMENT:
        handle_document(file, folder / 'document' / 'DOCX')
    for file in parser.TXT_DOCUMENT:
        handle_document(file, folder / 'document' / 'TXT')
    for file in parser.PDF_DOCUMENT:
        handle_document(file, folder / 'document' / 'PDF')
    for file in parser.XLSX_DOCUMENT:
        handle_document(file, folder / 'document' / 'XLSX')
    for file in parser.PPTX_DOCUMENT:
        handle_document(file, folder / 'document' / 'PPTX')

    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


def main():
    try:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder {folder_for_scan.resolve()}')
        main_scan(folder_for_scan.resolve())
    except IndexError:
        print('Script need path to folder as parameter')


if __name__ == '__main__':
    main()