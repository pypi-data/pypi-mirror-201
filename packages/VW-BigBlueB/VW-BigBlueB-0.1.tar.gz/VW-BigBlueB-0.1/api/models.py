# Create your models here.
import os
import random
from ast import parse
from hashlib import sha1
from urllib.parse import urlencode
from urllib.request import urlopen
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import django.utils.timezone
from dotenv import load_dotenv

load_dotenv()
SALT = os.environ.get('SALT_VALUE')
BBB_API_URL = os.environ.get('BBB_API_URL_VALUE')
BASE_URL = os.environ.get('BASE_URL_VALUE')


class Meeting(models.Model):
    user_id = models.IntegerField(blank=False)
    event_name = models.CharField(max_length=100)
    event_creator_name = models.CharField(max_length=50)
    event_creator_email = models.CharField(max_length=50)
    private_meeting_id = models.CharField(max_length=100, unique=True)
    public_meeting_id = models.CharField(max_length=100, unique=True)
    meeting_type = models.CharField(max_length=10, blank=True, null=True, default='private')
    attendee_password = models.CharField(max_length=50)
    hashed_attendee_password = models.CharField(max_length=100, null=True, blank=True, default=None)
    moderator_password = models.CharField(max_length=50)
    hashed_moderator_password = models.CharField(max_length=100, null=True, blank=True, default=None)
    viewer_password = models.CharField(max_length=50)
    hashed_viewer_password = models.CharField(max_length=100, null=True, blank=True, default=None)
    viewer_mode = models.BooleanField(default=False, blank=True, null=True)
    moderator_only_text = models.TextField(blank=True, null=True)
    welcome = models.TextField(default='welcome', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    max_participant = models.IntegerField(blank=True, null=True, default=0, validators=[
        MaxValueValidator(1000),
        MinValueValidator(0)
    ])
    record = models.BooleanField(default=False, blank=True, null=True)
    duration = models.IntegerField(default=1000, blank=True, null=True)
    mute_on_start = models.BooleanField(default=True, blank=True, null=True)
    banner_text = models.CharField(max_length=300, blank=True, null=True)
    logo = models.ImageField(blank=True, upload_to='logo_images', null=True)
    guest_policy = models.CharField(max_length=25, default='ALWAYS_ACCEPT', blank=True, null=True)
    end_when_no_moderator = models.BooleanField(default=False, blank=True, null=True)
    allow_moderator_to_unmute_user = models.BooleanField(default=False, null=True, blank=True)
    webcam_only_for_moderator = models.BooleanField(default=False, blank=True, null=True)
    auto_start_recording = models.BooleanField(default=False, blank=True, null=True)
    allow_start_stop_recording = models.BooleanField(default=True, blank=True, null=True)
    disable_cam = models.BooleanField(default=False, null=True, blank=True)
    disable_mic = models.BooleanField(default=False, null=True, blank=True)
    disable_private_chat = models.BooleanField(default=False, null=True, blank=True)
    disable_public_chat = models.BooleanField(default=False, null=True, blank=True)
    disable_note = models.BooleanField(default=False, null=True, blank=True)
    logout_url = models.URLField(blank=True, null=True)
    lock_layout = models.BooleanField(default=False, null=True, blank=True)
    lock_on_join = models.BooleanField(default=True, null=True, blank=True)
    hide_users = models.BooleanField(default=False, null=True, blank=True)
    schedule_time = models.DateTimeField(blank=False, default=django.utils.timezone.now, null=True)
    primary_color = models.CharField(blank=True, max_length=20, null=True)
    secondary_color = models.CharField(blank=True, max_length=20, null=True)
    back_image = models.URLField(blank=True, null=True)
    event_tag = models.CharField(blank=True, max_length=25, null=True)
    schedular_name_reminder = models.CharField(max_length=50)
    cover_image = models.ImageField(blank=True, upload_to='cover_images', null=True)
    is_streaming = models.BooleanField(default=False, null=True, blank=True)
    bbb_resolution = models.CharField(max_length=20, default="1280x720", blank=True, null=True)
    bbb_stream_url_vw = models.TextField(blank=True, null=True)
    raw_time = models.CharField(max_length=100, blank=True, null=True)
    give_nft = models.BooleanField(default=False, null=True, blank=True)
    give_vc = models.BooleanField(default=False, null=True, blank=True)
    send_otp = models.BooleanField(default=False, null=True, blank=True)
    audience_airdrop = models.BooleanField(default=False, blank=True, null=True)
    password_auth = models.BooleanField(default=False, blank=True, null=True)
    public_otp = models.BooleanField(default=False, blank=True, null=True)
    public_nft_flow = models.BooleanField(default=False, blank=True, null=True)
    public_nft_activate = models.BooleanField(default=False, blank=True, null=True)
    public_stream = models.BooleanField(default=False, blank=True, null=True)
    join_count = models.IntegerField(default=0, null=True, blank=True)

    @classmethod
    def api_call(self, query, call):
        prepared = "%s%s%s" % (call, query, SALT)
        checksum = sha1(prepared.encode('utf-8')).hexdigest()
        result = "%s&checksum=%s" % (query, checksum)
        return result

    def is_running(self):
        call = 'isMeetingRunning'
        query = urlencode((
            ('meetingID', self.private_meeting_id),
        ))
        hashed = self.api_call(query, call)
        url = BBB_API_URL + 'api/' + call + '?' + hashed
        result = parse(urlopen(url).read())
        return result.find('running').text

    @classmethod
    def end_meeting(cls, private_meeting_id, password):
        call = 'end'
        query = urlencode((
            ('meetingID', private_meeting_id),
            ('password', password),
        ))
        hashed = cls.api_call(query, call)
        url = BBB_API_URL + 'api/' + call + '?' + hashed
        result = parse(urlopen(url).read())
        return result

    @classmethod
    def meeting_info(cls, private_meeting_id, password):
        call = 'getMeetingInfo'
        query = urlencode((
            ('meetingID', private_meeting_id),
            ('password', password),
        ))
        hashed = cls.api_call(query, call)
        url = BBB_API_URL + 'api/' + call + '?' + hashed
        r = parse(urlopen(url).read())
        if r:
            # Create dict of values for easy use in template
            d = {
                'start_time': r.find('startTime').text,
                'end_time': r.find('endTime').text,
                'participant_count': r.find('participantCount').text,
                'moderator_count': r.find('moderatorCount').text,
                'max_users': r.find('maxUsers').text
            }
            return d
        else:
            return None

    @classmethod
    def get_meetings(cls):
        call = 'getMeetings'
        query = urlencode((
            ('random', 'random'),
        ))
        hashed = cls.api_call(query, call)
        url = BBB_API_URL + 'api/' + call + '?' + hashed
        result = parse(urlopen(url).read())
        if result:
            # Create dict of values for easy use in template
            d = []
            r = result[1].findall('meeting')
            for m in r:
                name = m.find('meetingName').text
                password = m.find('moderatorPW').text
                meeting_id = m.find('meetingID').text
                d.append({
                    'name': name,
                    'running': m.find('running').text,
                    'info': Meeting.meeting_info(
                        meeting_id,
                        password)
                })
            return d

    def start(self):
        call = 'create'
        voicebridge = 70000 + random.randint(0, 9999)
        tuple_1 = (
            ('name', self.event_name),
            ('meetingID', self.private_meeting_id),
            ('attendeePW', self.attendee_password),
            ('moderatorPW', self.moderator_password),
            ('voiceBridge', voicebridge),
            ('moderatorOnlyMessage', self.moderator_only_text),
            ('welcome', self.welcome),
            ('maxParticipants', self.max_participant),
            ('record', self.record),
            ('duration', self.duration),
            ('logoutURL', self.logout_url),
            ('muteOnStart', self.mute_on_start),
            ('logo', str(path_getter(self.logo))),
            ('endWhenNoModerator', self.end_when_no_moderator),
            ('guestPolicy', self.guest_policy),
            ('allowModsToUnmuteUsers', self.allow_moderator_to_unmute_user),
            ('webcamsOnlyForModerator', self.webcam_only_for_moderator),
            ('autoStartRecording', self.auto_start_recording),
            ('allowStartStopRecording', self.allow_start_stop_recording),
            ('lockSettingsDisableCam', self.disable_cam),
            ('lockSettingsDisableMic', self.disable_mic),
            ('lockSettingsDisableNote', self.disable_note),
            ('lockSettingsDisablePrivateChat', self.disable_public_chat),
            ('lockSettingsDisablePublicChat', self.disable_private_chat),
            ('lockSettingsLockedLayout', self.lock_layout),
            ('lockSettingsLockOnJoin', self.lock_on_join),
            ('lockSettingsHideUserList', self.hide_users),
            ('meta_bbb-origin', 'Greenlight'),
            ('meta_bbb-origin-version', "v2"),
            ('meta_bbb-origin-server-name', 'room.video.wiki'),
            ('meta_primary-color', self.primary_color),
            ('meta_secondary-color', self.secondary_color),
            ('meta_back-image', self.back_image),
            ('meta_gl-listed', False)
        )
        tuple_2 = ('bannerText', self.banner_text)
        if self.banner_text == None:
            f_tuple = tuple_1
        else:
            tuple_1_list = list(tuple_1)
            tuple_1_list.append(tuple_2)
            f_tuple = tuple(tuple_1_list)
        query = urlencode(f_tuple)
        hashed = self.api_call(query, call)
        url = BBB_API_URL + 'api/' + call + '?' + hashed
        result = parse(urlopen(url).read())
        return result

    @classmethod
    def join_url(cls, meeting_id, name, password, force_listen_only, enable_screen_sharing, enable_webcam):
        call = 'join'
        query = urlencode((
            ('meetingID', meeting_id),
            ('password', password),
            ('fullName', name),
            ('userdata-bbb_force_listen_only', force_listen_only),
            ('bbb_enable_screen_sharing', enable_screen_sharing),
            ('userdata-bbb_enable_video', enable_webcam)
        ))
        hashed = cls.api_call(query, call)
        url = BBB_API_URL + 'api/' + call + '?' + hashed
        return url

    @classmethod
    def get_recordings(cls, private_meeting_id):
        call = "getRecordings"
        query = urlencode((
            ('meetingID', private_meeting_id),
        ))
        hashed = cls.api_call(query, call)
        url = BBB_API_URL + 'api/' + call + '?' + hashed
        result = parse(urlopen(url).read())
        d = []
        r = result[1].findall('recording')
        for m in r:
            a = m.findall("playback")
            for i in a:
                a = i.findall("format")
                for i in a:
                    url = i.find("url").text
                    return url
        return None

    @classmethod
    def is_meeting_running(cls, private_meeting_id):
        call = 'isMeetingRunning'
        query = urlencode((
            ('meetingID', private_meeting_id),
        ))
        hashed = cls.api_call(query, call)
        url = BBB_API_URL + 'api/' + call + '?' + hashed
        result = parse(urlopen(url).read())
        return result.find('running').text


def path_getter(path):
    if path == "https://videowikistorage.blob.core.windows.net/room-db-backup/vwlogo.png":
        url = path
    else:
        url = BASE_URL + path.url
    return url


def generate_random_key(self):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(8, chars)
    return secret_key


def user_info(token):
    data = {'token': token}
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user_id = valid_data['user_id']
        return user_id

    except ValidationError as v:
        return -1


def user_info_email(token):
    data = {'token': token}
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        email = valid_data['email']
        return email

    except ValidationError as v:
        return -1


def user_info_name(token):
    data = {'token': token}
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        name = valid_data['username']
        return name

    except ValidationError as v:
        return -1
