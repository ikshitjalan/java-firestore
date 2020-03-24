# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp
import synthtool.languages.java as java

AUTOSYNTH_MULTIPLE_COMMITS = True

gapic = gcp.GAPICGenerator()

protobuf_header = "// Generated by the protocol buffer compiler.  DO NOT EDIT!"
# License header
license_header = """/*
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
"""
bad_license_header = """/\\*
 \\* Copyright 2018 Google LLC
 \\*
 \\* Licensed under the Apache License, Version 2.0 \\(the "License"\\); you may not use this file except
 \\* in compliance with the License. You may obtain a copy of the License at
 \\*
 \\* http://www.apache.org/licenses/LICENSE-2.0
 \\*
 \\* Unless required by applicable law or agreed to in writing, software distributed under the License
 \\* is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 \\* or implied. See the License for the specific language governing permissions and limitations under
 \\* the License.
 \\*/
"""


def generate_client(service, version, config_path, package, include_gapic=True):
  library = gapic.java_library(
      service=service,
      version=version,
      config_path=config_path,
      artman_output_name='')

  s.replace(
      library / f'proto-google-cloud-{service}-{version}/src/**/*.java',
      protobuf_header,
      f'{license_header}{protobuf_header}'
  )
  s.replace(
      library / f'grpc-google-cloud-{service}-{version}/src/**/*.java',
      bad_license_header,
      license_header
  )
  s.replace(
      library / f'proto-google-cloud-{service}-{version}/src/**/*.java',
      bad_license_header,
      license_header
  )
  s.replace(
      library / f'grpc-google-cloud-{service}-{version}/src/**/*.java',
      f'package {package};',
      f'{license_header}package {package};'
  )

  s.copy(library / f'grpc-google-cloud-{service}-{version}/src', f'grpc-google-cloud-{service}-{version}/src')
  s.copy(library / f'proto-google-cloud-{service}-{version}/src', f'proto-google-cloud-{service}-{version}/src')
  java.format_code(f'grpc-google-cloud-{service}-{version}/src')
  java.format_code(f'proto-google-cloud-{service}-{version}/src')

  if include_gapic:
    s.copy(library / f'gapic-google-cloud-{service}-{version}/src', 'google-cloud-firestore/src')
    java.format_code(f'google-cloud-firestore/src')

  return library

admin_v1 = generate_client(
    service='firestore-admin',
    version='v1',
    config_path='/google/firestore/admin/artman_firestore_v1.yaml',
    package='com.google.firestore.admin.v1',
    include_gapic=True
)

firestore_v1 = generate_client(
    service='firestore',
    version='v1',
    config_path='/google/firestore/artman_firestore_v1.yaml',
    package='com.google.firestore.v1',
    include_gapic=True
)

firestore_v1beta1 = generate_client(
    service='firestore',
    version='v1beta1',
    config_path='/google/firestore/artman_firestore.yaml',
    package='com.google.firestore.v1beta1',
    include_gapic=False
)

java.common_templates(excludes=[
    'README.md',
    # firestore uses a different project for its integration tests
    # due to the default project running datastore
    '.kokoro/presubmit/integration.cfg'
])
