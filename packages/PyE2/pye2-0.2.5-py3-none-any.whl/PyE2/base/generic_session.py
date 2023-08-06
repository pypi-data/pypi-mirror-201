"""
Copyright 2019-2022 Lummetry.AI (Knowledge Investment Group SRL). All Rights Reserved.


* NOTICE:  All information contained herein is, and remains
* the property of Knowledge Investment Group SRL.  
* The intellectual and technical concepts contained
* herein are proprietary to Knowledge Investment Group SRL
* and may be covered by Romanian and Foreign Patents,
* patents in process, and are protected by trade secret or copyright law.
* Dissemination of this information or reproduction of this material
* is strictly forbidden unless prior written permission is obtained
* from Knowledge Investment Group SRL.


@copyright: Lummetry.AI
@author: Lummetry\.AI - Stefan Saraev
@project: 
@description:
"""

import os
import sys
import traceback
from time import localtime, mktime, strftime, strptime
from time import time as tm

from ..const import comms as comm_ct
from .pipeline import Pipeline
from .payload import Payload
from ..io_formatter import IOFormatterManager


class Logger():
  def __init__(self, **kwargs) -> None:
    return

  def P(self, msg, **kwargs):
    print(msg)

  def get_unique_id(self, size=8):
    """
    efficient and low-colision function for small unique id generation
    """
    import random
    import string
    alphabet = string.ascii_lowercase + string.digits
    uid = ''.join(random.choices(alphabet, k=size))
    return uid

  def start_timer(self, *args, **kwargs):
    return

  def end_timer(self, *args, **kwargs):
    return

  def stop_timer(self, *args, **kwargs):
    return

  def time_to_str(self, t=None, fmt='%Y-%m-%d %H:%M:%S'):
    if t is None:
      t = tm()
    return strftime(fmt, localtime(t))

  def get_error_info(self, return_err_val=False):
    """
    Returns error_type, file, method, line for last error if available

    Parameters
    ----------
    return_err_val: boolean, optional
      Whether the method returns or not the error message (err_val)

    Returns
    -------
    if not return_err_val:
      (tuple) str, str, str, str : errortype, file, method, line
    else:
      (tuple) str, str, str, str, str : errortype, file, method, line, err message
    """
    err_type, err_val, err_trace = sys.exc_info()
    if False:
      # dont try this at home :) if you want to pickle a logger instance after
      # `get_error_info` was triggered, then it won't work because `self._last_extracted_error`
      # contain an object of type `traceback` and tracebacks cannot be pickled
      self._last_extracted_error = err_type, err_val, err_trace
    # endif
    if err_type is not None:
      str_err = err_type.__name__
      stack_summary = traceback.extract_tb(err_trace)
      last_error_frame = stack_summary[-1]
      fn = os.path.splitext(os.path.split(last_error_frame.filename)[-1])[0]
      lineno = last_error_frame.lineno
      func_name = last_error_frame.name
      if not return_err_val:
        return str_err, 'File: ' + fn, 'Func: ' + func_name, 'Line: ' + str(lineno)
      else:
        return str_err, 'File: ' + fn, 'Func: ' + func_name, 'Line: ' + str(lineno), str(err_val)
    else:
      return "", "", "", "", ""

  def dict_pretty_format(self, d, indent=4, as_str=True, display_callback=None, display=False, limit_str=250):
    assert isinstance(d, dict), "`d` must be dict"
    if display and display_callback is None:
      display_callback = self.P
    lst_data = []

    def deep_parse(dct, ind=indent):
      for ki, key in enumerate(dct):
        # dct actually can be dict or list
        str_key = str(key) if not isinstance(key, str) else '"{}"'.format(key)
        if isinstance(dct, dict):
          value = dct[key]
          lst_data.append(' ' * ind + str(str_key) + ' : ')
        else:
          value = key
        if isinstance(value, dict):
          if lst_data[-1][-1] in ['[', ',']:
            lst_data.append(' ' * ind + '{')
          else:
            lst_data[-1] = lst_data[-1] + '{'
          deep_parse(value, ind=ind + indent)
          lst_data.append(' ' * ind + '}')
        elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
          lst_data[-1] = lst_data[-1] + '['
          deep_parse(value, ind=ind + indent)
          lst_data.append(' ' * ind + ']')
        else:
          str_value = str(value) if not isinstance(value, str) else '"{}"'.format(value)
          if isinstance(value, str) and len(str_value) > limit_str:
            str_value = str_value[:limit_str]
          lst_data[-1] = lst_data[-1] + str_value

        if ki < (len(dct) - 1):
          lst_data[-1] = lst_data[-1] + ','
      return

    deep_parse(dct=d, ind=0)

    displaybuff = "{\n"
    for itm in lst_data:
      displaybuff += '  ' + itm + '\n'
    displaybuff += "}"

    if display_callback is not None:
      displaybuff = "Dict pretty formatter:\n" + displaybuff
      display_callback(displaybuff)
    if as_str:
      return displaybuff
    else:
      return lst_data

  def camel_to_snake(self, s):
    import re
    if s.isupper():
      result = s.lower()
    else:
      s = re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()
      s = s.replace('__', '_')
      result = s
    return result


class GenericSession(object):
  default_config = {
      "CONFIG_CHANNEL": {
          "TOPIC": "lummetry/{}/config"
      },
      "CTRL_CHANNEL": {
          "TOPIC": "lummetry/ctrl"
      },
      "NOTIF_CHANNEL": {
          "TOPIC": "lummetry/notif"
      },
      "PAYLOADS_CHANNEL": {
          "TOPIC": "lummetry/payloads"
      },
      "QOS": 0
  }

  def __init__(self, *, host, port, user, pwd, name='pySDK', config={}, log=None, on_notification=None, on_heartbeat=None, silent=False, **kwargs) -> None:
    if log is None:
      log = Logger(
          lib_name='EE',
          base_folder='.',
          app_folder='_local_cache',
          config_file='config_startup.txt',
          max_lines=3000,
          TF_KERAS=False
      )

    super(GenericSession, self).__init__()

    self.silent = silent

    # maybe read config from file?
    self._config = {**self.default_config, **config}
    self.log = log
    self.name = name

    self._online_boxes = {}

    self._fill_config(host, port, user, pwd, name)

    self.custom_on_heartbeat = on_heartbeat
    self.custom_on_notification = on_notification

    self.on_payload = self._on_payload_default
    self.on_heartbeat = self._on_heartbeat_default
    self.on_notification = self._on_notification_default

    self.payload_instance_callbacks = []
    self.notification_instance_callbacks = []

    self.payload_pipeline_callbacks = []
    self.notification_pipeline_callbacks = []
    self.heartbeat_pipeline_callbacks = []

    self.formatter_wrapper = IOFormatterManager(log)

    return

  @property
  def server(self):
    return self._config[comm_ct.HOST]

  def P(self, *args, **kwargs):
    if not self.silent:
      self.log.P(*args, **kwargs)

  def _fill_config(self, host, port, user, pwd, name):
    if self._config.get(comm_ct.SB_ID, None) is None:
      self._config[comm_ct.SB_ID] = name

    if self._config.get(comm_ct.USER, None) is None:
      self._config[comm_ct.USER] = user

    if self._config.get(comm_ct.PASS, None) is None:
      self._config[comm_ct.PASS] = pwd

    if self._config.get(comm_ct.HOST, None) is None:
      self._config[comm_ct.HOST] = host

    if self._config.get(comm_ct.PORT, None) is None:
      self._config[comm_ct.PORT] = port
    return

  def connect(self) -> None:
    raise NotImplementedError

  def _parse_message(self, dict_msg: dict):
    formatter = self.formatter_wrapper \
        .get_required_formatter_from_payload(dict_msg)
    if formatter is not None:
      dict_msg = formatter.decode_output(dict_msg)
    return dict_msg

  def _on_heartbeat_default(self, dict_msg: dict):
    msg_eeid = dict_msg['EE_ID']
    msg_active_configs = dict_msg['CONFIG_STREAMS']

    # default action
    # TODO: print stuff
    self.P("Received hb from: {}".format(msg_eeid))
    self._online_boxes[msg_eeid] = {
        config['NAME']: config for config in msg_active_configs}

    # call the pipeline defined callbacks, if any
    for pipeline, callback in self.heartbeat_pipeline_callbacks:
      if msg_eeid == pipeline.e2id:
        callback(pipeline, dict_msg)

    # call the custom callback, if defined
    if self.custom_on_heartbeat is not None:
      self.custom_on_heartbeat(self, dict_msg)

    return

  def _on_notification_default(self, dict_msg: dict):
    msg_eeid = dict_msg['EE_ID']
    msg_stream = dict_msg.get('STREAM_NAME', None)
    notification_type = dict_msg.get("NOTIFICATION_TYPE")
    notification = dict_msg.get("NOTIFICATION")

    # call the pipeline defined callbacks, if any
    for pipeline, callback in self.notification_pipeline_callbacks:
      if msg_eeid == pipeline.e2id and msg_stream == pipeline.name:
        callback(pipeline, dict_msg)

    # call the custom callback, if defined
    if self.custom_on_notification is not None:
      self.custom_on_notification(self, dict_msg)

    # call default action on notif
    # TODO: maybe print stuff
    color = None
    if notification_type != "NORMAL":
      color = 'r'
    self.P("Received notification {} from <{}/{}>: {}".format(notification_type,
           msg_eeid, msg_stream, notification), color=color)

    return

  # TODO: maybe convert dict_msg to Payload object
  #       also maybe strip the dict from useless info for the user of the sdk
  #       Add try-except + sleep
  def _on_payload_default(self, dict_msg: dict) -> None:
    msg_stream = dict_msg.get('STREAM', None)
    msg_eeid = dict_msg['EE_ID']
    msg_signature = dict_msg.get('SIGNATURE', '').upper()
    msg_instance = dict_msg.get('INSTANCE_ID', None)
    msg_data = dict_msg

    for pipeline, callback in self.payload_pipeline_callbacks:
      if msg_eeid == pipeline.e2id and msg_stream == pipeline.name:
        callback(pipeline, msg_signature, msg_instance, msg_data)

    for pipeline, signature, instance, callback in self.payload_instance_callbacks:
      if msg_eeid == pipeline.e2id and msg_stream == pipeline.name and msg_signature == signature and msg_instance == instance:
        callback(pipeline, msg_data)
    return

  # TODO: add arguments after they are finally set in Pipeline
  def create_pipeline(self, *args, **kwargs) -> Pipeline:
    return Pipeline(self, self.log, *args, silent=self.silent, **kwargs)

  def _send_command_to_box(self, command, worker, payload):
    msg_to_send = {
        'EE_ID': worker,
        'SB_ID': worker,
        'ACTION': command,
        'PAYLOAD': payload,
        'INITIATOR_ID': self.name
    }

    self._send_payload(worker, msg_to_send)

  def remove_pipeline_callbacks(self, pipeline) -> None:
    instance_indexes = [i for i, t in enumerate(
        self.payload_instance_callbacks) if t[0] == pipeline][::-1]
    for i in instance_indexes:
      self.payload_instance_callbacks.pop(i)

    pipeline_index = [i for i, t in enumerate(
        self.payload_pipeline_callbacks) if t[0] == pipeline][0]
    self.payload_pipeline_callbacks.pop(pipeline_index)
    return

  def remove_instance_callback(self, pipeline, signature, instance_id):
    instance_index = None

    for i, (cb_pipeline, cb_signature, cb_instance_id, _) in enumerate(self.payload_instance_callbacks):
      if cb_pipeline == pipeline and cb_signature == signature and cb_instance_id == instance_id:
        instance_index = i
        break

    self.payload_instance_callbacks.pop(instance_index)
    return

  def send_command_update_pipeline(self, worker, stream_config):
    self._send_command_to_box('UPDATE_CONFIG', worker, stream_config)

  def send_command_delete_pipeline(self, worker, stream_name):
    self._send_command_to_box('ARCHIVE_CONFIG', worker, stream_name)

  def close(self):
    raise NotImplementedError

  def _send_payload(self, to, payload):
    raise NotImplementedError

  def get_active_nodes(self):
    return list(self._online_boxes.keys())

  def get_active_pipelines(self, e2id):
    return self._online_boxes.get(e2id, None)

  def attach_to_pipeline(self, e2id, pipeline_name, **kwargs) -> Pipeline:
    if e2id not in self._online_boxes:
      raise Exception("Unable to attach to pipeline. Node does not exist")

    if pipeline_name not in self._online_boxes[e2id]:
      raise Exception("Unable to attach to pipeline. Pipeline does not exist")

    pipeline_config = {
        k.lower(): v for k, v in self._online_boxes[e2id][pipeline_name].items()}
    data_source = pipeline_config['type']
    return Pipeline(self, self.log, e2id=e2id, config={}, data_source=data_source, create_pipeline=False, silent=self.silent, **pipeline_config, **kwargs)
