from datetime import datetime, timedelta
import io
import cv2
import pytz
import copy
import math
import base64
import numpy as np
from PIL import Image

def get_now_with_format(date_format):
    """
    Param : datetime format (ex. '%Y%m%d%H%M%S%f')
    Return : sysdate (now))
    """
    try:
        date_now = datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime(date_format) #get date
        return date_now
    except Exception as e:
        print("[ERROR] get_now_with_format : {}".format(e))
        return None

def cal_time_div(timeA, timeB):
    """
    Param : timeA : YYYYMMDDhh24missms
    """
    try:
        time1 = datetime.strptime(timeA,"%Y%m%d%H%M%S%f")
        time2 = datetime.strptime(timeB,"%Y%m%d%H%M%S%f")

        normal = time1-time2
        days = normal.days * 60 * 60 * 24
        seconds = normal.seconds
        microseconds = normal.microseconds / 1000000
        total = days + seconds + microseconds

        return total
    except Exception as e:
        print("[ERROR] cal_time_div : {}".format(e))
        return None

def get_time_minus_sec(timeA, addSec):
    try:
        time1 = datetime.strptime(timeA,"%Y%m%d%H%M%S%f")
        cal_time = time1 - timedelta(seconds=addSec)
        rtn_date = cal_time.strftime("%Y%m%d%H%M%S%f")
        return rtn_date
    except Exception as e:
        print("[ERROR] get_time_minus_sec : {}".format(e))
        return None

def get_time_add_sec(timeA, addSec):
    try:
        time1 = datetime.strptime(timeA,"%Y%m%d%H%M%S%f")
        cal_time = time1 + timedelta(seconds=addSec)
        rtn_date = cal_time.strftime("%Y%m%d%H%M%S%f")
        return rtn_date
    except Exception as e:
        print("[ERROR] get_time_minus_sec : {}".format(e))
        return None

def convert_timestamp_to_display(timestamp, date_format):
    try:
        time_delta = datetime.strptime(timestamp,"%Y%m%d%H%M%S%f")
        return time_delta.strftime(date_format)
    except Exception as e:
        print('convert_timestamp_to_display : {}'.format(e))
        return None

def cal_dict_a_minus_b(dictA, dictB):
    """
    Param : dictionary A, dictionary B
    Return : dictionary A - dictionary B
    """
    try:
        tmp_dictA = copy.deepcopy(dictA)
        tmp_dictB = copy.deepcopy(dictB)

        if not tmp_dictA:
            rtn_dict = {}
        else:
            rtn_dict = copy.deepcopy(dictA)
            for key, val in tmp_dictA.items():
                if key not in tmp_dictB:
                    del rtn_dict[key]

        return rtn_dict
    except Exception as e:
        print("[ERROR] cal_dict_a_minus_b : {}".format(e))
        return None

def cal_new_one_dict_a_minus_b(dictA, dictB):
    """
    Param : dictionary A, dictionary B
    Return : dictionary A - dictionary B
    """
    try:
        tmp_dictA = copy.deepcopy(dictA)
        tmp_dictB = copy.deepcopy(dictB)

        if not tmp_dictA:
            rtn_dict = {}
        else:
            rtn_dict = copy.deepcopy(dictA)
            for key, val in tmp_dictA.items():
                if key in tmp_dictB:
                    del rtn_dict[key]

        return rtn_dict
    except Exception as e:
        print("[ERROR] cal_dict_a_minus_b : {}".format(e))
        return None

def getBoxPos_calEnd(box, keypoint=None):
    try:
        startX = int(box[0])
        startY = int(box[1])
        width = int(box[2])
        height = int(box[3])
        endX = startX+width
        endY = startY+height

        if keypoint is not None:
            (left_hand_x, left_hand_y, right_hand_x, right_hand_y) = keypoint

            if left_hand_x is not None and left_hand_y is not None and right_hand_x is not None and right_hand_y is not None:
                # 가장 낮은 좌표
                hand_y = left_hand_y
                if left_hand_y < right_hand_y:
                    hand_y = right_hand_y

                if endY < hand_y:
                    endY = int(hand_y)

                # 가장 왼쪽(box기준)
                hand_start_x = right_hand_x
                if hand_start_x > left_hand_x:
                    hand_start_x = left_hand_x
                if startX > hand_start_x:
                    startX = int(hand_start_x)

                # 가장 오른쪽(box 기준)
                hand_end_x = left_hand_x
                if hand_end_x < right_hand_x:
                    hand_end_x = right_hand_x
                if endX < hand_end_x:
                    endX = int(hand_end_x)

                height = int(endY - startY)
                width = int(endX - startX)

        return (startX, startY, width, height, endX, endY)

    except Exception as e:
        print("[ERROR] getBoxPos_calEnd : {}".format(e))
        return None

def getBoxPos_calMax(boxs):
    try:
        max_startX = None
        max_startY = None
        max_width = None
        max_height = None
        max_endX = None
        max_endY = None
        max_size = 0

        # get bounding boxs
        for box in boxs:
            startX = int(box[0])
            startY = int(box[1])
            width = int(box[2])
            height = int(box[3])
            endX = startX+width
            endY = startY+height

            size = width * height

            if size > max_size:
                max_startX = startX
                max_startY = startY
                max_width = width
                max_height = height
                max_endX = endX
                max_endY = endY
                max_size = size

        return (max_startX, max_startY, max_width, max_height, max_endX, max_endY, max_size)
    except Exception as e:
        print("[ERROR] getBoxPos_calMax : {}".format(e))
        return None

def getBoxPosByRate(pos, frame_rate, max_w, max_h):
    try:
        (startX, startY, width, height, endX, endY) = pos

        bboxX = int(startX*frame_rate)
        bboxY = int(startY*frame_rate)
        bboxEX = int(endX*frame_rate)
        bboxEY = int(endY*frame_rate)

        if bboxX < 0:
            bboxX = 0
        if bboxY < 0:
            bboxY = 0
        if bboxEX > max_w:
            bboxEX = max_w
        if bboxEY > max_h:
            bboxEY = max_h

        bboxW = bboxEX - bboxX
        bboxH = bboxEY - bboxY

        return (bboxX, bboxY, bboxW, bboxH, bboxEX, bboxEY)
    except Exception as e:
        print("[ERROR] getBoxPosByRate : {}".format(e))
        return None

def adjustBoxOversizeTlbr(input_image, box_info, rtn_type='tuple'):
    if rtn_type == 'tuple':
        rtn_box_info = ()
    else:
        rtn_box_info = []
    try:
        startX = int(box_info[0])
        startY = int(box_info[1])
        endX = int(box_info[4])
        endY = int(box_info[5])

        if startX < 0:
            startX = 0
        if startY < 0:
            startY = 0
        if endX > input_image.shape[1]:
            endX = input_image.shape[1]
        if endY > input_image.shape[0]:
            endY = input_image.shape[0]
        
        if rtn_type == 'tuple':
            rtn_box_info = (startX, startY, endX, endY)
        else:
            rtn_box_info = [startX, startY, endX, endY]
    except Exception as e:
        print('[ERROR] adjustBoxOversizeTlbr : {}'.format(e))
    return rtn_box_info


def getCenterPosByRage(center, frame_rate):
    try:
        (startX, startY) = center

        centerX = int(startX*frame_rate)
        centerY = int(startY*frame_rate)

        return (centerX, centerY)
    except Exception as e:
        print("[ERROR] getCenterPosByRage : {}".format(e))
        return None

def getCenterPosFromBox(box):
    try:
        (startX, startY, width, height) = box

        centerX = startX + int(width/2)
        centerY = startY + int(height/2)

        return (centerX, centerY)
    except Exception as e:
        print("[ERROR] getCenterPosFromBox : {}".format(e))
        return None

def getRadius(a_b):
    try:
        diameter = min(a_b)
        radius = int(diameter / 2)

        return radius
    except Exception as e:
        print("[ERROR] getRadius : {}".format(e))
        return None

def get_base_by_cos(base, hypot, add_hypot):
    try:
        if add_hypot > 0:
            added_hypot = hypot + add_hypot
        else:
            added_hypot = hypot

        cosA = base / hypot

        rtn_base = added_hypot * cosA
        return rtn_base
    except Exception as e:
        print("[ERROR] get_hypot : {}".format(e))
        return None

def get_height_by_sin(height, hypot, add_hypot):
    try:
        if add_hypot > 0:
            added_hypot = hypot + add_hypot
        else:
            added_hypot = hypot

        sinA = height / hypot

        rtn_height = added_hypot * sinA

        return rtn_height
    except Exception as e:
        print("[ERROR] get_hypot : {}".format(e))
        return None


def get_hypot(base, height):
    try:
        rtn_hypot = math.sqrt((base ** 2) + (height ** 2))
        return rtn_hypot
    except Exception as e:
        print("[ERROR] get_hypot : {}".format(e))
        return None

def get_distance(posA, posB):
    try:
        (AX, AY) = posA
        (BX, BY) = posB

        base = AX-BX
        if base < 0:
            base = base * -1

        height = AY-BY
        if height < 0:
            height = height * -1

        distance = math.sqrt((base ** 2) + (height ** 2))

        return distance
    except Exception as e:
        print("[ERROR] get_distance : {}".format(e))
        return None

def getCenterPosByShoulder(soulders):
    try:
        (l_s_x, l_s_y, r_s_x, r_s_y) = soulders

        if l_s_x > r_s_x:
            w = l_s_x - r_s_x
            c_x = r_s_x + (w/2)
        else:
            w = r_s_x - l_s_x
            c_x = l_s_x + (w/2)

        if l_s_y > r_s_y:
            h = l_s_y - r_s_y
            c_y = r_s_y + (h/2)
        else:
            h = r_s_y - l_s_y
            c_y = l_s_y + (h/2)

        return (c_x, c_y)

    except Exception as e:
        print("[ERROR] getCenterPosByShoulder : {}".format(e))
        return None

def bbox_iou(boxA, boxB):
    try:
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        interArea = max(0, xB- xA + 1) * max(0, yB - yA + 1)

        boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

        iou = interArea / float(boxAArea + boxBArea - interArea)

        return iou

    except Exception as e:
        print('[ERROR] bbox_iou : {}'.format(e))
        return 0.0

def convert_bytes_to_nparray(byte_str):
    try:
        image = Image.open(io.BytesIO(byte_str))            
        return np.array(image)
    except Exception as e:
        print("b64_convert_to_img : {}".format(e))
        return None

def b64_convert_to_img(b64_str):
    try:
        byte_str = b64_str.encode("UTF-8") # json 파싱한 str을 bytes type으로 변환
        decode_str = base64.decodestring(byte_str) # base64를 디코딩
        nparr = np.fromstring(decode_str, np.uint8) # 이건 다시 numpy array로 변환
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        return img
    except Exception as e:
        print("b64_convert_to_img : {}".format(e))
        return None

def download_and_view_image(s3_obj, bucket_name, file_name):
    try:
        obj = s3_obj.Object(bucket_name, file_name)
        body = obj.get()['Body'].read()
        rtn_img = convert_bytes_to_nparray(body)
        rtn_img = cv2.cvtColor(rtn_img, cv2.COLOR_RGB2BGR)
        return rtn_img
    except Exception as e:
        print("[ERROR] download_and_view_image: bucket={}, key={}".format(bucket_name, file_name))
        print("[ERROR] download_and_view_image:{}".format(e))
        return None
