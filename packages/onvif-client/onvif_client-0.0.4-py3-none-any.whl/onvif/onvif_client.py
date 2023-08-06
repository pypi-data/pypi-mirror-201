#!/user/bin/python
# -*- coding: utf-8 -*-
"""WS-Discoveryを用いてネットワークカメラを検索、ONVIFを用いてネットワークカメラを設定・操作するモジュール

"""


import base64
import os
import urllib.request
from dataclasses import dataclass
from typing import Any, Optional, List
from urllib.parse import urlparse
from ipaddress import IPv4Address

import zeep.helpers
from onvif2 import ONVIFCamera
from onvif2.exceptions import ONVIFError
from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from wsdiscovery import QName


@dataclass
class SocketAddressIn:
    ip_address: str
    port: int
    
    def __post_init__(self):
        if self.port is None:
            self.port = 80


class WsDiscoveryClient:
    """WS-Discoveryクライアント
    
    ネットワークカメラの検索をおこないます。

    """
    NVT_NAMESPACE = "http://www.onvif.org/ver10/network/wsdl"
    NVT_LOCALNAME = "NetworkVideoTransmitter"

    def __init__(self):
        self._service_type = QName(self.NVT_NAMESPACE, self.NVT_LOCALNAME)
        self._wsd = WSDiscovery()
        self._wsd.start()
    
    def dispose(self):
        assert(self._wsd)

        self._wsd.stop()
        self._wsd = None

    def search(self) -> List[SocketAddressIn]:
        """ネットワークカメラの検索をおこないます。
        """
        assert(self._wsd)

        results = []

        services = self._wsd.searchServices(types=[self._service_type])
        for service in services:
            for address in service.getXAddrs():
                # IPアドレスとポートにパースする
                parse_result = urlparse(address)
                # IPv4形式になっているかのチェック
                try:
                    IPv4Address(parse_result.hostname)
                    results.append(SocketAddressIn(parse_result.hostname, parse_result.port))
                except Exception:
                    pass

        return results


class OnvifClient:
    """ONVIFクライアント

    ネットワークカメラの設定・操作をおこないます。

    """
    def __init__(self, ip_address: str, port: int, user_name: Optional[str], password: Optional[str]):
        self._wsdl_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wsdl')

        self._onvif_camera = ONVIFCamera(ip_address, port, user_name, password, wsdl_dir=self._wsdl_dir_path)
    
    def _get_streaming_uri_ver10(self, media_service, profile_token: str) -> str:
        get_stream_uri_request = media_service.create_type('GetStreamUri')
        get_stream_uri_request.ProfileToken = profile_token
        get_stream_uri_request.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}

        get_stream_uri_response = media_service.GetStreamUri(get_stream_uri_request)

        # zeep.objects to dict 後に Uri のみ取得
        return dict(zeep.helpers.serialize_object(get_stream_uri_response))['Uri']

    def _get_streaming_uri_ver20(self, media_service, profile_token: str) -> str:
        get_stream_uri_request = media_service.create_type('GetStreamUri')
        get_stream_uri_request.ProfileToken = profile_token
        get_stream_uri_request.Protocol = 'RTSP'
        streaming_uri = media_service.GetStreamUri(get_stream_uri_request)

        return streaming_uri
    
    def _move(self, profile_token: str, pan_velocity: float=0.0, tilt_velocity: float=0.0, zoom_velocity: float=0.0):
        try:
            ptz_configuration_token = self.get_ptz_configuration_token(profile_token)
            
            ptz_service = self._onvif_camera.create_ptz_service()

            get_status_request = ptz_service.create_type('GetStatus')
            get_status_request.ProfileToken = profile_token
            
            ptz_status = ptz_service.GetStatus(get_status_request)

            get_configuration_options_request = ptz_service.create_type('GetConfigurationOptions')
            get_configuration_options_request.ConfigurationToken = ptz_configuration_token
            ptz_configuration_options = ptz_service.GetConfigurationOptions(get_configuration_options_request)

            continuous_move_request = ptz_service.create_type('ContinuousMove')
            continuous_move_request.ProfileToken = profile_token
            continuous_move_request.Velocity = ptz_status.Position
            continuous_move_request.Velocity.PanTilt.space = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].URI
            continuous_move_request.Velocity.Zoom.space = ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].URI

            continuous_move_request.Velocity.PanTilt.x = pan_velocity
            continuous_move_request.Velocity.PanTilt.y = tilt_velocity
            continuous_move_request.Velocity.Zoom.x = zoom_velocity

            ptz_service.ContinuousMove(continuous_move_request)        
        except ONVIFError:
            pass

    def get_profile_tokens(self) -> List[str]:
        # Ver2.0のMedia Serviceオブジェクトを生成
        try:
            media2_service = self._onvif_camera.create_media2_service()
            return [profile.token for profile in media2_service.GetProfiles()]
        except ONVIFError:
            pass

        # Ver1.0のMedia Serviceオブジェクトを生成
        try:
            media_service = self._onvif_camera.create_media_service()
            return [profile.token for profile in media_service.GetProfiles()]
        except ONVIFError:
            pass

        return []
    
    def get_streaming_uri(self, profile_token: str) -> Optional[str]:
        # Ver2.0のMedia Serviceオブジェクトを生成
        try:
            media2_service = self._onvif_camera.create_media2_service()
            return self._get_streaming_uri_ver20(media2_service, profile_token)
        except ONVIFError:
            pass

        # Ver1.0のMedia Serviceオブジェクトを生成
        try:
            media_service = self._onvif_camera.create_media_service()
            return self._get_streaming_uri_ver10(media_service, profile_token)
        except ONVIFError:
            pass

        return None
    
    def get_snapshot_uri(self, profile_token: str) -> Optional[str]:
        # Ver2.0のMedia Serviceオブジェクトを生成
        try:
            media2_service = self._onvif_camera.create_media2_service()
            get_snapshot_uri_request = media2_service.create_type('GetSnapshotUri')
            get_snapshot_uri_request.ProfileToken = profile_token
            
            return media2_service.GetSnapshotUri(get_snapshot_uri_request)
        except ONVIFError:
            pass

        # Ver1.0のMedia Serviceオブジェクトを生成
        try:
            media_service = self._onvif_camera.create_media_service()
            get_snapshot_uri_request = media_service.create_type('GetSnapshotUri')
            get_snapshot_uri_request.ProfileToken = profile_token
            
            get_snapshot_uri_response =  media_service.GetSnapshotUri(get_snapshot_uri_request)
            
            # zeep.objects to dict 後に Uri のみ取得
            return dict(zeep.helpers.serialize_object(get_snapshot_uri_response))['Uri']
        except ONVIFError:
            pass

        return None

    def get_snapshot(self, snapshot_uri: str, user_name: str, password: str) -> Optional[bytes]:
        try:
            # Basic認証用の文字列を作成
            basic_user_and_pasword = base64.b64encode('{}:{}'.format(user_name, password).encode('utf-8'))

            # Basic認証付きのGETリクエストを作成する
            request = urllib.request.Request(
                                        snapshot_uri, 
                                        headers={"Authorization": "Basic " + basic_user_and_pasword.decode('utf-8')})

            # 送信する
            with urllib.request.urlopen(request) as response:
                snapshot_image = response.read()
                return snapshot_image
        except Exception:
            pass
        
        return None
    
    def get_video_encoder_configurations(self) -> List[Any]:
        # Ver1.0のMedia Serviceオブジェクトを生成
        try:
            media_service = self._onvif_camera.create_media_service()

            return media_service.GetVideoEncoderConfigurations()
        except ONVIFError:
            pass

        return []

    def get_video_encoder_configuration(self, video_encoder_configuration_token: str) -> Optional[Any]:
        # Ver1.0のMedia Serviceオブジェクトを生成
        try:
            media_service = self._onvif_camera.create_media_service()

            get_video_encoder_configuration_request = media_service.create_type('GetVideoEncoderConfiguration')
            get_video_encoder_configuration_request.ConfigurationToken = video_encoder_configuration_token

            return media_service.GetVideoEncoderConfiguration(get_video_encoder_configuration_request)
        except ONVIFError:
            pass

        return None

    def set_video_encoder_configuration(self, video_encoder_configuration: Any):
        # Ver1.0のMedia Serviceオブジェクトを生成
        try:
            media_service = self._onvif_camera.create_media_service()

            set_video_encoder_configuration_request = media_service.create_type('SetVideoEncoderConfiguration')
            set_video_encoder_configuration_request.Configuration = video_encoder_configuration
            set_video_encoder_configuration_request.ForcePersistence = True

            media_service.SetVideoEncoderConfiguration(set_video_encoder_configuration_request)
        except ONVIFError:
            pass
    
    def get_ptz_configuration_token(self, profile_token: str) -> Optional[str]:
        # Ver1.0のMedia Serviceオブジェクトを生成
        try:
            media_service = self._onvif_camera.create_media_service()

            get_profile_request = media_service.create_type('GetProfile')
            get_profile_request.ProfileToken = profile_token

            profile = media_service.GetProfile(get_profile_request)

            if hasattr(profile, 'PTZConfiguration'):
                return profile.PTZConfiguration.token
            
            return None
        except ONVIFError:
            pass

        return None

    def goto_home_position(self, profile_token: str):
        try:
            ptz_service = self._onvif_camera.create_ptz_service()

            goto_home_position_request = ptz_service.create_type('GotoHomePosition')
            goto_home_position_request.ProfileToken = profile_token
            
            ptz_service.GotoHomePosition(goto_home_position_request)
        except ONVIFError:
            pass

    def move_pan(self, profile_token: str, velocity: float):
        self._move(profile_token, pan_velocity=velocity)

    def move_tilt(self, profile_token: str, velocity: float):
        self._move(profile_token, tilt_velocity=velocity)

    def move_zoom(self, profile_token: str, velocity: float):
        self._move(profile_token, zoom_velocity=velocity)

    def stop_ptz(self, profile_token: str):
        try:
            ptz_service = self._onvif_camera.create_ptz_service()

            stop_request = ptz_service.create_type('Stop')
            stop_request.ProfileToken = profile_token
            stop_request.PanTilt = True
            stop_request.Zoom = True

            ptz_service.Stop(stop_request)
        except ONVIFError:
            pass
