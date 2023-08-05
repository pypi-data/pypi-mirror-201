from enum import Enum

from .code_mappings import STATE_CODE_TO_STATUS, ERROR_CODE_TO_TEXT, FAN_SPEED_CODES, MOP_MODE_CODES, \
    MOP_INTENSITY_CODES, DOCK_ERROR_TO_TEXT, DOCK_TYPE_MAP, RoborockDockType, RoborockDockDustCollectionType, \
    DUST_COLLECTION_MAP, WASH_MODE_MAP, RoborockDockWashingModeType


class UserDataRRiotReferenceField(str, Enum):
    REGION = "r"
    API = "a"
    MQTT = "m"
    L_UNKNOWN = "l"


class UserDataRRiotField(str, Enum):
    USER = "u"
    PASSWORD = "s"
    H_UNKNOWN = "h"
    ENDPOINT = "k"
    REFERENCE = "r"


class UserDataField(str, Enum):
    UID = "uid"
    TOKEN_TYPE = "tokentype"
    TOKEN = "token"
    RR_UID = "rruid"
    REGION = "region"
    COUNTRY_CODE = "countrycode"
    COUNTRY = "country"
    NICKNAME = "nickname"
    RRIOT = "rriot"
    TUYA_DEVICE_STATE = "tuyaDeviceState"
    AVATAR_URL = "avatarurl"


class HomeDataProductSchemaField(str, Enum):
    ID = "id"
    NAME = "name"
    CODE = "code"
    MODE = "mode"
    TYPE = "type"
    PROPERTY = "property"
    DESC = "desc"


class HomeDataProductField(str, Enum):
    ID = "id"
    NAME = "name"
    CODE = "code"
    MODEL = "model"
    ICONURL = "iconUrl"
    ATTRIBUTE = "attribute"
    CAPABILITY = "capability"
    CATEGORY = "category"
    SCHEMA = "schema"


class HomeDataDeviceStatusField(str, Enum):
    ID = "id"
    NAME = "name"
    CODE = "code"
    MODEL = "model"
    ICON_URL = "iconUrl"
    ATTRIBUTE = "attribute"
    CAPABILITY = "capability"
    CATEGORY = "category"
    SCHEMA = "schema"


class HomeDataDeviceField(str, Enum):
    DUID = "duid"
    NAME = "name"
    ATTRIBUTE = "attribute"
    ACTIVETIME = "activeTime"
    LOCAL_KEY = "localKey"
    RUNTIME_ENV = "runtimeEnv"
    TIME_ZONE_ID = "timeZoneId"
    ICON_URL = "iconUrl"
    PRODUCT_ID = "productId"
    LON = "lon"
    LAT = "lat"
    SHARE = "share"
    SHARE_TIME = "shareTime"
    ONLINE = "online"
    FV = "fv"
    PV = "pv"
    ROOM_ID = "roomId"
    TUYA_UUID = "tuyaUuid"
    TUYA_MIGRATED = "tuyaMigrated"
    EXTRA = "extra"
    SN = "sn"
    FEATURE_SET = "featureSet"
    NEW_FEATURE_SET = "newFeatureSet"
    DEVICE_STATUS = "deviceStatus"
    SILENT_OTA_SWITCH = "silentOtaSwitch"


class HomeDataRoomField(str, Enum):
    ID = "id"
    NAME = "name"


class HomeDataField(str, Enum):
    ID = "id"
    NAME = "name"
    LON = "lon"
    LAT = "lat"
    GEO_NAME = "geoName"
    PRODUCTS = "products"
    DEVICES = "devices"
    RECEIVED_DEVICES = "receivedDevices"
    ROOMS = "rooms"


class StatusField(str, Enum):
    MSG_VER = "msg_ver"
    MSG_SEQ = "msg_seq"
    STATE = "state"
    BATTERY = "battery"
    CLEAN_TIME = "clean_time"
    CLEAN_AREA = "clean_area"
    ERROR_CODE = "error_code"
    MAP_PRESENT = "map_present"
    IN_CLEANING = "in_cleaning"
    IN_RETURNING = "in_returning"
    IN_FRESH_STATE = "in_fresh_state"
    LAB_STATUS = "lab_status"
    WATER_BOX_STATUS = "water_box_status"
    BACK_TYPE = "back_type"
    WASH_PHASE = "wash_phase"
    WASH_READY = "wash_ready"
    FAN_POWER = "fan_power"
    DND_ENABLED = "dnd_enabled"
    MAP_STATUS = "map_status"
    IS_LOCATING = "is_locating"
    LOCK_STATUS = "lock_status"
    WATER_BOX_MODE = "water_box_mode"
    WATER_BOX_CARRIAGE_STATUS = "water_box_carriage_status"
    MOP_FORBIDDEN_ENABLE = "mop_forbidden_enable"
    CAMERA_STATUS = "camera_status"
    IS_EXPLORING = "is_exploring"
    HOME_SEC_STATUS = "home_sec_status"
    HOME_SEC_ENABLE_PASSWORD = "home_sec_enable_password"
    ADBUMPER_STATUS = "adbumper_status"
    WATER_SHORTAGE_STATUS = "water_shortage_status"
    DOCK_TYPE = "dock_type"
    DUST_COLLECTION_STATUS = "dust_collection_status"
    AUTO_DUST_COLLECTION = "auto_dust_collection"
    AVOID_COUNT = "avoid_count"
    MOP_MODE = "mop_mode"
    DEBUG_MODE = "debug_mode"
    COLLISION_AVOID_STATUS = "collision_avoid_status"
    SWITCH_MAP_MODE = "switch_map_mode"
    DOCK_ERROR_STATUS = "dock_error_status"
    CHARGE_STATUS = "charge_status"
    UNSAVE_MAP_REASON = "unsave_map_reason"
    UNSAVE_MAP_FLAG = "unsave_map_flag"


class DNDTimerField(str, Enum):
    START_HOUR = "start_hour"
    START_MINUTE = "start_minute"
    END_HOUR = "end_hour"
    END_MINUTE = "end_minute"
    ENABLED = "enabled"


class CleanSummaryField(str, Enum):
    CLEAN_TIME = "clean_time"
    CLEAN_AREA = "clean_area"
    CLEAN_COUNT = "clean_count"
    DUST_COLLECTION_COUNT = "dust_collection_count"
    RECORDS = "records"


class CleanRecordField(str, Enum):
    BEGIN = "begin"
    END = "end"
    DURATION = "duration"
    AREA = "area"
    ERROR = "error"
    COMPLETE = "complete"
    START_TYPE = "start_type"
    CLEAN_TYPE = "clean_type"
    FINISH_REASON = "finish_reason"
    DUST_COLLECTION_STATUS = "dust_collection_status"
    AVOID_COUNT = "avoid_count"
    WASH_COUNT = "wash_count"
    MAP_FLAG = "map_flag"


class ConsumableField(str, Enum):
    MAIN_BRUSH_WORK_TIME = "main_brush_work_time"
    SIDE_BRUSH_WORK_TIME = "side_brush_work_time"
    FILTER_WORK_TIME = "filter_work_time"
    FILTER_ELEMENT_WORK_TIME = "filter_element_work_time"
    SENSOR_DIRTY_TIME = "sensor_dirty_time"
    STRAINER_WORK_TIMES = "strainer_work_times"
    DUST_COLLECTION_WORK_TIMES = "dust_collection_work_times"
    CLEANING_BRUSH_WORK_TIMES = "cleaning_brush_work_times"


class MultiMapListMapInfoBakMapsField(str, Enum):
    MAPFLAG = "mapFlag"
    ADD_TIME = "add_time"


class MultiMapListMapInfoField(str, Enum):
    MAPFLAG = "mapFlag"
    ADD_TIME = "add_time"
    LENGTH = "length"
    NAME = "name"
    BAK_MAPS = "bak_maps"


class MultiMapListField(str, Enum):
    MAX_MULTI_MAP = "max_multi_map"
    MAX_BAK_MAP = "max_bak_map"
    MULTI_MAP_COUNT = "multi_map_count"
    MAP_INFO = "map_info"


class SmartWashField(str, Enum):
    SMART_WASH = "smart_wash"
    WASH_INTERVAL = "wash_interval"


class DustCollectionField(str, Enum):
    MODE = "mode"


class WashTowelField(str, Enum):
    WASH_MODE = "wash_mode"


class NetworkInfoField(str, Enum):
    SSID = "ssid"
    IP = "ip"
    MAC = "mac"
    BSSID = "bssid"
    RSSI = "rssi"


class RoborockDeviceInfoField(str, Enum):
    DEVICE = "device"
    PRODUCT = "product"


class RoborockLocalDeviceInfoField(str, Enum):
    NETWORK_INFO = "network_info"


class RoborockBase(dict):
    def __init__(self, data: dict[str, any]) -> None:
        super().__init__()
        if isinstance(data, dict):
            self.update(data)

    def is_valid(self):
        return set(self.keys()) == set([
            f for f in dir(self)
            if not callable(getattr(self,f)) and not f.startswith('__')
        ])

    def as_dict(self):
        return self.__dict__


class Reference(RoborockBase):

    @property
    def region(self) -> str:
        return self.get(UserDataRRiotReferenceField.REGION)

    @property
    def api(self) -> str:
        return self.get(UserDataRRiotReferenceField.API)

    @property
    def mqtt(self) -> str:
        return self.get(UserDataRRiotReferenceField.MQTT)

    @property
    def l_unknown(self) -> str:
        return self.get(UserDataRRiotReferenceField.L_UNKNOWN)


class RRiot(RoborockBase):

    @property
    def user(self) -> str:
        return self.get(UserDataRRiotField.USER)

    @property
    def password(self) -> str:
        return self.get(UserDataRRiotField.PASSWORD)

    @property
    def h_unknown(self) -> str:
        return self.get(UserDataRRiotField.H_UNKNOWN)

    @property
    def endpoint(self) -> str:
        return self.get(UserDataRRiotField.ENDPOINT)

    @property
    def reference(self) -> Reference:
        return Reference(self.get(UserDataRRiotField.REFERENCE))


class UserData(RoborockBase):

    @property
    def uid(self) -> int:
        return self.get(UserDataField.UID)

    @property
    def token_type(self) -> str:
        return self.get(UserDataField.TOKEN_TYPE)

    @property
    def token(self) -> str:
        return self.get(UserDataField.TOKEN)

    @property
    def rr_uid(self) -> str:
        return self.get(UserDataField.RR_UID)

    @property
    def region(self) -> str:
        return self.get(UserDataField.REGION)

    @property
    def country_code(self) -> str:
        return self.get(UserDataField.COUNTRY_CODE)

    @property
    def country(self) -> str:
        return self.get(UserDataField.COUNTRY)

    @property
    def nickname(self) -> str:
        return self.get(UserDataField.NICKNAME)

    @property
    def rriot(self) -> RRiot:
        return RRiot(self.get(UserDataField.RRIOT))

    @property
    def tuya_device_state(self) -> int:
        return self.get(UserDataField.TUYA_DEVICE_STATE)

    @property
    def avatar_url(self) -> str:
        return self.get(UserDataField.AVATAR_URL)


class LoginData(RoborockBase):

    @property
    def user_data(self) -> UserData:
        user_data = self.get("user_data")
        if user_data:
            return UserData(user_data)

    @property
    def home_data(self):
        home_data = self.get("home_data")
        if home_data:
            return HomeData(home_data)

    @property
    def email(self):
        return self.get("email")


class HomeDataProductSchema(RoborockBase):

    @property
    def id(self):
        return self.get(HomeDataProductSchemaField.ID)

    @property
    def name(self):
        return self.get(HomeDataProductSchemaField.NAME)

    @property
    def code(self):
        return self.get(HomeDataProductSchemaField.CODE)

    @property
    def mode(self):
        return self.get(HomeDataProductSchemaField.MODE)

    @property
    def type(self):
        return self.get(HomeDataProductSchemaField.TYPE)

    @property
    def product_property(self):
        return self.get(HomeDataProductSchemaField.PROPERTY)

    @property
    def desc(self):
        return self.get(HomeDataProductSchemaField.DESC)


class HomeDataProduct(RoborockBase):

    @property
    def id(self) -> str:
        return self.get(HomeDataProductField.ID)

    @property
    def name(self) -> str:
        return self.get(HomeDataProductField.NAME)

    @property
    def code(self) -> str:
        return self.get(HomeDataProductField.CODE)

    @property
    def model(self) -> str:
        return self.get(HomeDataProductField.MODEL)

    @property
    def iconurl(self) -> str:
        return self.get(HomeDataProductField.ICONURL)

    @property
    def attribute(self):
        return self.get(HomeDataProductField.ATTRIBUTE)

    @property
    def capability(self) -> int:
        return self.get(HomeDataProductField.CAPABILITY)

    @property
    def category(self) -> str:
        return self.get(HomeDataProductField.CATEGORY)

    @property
    def schema(self) -> list[HomeDataProductSchema]:
        return [HomeDataProductSchema(schema) for schema in self.get(HomeDataProductField.SCHEMA)]


class HomeDataDeviceStatus(RoborockBase):

    @property
    def id(self):
        return self.get(HomeDataDeviceStatusField.ID)

    @property
    def name(self):
        return self.get(HomeDataDeviceStatusField.NAME)

    @property
    def code(self):
        return self.get(HomeDataDeviceStatusField.CODE)

    @property
    def model(self):
        return self.get(HomeDataDeviceStatusField.MODEL)

    @property
    def icon_url(self):
        return self.get(HomeDataDeviceStatusField.ICON_URL)

    @property
    def attribute(self):
        return self.get(HomeDataDeviceStatusField.ATTRIBUTE)

    @property
    def capability(self):
        return self.get(HomeDataDeviceStatusField.CAPABILITY)

    @property
    def category(self):
        return self.get(HomeDataDeviceStatusField.CATEGORY)

    @property
    def schema(self):
        return self.get(HomeDataDeviceStatusField.SCHEMA)


class HomeDataDevice(RoborockBase):

    @property
    def duid(self) -> str:
        return self.get(HomeDataDeviceField.DUID)

    @property
    def name(self) -> str:
        return self.get(HomeDataDeviceField.NAME)

    @property
    def attribute(self):
        return self.get(HomeDataDeviceField.ATTRIBUTE)

    @property
    def activetime(self) -> int:
        return self.get(HomeDataDeviceField.ACTIVETIME)

    @property
    def local_key(self) -> str:
        return self.get(HomeDataDeviceField.LOCAL_KEY)

    @property
    def runtime_env(self):
        return self.get(HomeDataDeviceField.RUNTIME_ENV)

    @property
    def time_zone_id(self) -> str:
        return self.get(HomeDataDeviceField.TIME_ZONE_ID)

    @property
    def icon_url(self) -> str:
        return self.get(HomeDataDeviceField.ICON_URL)

    @property
    def product_id(self) -> str:
        return self.get(HomeDataDeviceField.PRODUCT_ID)

    @property
    def lon(self):
        return self.get(HomeDataDeviceField.LON)

    @property
    def lat(self):
        return self.get(HomeDataDeviceField.LAT)

    @property
    def share(self) -> bool:
        return self.get(HomeDataDeviceField.SHARE)

    @property
    def share_time(self):
        return self.get(HomeDataDeviceField.SHARE_TIME)

    @property
    def online(self) -> bool:
        return self.get(HomeDataDeviceField.ONLINE)

    @property
    def fv(self) -> str:
        return self.get(HomeDataDeviceField.FV)

    @property
    def pv(self) -> str:
        return self.get(HomeDataDeviceField.PV)

    @property
    def room_id(self):
        return self.get(HomeDataDeviceField.ROOM_ID)

    @property
    def tuya_uuid(self):
        return self.get(HomeDataDeviceField.TUYA_UUID)

    @property
    def tuya_migrated(self) -> bool:
        return self.get(HomeDataDeviceField.TUYA_MIGRATED)

    @property
    def extra(self):
        return self.get(HomeDataDeviceField.EXTRA)

    @property
    def sn(self) -> str:
        return self.get(HomeDataDeviceField.SN)

    @property
    def feature_set(self) -> str:
        return self.get(HomeDataDeviceField.FEATURE_SET)

    @property
    def new_feature_set(self) -> str:
        return self.get(HomeDataDeviceField.NEW_FEATURE_SET)

    @property
    def device_status(self) -> HomeDataDeviceStatus:
        return HomeDataDeviceStatus(self.get(HomeDataDeviceField.DEVICE_STATUS))

    @property
    def silent_ota_switch(self) -> bool:
        return self.get(HomeDataDeviceField.SILENT_OTA_SWITCH)


class HomeDataRoom(RoborockBase):

    @property
    def id(self):
        return self.get(HomeDataRoomField.ID)

    @property
    def name(self):
        return self.get(HomeDataRoomField.NAME)


class HomeData(RoborockBase):

    @property
    def id(self) -> int:
        return self.get(HomeDataField.ID)

    @property
    def name(self) -> str:
        return self.get(HomeDataField.NAME)

    @property
    def lon(self):
        return self.get(HomeDataField.LON)

    @property
    def lat(self):
        return self.get(HomeDataField.LAT)

    @property
    def geo_name(self):
        return self.get(HomeDataField.GEO_NAME)

    @property
    def products(self) -> list[HomeDataProduct]:
        return [HomeDataProduct(product) for product in self.get(HomeDataField.PRODUCTS)]

    @property
    def devices(self) -> list[HomeDataDevice]:
        return [HomeDataDevice(device) for device in self.get(HomeDataField.DEVICES)]

    @property
    def received_devices(self) -> list[HomeDataDevice]:
        return [HomeDataDevice(device) for device in self.get(HomeDataField.RECEIVED_DEVICES)]

    @property
    def rooms(self) -> list[HomeDataRoom]:
        return [HomeDataRoom(room) for room in self.get(HomeDataField.ROOMS)]


class Status(RoborockBase):

    @property
    def msg_ver(self) -> int:
        return self.get(StatusField.MSG_VER)

    @property
    def msg_seq(self) -> int:
        return self.get(StatusField.MSG_SEQ)

    @property
    def status(self) -> str:
        return STATE_CODE_TO_STATUS.get(self.state)

    @property
    def state(self) -> int:
        return self.get(StatusField.STATE)

    @property
    def battery(self) -> int:
        return self.get(StatusField.BATTERY)

    @property
    def clean_time(self) -> int:
        return self.get(StatusField.CLEAN_TIME)

    @property
    def clean_area(self) -> int:
        return self.get(StatusField.CLEAN_AREA)

    @property
    def error_code(self) -> int:
        return self.get(StatusField.ERROR_CODE)

    @property
    def error(self) -> str:
        return ERROR_CODE_TO_TEXT.get(self.error_code)

    @property
    def map_present(self) -> int:
        return self.get(StatusField.MAP_PRESENT)

    @property
    def in_cleaning(self) -> int:
        return self.get(StatusField.IN_CLEANING)

    @property
    def in_returning(self) -> int:
        return self.get(StatusField.IN_RETURNING)

    @property
    def in_fresh_state(self) -> int:
        return self.get(StatusField.IN_FRESH_STATE)

    @property
    def lab_status(self) -> int:
        return self.get(StatusField.LAB_STATUS)

    @property
    def water_box_status(self) -> int:
        return self.get(StatusField.WATER_BOX_STATUS)

    @property
    def back_type(self) -> int:
        return self.get(StatusField.BACK_TYPE)

    @property
    def wash_phase(self) -> int:
        return self.get(StatusField.WASH_PHASE)

    @property
    def wash_ready(self) -> int:
        return self.get(StatusField.WASH_READY)

    @property
    def fan_power_code(self) -> int:
        return self.get(StatusField.FAN_POWER)

    @property
    def fan_power(self) -> str:
        return FAN_SPEED_CODES.get(self.fan_power_code)

    @property
    def dnd_enabled(self) -> int:
        return self.get(StatusField.DND_ENABLED)

    @property
    def map_status(self) -> int:
        return self.get(StatusField.MAP_STATUS)

    @property
    def is_locating(self) -> int:
        return self.get(StatusField.IS_LOCATING)

    @property
    def lock_status(self) -> int:
        return self.get(StatusField.LOCK_STATUS)

    @property
    def water_box_mode(self) -> int:
        return self.get(StatusField.WATER_BOX_MODE)

    @property
    def mop_intensity(self) -> str:
        return MOP_INTENSITY_CODES.get(self.water_box_mode)

    @property
    def water_box_carriage_status(self) -> int:
        return self.get(StatusField.WATER_BOX_CARRIAGE_STATUS)

    @property
    def mop_forbidden_enable(self) -> int:
        return self.get(StatusField.MOP_FORBIDDEN_ENABLE)

    @property
    def camera_status(self) -> int:
        return self.get(StatusField.CAMERA_STATUS)

    @property
    def is_exploring(self) -> int:
        return self.get(StatusField.IS_EXPLORING)

    @property
    def home_sec_status(self) -> int:
        return self.get(StatusField.HOME_SEC_STATUS)

    @property
    def home_sec_enable_password(self) -> int:
        return self.get(StatusField.HOME_SEC_ENABLE_PASSWORD)

    @property
    def adbumper_status(self) -> list[int]:
        return self.get(StatusField.ADBUMPER_STATUS)

    @property
    def water_shortage_status(self) -> int:
        return self.get(StatusField.WATER_SHORTAGE_STATUS)

    @property
    def dock_type_code(self) -> int:
        return self.get(StatusField.DOCK_TYPE)

    @property
    def dock_type(self) -> RoborockDockType:
        return DOCK_TYPE_MAP.get(self.get(StatusField.DOCK_TYPE), RoborockDockType.UNKNOWN)

    @property
    def dust_collection_status(self) -> int:
        return self.get(StatusField.DUST_COLLECTION_STATUS)

    @property
    def auto_dust_collection(self) -> int:
        return self.get(StatusField.AUTO_DUST_COLLECTION)

    @property
    def avoid_count(self) -> int:
        return self.get(StatusField.AVOID_COUNT)

    @property
    def mop_mode_code(self) -> int:
        return self.get(StatusField.MOP_MODE)

    @property
    def mop_mode(self) -> str:
        return MOP_MODE_CODES.get(self.mop_mode_code)

    @property
    def debug_mode(self) -> int:
        return self.get(StatusField.DEBUG_MODE)

    @property
    def collision_avoid_status(self) -> int:
        return self.get(StatusField.COLLISION_AVOID_STATUS)

    @property
    def switch_map_mode(self) -> int:
        return self.get(StatusField.SWITCH_MAP_MODE)

    @property
    def dock_error_status_code(self) -> int:
        return self.get(StatusField.DOCK_ERROR_STATUS)

    @property
    def dock_error_status(self) -> str:
        return DOCK_ERROR_TO_TEXT.get(self.get(StatusField.DOCK_ERROR_STATUS))

    @property
    def charge_status(self) -> int:
        return self.get(StatusField.CHARGE_STATUS)

    @property
    def unsave_map_reason(self) -> int:
        return self.get(StatusField.UNSAVE_MAP_REASON)

    @property
    def unsave_map_flag(self) -> int:
        return self.get(StatusField.UNSAVE_MAP_FLAG)


class DNDTimer(RoborockBase):

    @property
    def start_hour(self) -> int:
        return self.get(DNDTimerField.START_HOUR)

    @property
    def start_minute(self) -> int:
        return self.get(DNDTimerField.START_MINUTE)

    @property
    def end_hour(self) -> int:
        return self.get(DNDTimerField.END_HOUR)

    @property
    def end_minute(self) -> int:
        return self.get(DNDTimerField.END_MINUTE)

    @property
    def enabled(self) -> int:
        return self.get(DNDTimerField.ENABLED)


class CleanSummary(RoborockBase):

    @property
    def clean_time(self) -> int:
        return self.get(CleanSummaryField.CLEAN_TIME)

    @property
    def clean_area(self) -> int:
        return self.get(CleanSummaryField.CLEAN_AREA)

    @property
    def clean_count(self) -> int:
        return self.get(CleanSummaryField.CLEAN_COUNT)

    @property
    def dust_collection_count(self) -> int:
        return self.get(CleanSummaryField.DUST_COLLECTION_COUNT)

    @property
    def records(self) -> list[int]:
        return self.get(CleanSummaryField.RECORDS)


class CleanRecord(RoborockBase):

    @property
    def begin(self) -> int:
        return self.get(CleanRecordField.BEGIN)

    @property
    def end(self) -> int:
        return self.get(CleanRecordField.END)

    @property
    def duration(self) -> int:
        return self.get(CleanRecordField.DURATION)

    @property
    def area(self) -> int:
        return self.get(CleanRecordField.AREA)

    @property
    def error(self) -> int:
        return self.get(CleanRecordField.ERROR)

    @property
    def complete(self) -> int:
        return self.get(CleanRecordField.COMPLETE)

    @property
    def start_type(self) -> int:
        return self.get(CleanRecordField.START_TYPE)

    @property
    def clean_type(self) -> int:
        return self.get(CleanRecordField.CLEAN_TYPE)

    @property
    def finish_reason(self) -> int:
        return self.get(CleanRecordField.FINISH_REASON)

    @property
    def dust_collection_status(self) -> int:
        return self.get(CleanRecordField.DUST_COLLECTION_STATUS)

    @property
    def avoid_count(self) -> int:
        return self.get(CleanRecordField.AVOID_COUNT)

    @property
    def wash_count(self) -> int:
        return self.get(CleanRecordField.WASH_COUNT)

    @property
    def map_flag(self) -> int:
        return self.get(CleanRecordField.MAP_FLAG)


class Consumable(RoborockBase):

    @property
    def main_brush_work_time(self) -> int:
        return self.get(ConsumableField.MAIN_BRUSH_WORK_TIME)

    @property
    def side_brush_work_time(self) -> int:
        return self.get(ConsumableField.SIDE_BRUSH_WORK_TIME)

    @property
    def filter_work_time(self) -> int:
        return self.get(ConsumableField.FILTER_WORK_TIME)

    @property
    def filter_element_work_time(self) -> int:
        return self.get(ConsumableField.FILTER_ELEMENT_WORK_TIME)

    @property
    def sensor_dirty_time(self) -> int:
        return self.get(ConsumableField.SENSOR_DIRTY_TIME)

    @property
    def strainer_work_times(self) -> int:
        return self.get(ConsumableField.STRAINER_WORK_TIMES)

    @property
    def dust_collection_work_times(self) -> int:
        return self.get(ConsumableField.DUST_COLLECTION_WORK_TIMES)

    @property
    def cleaning_brush_work_times(self) -> int:
        return self.get(ConsumableField.CLEANING_BRUSH_WORK_TIMES)


class MultiMapsListMapInfoBakMaps(RoborockBase):

    @property
    def mapflag(self):
        return self.get(MultiMapListMapInfoBakMapsField.MAPFLAG)

    @property
    def add_time(self):
        return self.get(MultiMapListMapInfoBakMapsField.ADD_TIME)


class MultiMapsListMapInfo(RoborockBase):

    @property
    def mapflag(self):
        return self.get(MultiMapListMapInfoField.MAPFLAG)

    @property
    def add_time(self):
        return self.get(MultiMapListMapInfoField.ADD_TIME)

    @property
    def length(self):
        return self.get(MultiMapListMapInfoField.LENGTH)

    @property
    def name(self):
        return self.get(MultiMapListMapInfoField.NAME)

    @property
    def bak_maps(self):
        return [MultiMapsListMapInfoBakMaps(bak_maps) for bak_maps in self.get(MultiMapListMapInfoField.BAK_MAPS)]


class MultiMapsList(RoborockBase):

    @property
    def max_multi_map(self) -> int:
        return self.get(MultiMapListField.MAX_MULTI_MAP)

    @property
    def max_bak_map(self) -> int:
        return self.get(MultiMapListField.MAX_BAK_MAP)

    @property
    def multi_map_count(self) -> int:
        return self.get(MultiMapListField.MULTI_MAP_COUNT)

    @property
    def map_info(self) -> list[MultiMapsListMapInfo]:
        return [MultiMapsListMapInfo(map_info) for map_info in self.get(MultiMapListField.MAP_INFO)]


class SmartWashParameters(RoborockBase):

    @property
    def smart_wash(self) -> int:
        return self.get(SmartWashField.SMART_WASH)

    @property
    def wash_interval(self) -> int:
        return self.get(SmartWashField.WASH_INTERVAL)


class DustCollectionMode(RoborockBase):

    @property
    def mode(self) -> RoborockDockDustCollectionType:
        return DUST_COLLECTION_MAP.get(self.get(DustCollectionField.MODE))


class WashTowelMode(RoborockBase):

    @property
    def wash_mode(self) -> RoborockDockWashingModeType:
        return WASH_MODE_MAP.get(self.get(WashTowelField.WASH_MODE))


class NetworkInfo(RoborockBase):
    @property
    def ssid(self) -> str:
        return self.get(NetworkInfoField.SSID)

    @property
    def ip(self) -> str:
        return self.get(NetworkInfoField.IP)

    @property
    def mac(self) -> str:
        return self.get(NetworkInfoField.MAC)

    @property
    def bssid(self) -> str:
        return self.get(NetworkInfoField.BSSID)

    @property
    def rssi(self) -> int:
        return self.get(NetworkInfoField.RSSI)


class RoborockDeviceInfo(RoborockBase):
    @property
    def device(self) -> HomeDataDevice:
        return HomeDataDevice(self.get(RoborockDeviceInfoField.DEVICE))

    @property
    def product(self) -> HomeDataProduct:
        return HomeDataProduct(self.get(RoborockDeviceInfoField.PRODUCT))


class RoborockLocalDeviceInfo(RoborockDeviceInfo):
    @property
    def network_info(self) -> NetworkInfo:
        return NetworkInfo(self.get(RoborockLocalDeviceInfoField.NETWORK_INFO))
