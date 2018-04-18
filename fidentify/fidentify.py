import cv2
import face_recognition
from datetime import datetime, timedelta
import os, errno
import argparse
import json
import re
import csv

args_list = ["known_images_path","download_path","videos_path"]
white_listed_image_formats = ['jpg','jpeg','png','gif','bmp']
white_listed_video_formats = ['mp4']

def user_input():
    config = argparse.ArgumentParser()
    config.add_argument('-cf', '--config_file', help='config file name', default='', type=str, required=False)
    config.add_argument('-kip', '--known_images_path', help='Known images path', type=str, required=False)
    config.add_argument('-vp', '--videos_path', help='Video Path', type=str, required=False)
    config.add_argument('-dp', '--download_path', help='Downloads path', type=str, required=False)
    config.add_argument('-v','--version', action='version', version="%(prog)s " + open('VERSION','r').read())
    config_file_check = config.parse_known_args()
    object_check = vars(config_file_check[0])

    if object_check['config_file'] != '':
        records = []
        json_file = json.load(open(config_file_check[0].config_file))
        arguments = {}
        for i in args_list:
            arguments[i] = None
        for key in json_file['Arguments']:
            arguments[key] = json_file['Arguments'][key]
            records.append(arguments)
        records_count = len(records)
    else:
        # Taking command line arguments from users
        args = config.parse_args()
        arguments = vars(args)
        records = []
        records.append(arguments)
    return records


class fidentity:
    def __init__(self):
        pass

    def save_frame(self, frame, face_locations, face_names, download_path, frame_no):
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        # Save the resulting frame
        downloads_path = download_path +'/' + 'frame_' + str(frame_no) + '.jpg'
        cv2.imwrite(downloads_path, frame )

    def identity(self, known_images_path, videos_path, download_path):
        # Load a sample pictures and learn how to recognize it.
        known_face_names = []
        known_face_encodings = []

        for image in os.listdir(known_images_path):
            # Load the picture
            loaded_image = face_recognition.load_image_file("{}/{}".format(known_images_path,image))
            # Get facial encodings
            face_encoding = face_recognition.face_encodings(loaded_image)[0]
            known_face_names.append(image.split('.')[0])
            known_face_encodings.append(face_encoding)

        for video in os.listdir(videos_path):
            # Get a reference to webcam #0 (the default one)
            current_frame = 0
            video_capture = cv2.VideoCapture(videos_path + '/'+ video)
            fps = video_capture.get(cv2.CAP_PROP_FPS)
            # Initialize some variables
            face_locations = []
            face_encodings = []
            face_names = []
            process_this_frame = True
            while True:
                # Grab a single frame of video
                _ret, frame = video_capture.read()
                # frame doesn't exist then skip the loop.
                if (type(frame) == type(None)):
                    break
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]
                match_found = False
                if process_this_frame:
                    # Find all the faces and face encodings in the current frame of video
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                    # Initialize a empty array
                    face_names = []
                    for face_encoding in face_encodings:
                        # See if the face is a match for the known face(s)
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        name = "Unknown"
                        # If a match was found in known_face_encodings, just use the first one.
                        if True in matches:
                            match_found = True
                            first_match_index = matches.index(True)
                            name = known_face_names[first_match_index]
                        face_names.append(name)
                # process_this_frame = not process_this_frame
                if match_found:
                    self.save_frame(frame, face_locations, face_names, download_path, current_frame)
                current_frame += 1
            # Release handle to the webcam
            video_capture.release()
            # Destroy all open windows
            cv2.destroyAllWindows()

def check_path(path,type_of_path):
    return_val = ''
    if not os.path.exists(path):
        print("{} directory doesn't exist".format(path))
        return return_val

    files = os.listdir(path)
    if not len(files):
        print("{} directory doesn't contain any images".format(path))
    else:
        if type_of_path == 1:
            white_listed = white_listed_video_formats
        else:
            white_listed = white_listed_image_formats
        if not len(re.findall('|'.join(white_listed),''.join(files))):
            print("Please use one of the file extensions {}".format(','.join(white_listed)))
        else:
            return_val = path
    return return_val

def create_download_directory_if_not_exists(download_path):
    if not os.path.exists(download_path):
        print("Creating {} path as the directory doesn't exist".format(download_path))
        try:
            os.makedirs(download_path)
        except OSError as e:
            print("Error occured while creating directory {}".format(download_path))
            if e.errno != errno.EEXIST:
                raise

def main():
    paths = {
    'images_path': 0,
    'videos_path': 1
    }
    records = user_input()
    for arguments in records:
        if not arguments['known_images_path']:
            arguments['known_images_path'] = 'images'
        kip_return_val = check_path(arguments['known_images_path'], paths['images_path'])

        if not arguments['download_path']:
            arguments['download_path'] = 'downloads'
        create_download_directory_if_not_exists(arguments['download_path'])

        if not arguments['videos_path']:
            arguments['videos_path'] = 'videos'
        vp_return_val = check_path(arguments['videos_path'], paths['videos_path'])

        if not (kip_return_val or vp_return_val):
            break
        else:
            arguments['known_images_path'] = kip_return_val
            arguments['videos_path'] = vp_return_val

        fidentity_obj = fidentity()
        fidentity_obj.identity(arguments['known_images_path'], arguments['videos_path'], arguments['download_path'])
        return 0


if __name__ == "__main__":
    main()