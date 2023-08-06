# -*- coding: utf-8 -*-
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
@author: Lummetry.AI - AID
@project: 
@description:
Created on Thu Jan 26 14:57:44 2023
"""

import os
from time import sleep, time

from PyE2 import Payload, Pipeline, Session, code_to_base64

worker_code = """
_result=None
skip = False
for _ in range(plugin.cfg_max_tries):
  num = plugin.np.random.randint(1, 10_000)
  for n in range(2,int(num**0.5)+1):
    if num % n == 0:
      skip=True
      break
    # endif
  # endfor
  if not skip:
    _result=num
    break
  # endif
# endfor
"""

master_code = """
_result=None
if plugin.int_cache['run_first_time'] == 0:
  # this is the first run, consider this the setup
  
  plugin.int_cache['run_first_time'] = 1

  worker_code = plugin.cfg_worker_code
  n_workers = plugin.cfg_n_workers
  
  plugin.obj_cache['lst_workers'] = plugin.deapi_get_wokers(n_workers)
  plugin.obj_cache['dct_workers'] = {}
  plugin.obj_cache['dct_worker_progress'] = {}
  plugin.P(plugin.obj_cache['lst_workers'])
  
  
  for worker in plugin.obj_cache['lst_workers']:
    plugin.obj_cache['dct_worker_progress'][worker] = []
    stream_name = plugin.cmdapi_start_simple_custom_pipeline(
      base64code=worker_code, 
      dest=worker,
      instance_config={
        'MAX_TRIES': plugin.cfg_max_tries, 
      }
    )
    plugin.obj_cache['dct_workers'][worker] = stream_name 
  # endfor
  
  plugin.obj_cache["start_time"] = plugin.datetime.now()
  # endfor
# endif
elif (plugin.datetime.now() - plugin.obj_cache["start_time"]).seconds > plugin.cfg_max_run_time:
  # stop the workers and stop this instance
  
  for box_id, stream_name in plugin.obj_cache['dct_workers'].items():
    plugin.cmdapi_archive_stream_on_other_box(box_id=box_id, stream_name=stream_name)
  plugin.cmdapi_archive_current_stream()
  _result = plugin.obj_cache['dct_worker_progress']
else:
  # here are the operations we are running periodically

  payload = plugin.dataapi_struct_data()
  if payload is not None:
    
    box = payload.get('EE_ID', payload.get('SB_ID'))
    stream = payload.get('STREAM_NAME')
    
    if (box, stream) in plugin.obj_cache['dct_workers'].items():
      num = payload.get('EXEC_RESULT', payload.get('EXEC_INFO'))
      if num is not None:
        plugin.obj_cache['dct_worker_progress'][box].append(num)
  # endif
# endif
"""


def instance_on_data(pipeline, data: Payload):
  print(data)
  return


def pipeline_on_data(pipeline, signature, instance, data: Payload):
  pass


dct_server = {
    'host': "jenkinsx.globalintelligence.ro",
    'port': 31083,
    'user': "coreaixp",
    'pwd': "s3cret-passw0rd"
}

e2id = 'stefan-box'
sess = Session(**dct_server, silent=True)
sess.connect()

listener_params = {k.upper(): v for k, v in dct_server.items()}
listener_params["PASS"] = listener_params["PWD"]
listener_params["TOPIC"] = "lummetry/payloads"

pipeline = sess.create_pipeline(
    e2id=e2id,
    name='test_dist_jobs',
    # data_source='Void',
    # config={},
    data_source='IotQueueListener',
    config={
        'STREAM_CONFIG_METADATA': listener_params,
        "RECONNECTABLE": True,
    },
    plugins=None,
    on_data=pipeline_on_data,
)

# now start a ciclic process
# pipeline.start_custom_plugin(
#     instance_id='inst01',
#     plain_code=worker_code,
#     params={
#       'MAX_TRIES': 10,
#       },
#     on_data=instance_on_data,
#     process_delay=1
# )

pipeline.start_custom_plugin(
    instance_id='inst02',
    plain_code=master_code,
    params={
      'MAX_TRIES': 10,
      'MAX_RUN_TIME': 60,
      'N_WORKERS': 2,
      'WORKER_CODE': code_to_base64(worker_code)
      },
    on_data=instance_on_data,
    process_delay=0.2
)



try:
  while True:
    sleep(0.1)
except KeyboardInterrupt:
  pipeline.P("CTRL+C detected. Closing example..", color='r')


pipeline.close()
sess.close()
