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

from ..utils.code_exec import code_to_base64


class Pipeline(object):
  def __init__(self, session, log, *, e2id, name, data_source, config, plugins, on_data, silent=False, on_notification=None, **kwargs) -> None:
    self.log = log
    self.session = session
    self.e2id = e2id
    self.name = name
    self.data_source = data_source
    self.config = config
    self.plugins = plugins
    self.on_data = on_data
    self.on_notification = on_notification

    self.payload = {}

    self.silent = silent

    self._create_new_pipeline_on_box(**kwargs)
    return

  def _create_new_pipeline_on_box(self, *, create_pipeline=True, **kwargs):
    # beautify the fields that enter in the config file
    kwargs = {k.upper(): v for k, v in kwargs.items()}

    self.payload = {
        'NAME': self.name,
        'SESSION_ID': self.name,
        'DEFAULT_PLUGIN': False,
        'PLUGINS': [] if self.plugins is None else self.plugins,
        'TYPE': self.data_source,
        **self.config,
        **kwargs
    }

    if create_pipeline:
      self.session.send_command_update_pipeline(
          worker=self.e2id,
          stream_config=self.payload
      )

    if self.on_data is not None:
      self._add_payload_pipeline_callback_to_session(self.on_data)
    if self.on_notification is not None:
      self._add_notification_pipeline_callback_to_session(self.on_notification)
    return

  def _add_payload_instance_callback_to_session(self, signature, instance, callback):
    self.session.payload_instance_callbacks.append(
        (self, signature, instance, callback))

  def _add_notification_instance_callback_to_session(self, signature, instance, callback):
    self.session.notification_instance_callbacks.append(
        (self, signature, instance, callback))

  def _add_payload_pipeline_callback_to_session(self, callback):
    self.session.payload_pipeline_callbacks.append((self, callback))

  def _add_notification_pipeline_callback_to_session(self, callback):
    self.session.notification_pipeline_callbacks.append((self, callback))

  # TODO: maybe wait for a confirmation?
  def start_plugin_instance(self, *, signature, instance_id, params, on_data, on_notification=None, **kwargs):
    plugins = self.payload['PLUGINS']
    found_plugin_signature = False
    to_update_plugin = {
        'INSTANCES': [],
        'SIGNATURE': signature
    }
    # beautify the fields that enter in the config file
    kwargs = {k.upper(): v for k, v in kwargs.items()}

    to_add_instance = {
        'INSTANCE_ID': instance_id,
        **params,
        **kwargs
    }

    for plugin in plugins:
      if plugin['SIGNATURE'] == signature:
        found_plugin_signature = True
        to_update_plugin = plugin
        break

    if not found_plugin_signature:
      plugins.append(to_update_plugin)

    for instance in to_update_plugin['INSTANCES']:
      if instance['INSTANCE_ID'] == instance_id:
        raise Exception(
            "plugin {} with instance {} already exists".format(signature, instance_id))

    to_update_plugin['INSTANCES'].append(to_add_instance)

    self.session.send_command_update_pipeline(
        worker=self.e2id,
        stream_config=self.payload
    )

    self._add_payload_instance_callback_to_session(
        signature, instance_id, on_data)
    if on_notification is not None:
      self._add_notification_instance_callback_to_session(
          signature, instance_id, on_notification)
    self.P("Starting plugin {}:{} with params {}".format(
        signature, instance_id, params))
    return "##".join([self.e2id, self.name, signature, instance_id])

  def stop_plugin_instance(self, signature, instance_id=None, /):
    if instance_id is None:
      try:
        eeid, pipeline_name, signature, instance_id = tuple(
            signature.split('##'))
      except:
        raise ("Unknown format of instance_id. Please provide the return value of a 'start_plugin_instance' call")

      if self.e2id != eeid:
        raise ("Sending a command for a pipeline that was started by another box")

      if self.name != pipeline_name:
        raise ("Sending a command for a pipeline that was started by another instance")
    plugins = self.payload['PLUGINS']
    to_remove_instance_index = None
    to_update_plugin_index = None

    for i, plugin in enumerate(plugins):
      if plugin['SIGNATURE'] == signature:
        to_update_plugin_index = i
        break

    if to_update_plugin_index is None:
      return

    for i, instance in enumerate(plugins[to_update_plugin_index]['INSTANCES']):
      if instance['INSTANCE_ID'] == instance_id:
        to_remove_instance_index = i
        break

    if to_remove_instance_index is None:
      return

    plugins[to_update_plugin_index]['INSTANCES'].pop(to_remove_instance_index)

    if len(plugins[to_update_plugin_index]['INSTANCES']) == 0:
      self.payload['PLUGINS'].pop(to_update_plugin_index)

    self.session.send_command_update_pipeline(
        worker=self.e2id,
        stream_config=self.payload
    )
    self.session.remove_instance_callback(self, signature, instance_id)

    return

  def start_custom_plugin(self, *, instance_id, plain_code: str = None, plain_code_path: str = None, params, on_data, on_notification=None, **kwargs):
    def custom_exec_on_data(self, data):
      exec_data = None
      if "SB_IMPLEMENTATION" in data or "EE_FORMATTER" in data:
        exec_data = data.get('EXEC_RESULT', data.get('EXEC_INFO'))
        exec_error = data.get('EXEC_ERRORS', 'no keyword error')
      else:
        try:
          exec_data = data['specificValue']['exec_result']
        except Exception as e:
          self.P(e, color='r')
          self.P(data, color='r')
        exec_error = data['specificValue']['exec_errors']

      if exec_error is not None:
        self.P("Error received from <CUSTOM_EXEC_01:{}>: {}".format(
            instance_id, exec_error), color="r")
      if exec_data is not None:
        on_data(self, exec_data)
      return

    if plain_code is None and plain_code_path is None:
      raise Exception(
          "Need to specify at least one of the following: plain_code, plain_code_path")

    if plain_code is not None and plain_code_path is not None:
      raise Exception(
          "Need to specify at most one of the following: plain_code, plain_code_path")

    if plain_code is None:
      with open(plain_code_path, "r") as fd:
        plain_code = "".join(fd.readlines())

    b64code = code_to_base64(plain_code)
    return self.start_plugin_instance(
        signature='CUSTOM_EXEC_01',
        instance_id=instance_id,
        params={
            'CODE': b64code,
            **params
        },
        on_data=custom_exec_on_data,
        on_notification=on_notification,
        **kwargs
    )

  def stop_custom_instance(self, instance_id):
    self.stop_plugin_instance('CUSTOM_EXEC_01', instance_id)

  def wait_exec(self, *, plain_code: str = None, plain_code_path: str = None, params={}):
    if plain_code is None and plain_code_path is None:
      raise Exception(
          "Need to specify at least one of the following: plain_code, plain_code_path")

    if plain_code is None:
      with open(plain_code_path, "r") as fd:
        plain_code = "".join(fd.readlines())

    finished = False
    result = None
    error = None

    def on_data(pipeline, data):
      nonlocal finished
      nonlocal result
      nonlocal error

      if 'rest_execution_result' in data['specificValue'] and 'rest_execution_error' in data['specificValue']:
        result = data['specificValue']['rest_execution_result']
        error = data['specificValue']['rest_execution_error']
        finished = True
      return

    b64code = code_to_base64(plain_code)
    instance_id = self.name + "_rest_custom_exec_synchronous_0"
    params = {
        'REQUEST': {
            'DATA': {
                'CODE': b64code,
            },
            'TIMESTAMP': self.log.time_to_str()
        },
        'RESULT_KEY': 'REST_EXECUTION_RESULT',
        'ERROR_KEY': 'REST_EXECUTION_ERROR',
        **params
    }

    self.start_plugin_instance(
        signature='REST_CUSTOM_EXEC_01',
        instance_id=instance_id,
        params=params,
        on_data=on_data
    )
    while not finished:
      pass

    # stop the stream
    self.stop_plugin_instance('REST_CUSTOM_EXEC_01', instance_id)

    return result, error

  def close(self):
    # remove callbacks
    self.session.send_command_delete_pipeline(self.e2id, self.name)
    self.session.remove_pipeline_callbacks(self)

  def P(self, *args, **kwargs):
    if not self.silent:
      return self.log.P(*args, **kwargs)

  def attach_to_instance(self, signature, instance_id, on_data, on_notification=None):
    plugins = self.payload['PLUGINS']
    found_plugin_signature = False

    for plugin in plugins:
      if plugin['SIGNATURE'] == signature:
        found_plugin_signature = True
        break

    if not found_plugin_signature:
      raise Exception("Unable to attach to instance. Signature does not exist")

    for instance in plugin['INSTANCES']:
      if instance['INSTANCE_ID'] == instance_id:
        self._add_payload_instance_callback_to_session(
            signature, instance_id, on_data)
        if on_notification is not None:
          self._add_notification_instance_callback_to_session(
              signature, instance_id, on_notification)
        return "##".join([self.e2id, self.name, signature, instance_id])

    raise Exception("Unable to attach to instance. Instance does not exist")
