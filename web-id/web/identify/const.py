import os

from enum import IntEnum

from web import settings

BC_SERVER = 'http://192.168.60.82:9090/'
# BC_SERVER = '192.168.60.238:8080/'
BC_API_ADD_USER = 'add_user_by_id/'
BC_API_DEL_USER = 'del_user_by_id/'
BC_API_CALCULATE_SALARY_USER = 'calculate_salary_users/'
BC_API_GET_SALARY_IN_DAY = 'get_salary_in_day'
BC_API_GET_SALARY_IN_PERIOD = 'get_salary_in_period'

TMP_FOLDER = os.path.join(settings.BASE_DIR, 'image/')
EIGENFACES_FOLDER = os.path.join(settings.BASE_DIR, 'pas/eigenfaces/')
FACE_TRAIN_FOLDER = os.path.join(settings.BASE_DIR, 'identify/member_images/')
FACE_CASCADE_PATH = os.path.join(settings.BASE_DIR, 'pas/haarcascade_frontalface_default.xml')
PAS_FOLDER = os.path.join(settings.BASE_DIR, 'identify/')
BASE_DIR = settings.BASE_DIR


VIDEO_PATH = os.path.join(settings.BASE_DIR, 'video/')

TRAIN_FACES_FOLDER_NAME = 'train_faces/'
TEST_FACES_FOLDER_NAME = 'test_faces/'

NUMBER_COMPONENT = 200

MQTT_AUTH_TOPIC = "pas/mqtt/icse/auth"
MQTT_LATEST_USER_SCAN = 'pas/mqtt/server/latest_scan'
MQTT_MEMBER_DOES_NOT_EXIST="pas/mqtt/member/does_not_exist"


class MemberType(IntEnum):
    student = 1
    teacher = 2
