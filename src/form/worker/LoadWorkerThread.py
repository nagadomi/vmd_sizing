# -*- coding: utf-8 -*-
#

import wx
import time
from form.worker.BaseWorkerThread import BaseWorkerThread


class LoadWorkerThread(BaseWorkerThread):

    def __init__(self, frame: wx.Frame, result_event: wx.Event, is_exec: bool, is_morph: bool, is_arm: bool):
        self.elapsed_time = 0
        self.is_exec = is_exec
        self.is_morph = is_morph
        self.is_arm = is_arm

        super().__init__(frame, result_event, frame.file_panel_ctrl.console_ctrl)

    def thread_event(self):
        start = time.time()

        # メインセットの読み込み
        self.result = self.frame.file_panel_ctrl.file_set.load() and self.result

        # 複数セットの読み込み
        for file_set in self.frame.multi_panel_ctrl.file_set_list:
            self.result = file_set.load() and self.result
            
        # カメラモーションの読み込み
        if self.frame.camera_panel_ctrl.camera_vmd_file_ctrl.is_set_path():
            self.result = self.frame.camera_panel_ctrl.camera_vmd_file_ctrl.load() and self.result
        
        # カメラ元モデルの読み込み
        for camera_set in self.frame.camera_panel_ctrl.camera_set_dict.values():
            if camera_set.camera_model_file_ctrl.is_set_path():
                self.result = camera_set.camera_model_file_ctrl.load() and self.result
        
        self.elapsed_time = time.time() - start

    def post_event(self):
        wx.PostEvent(self.frame, self.result_event(result=self.result, elapsed_time=self.elapsed_time, is_exec=self.is_exec, is_morph=self.is_morph, is_arm=self.is_arm))
