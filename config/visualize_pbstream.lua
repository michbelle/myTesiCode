-- Copyright 2018 The Cartographer Authors
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--      http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

-- include "backpack_2d.lua"
include "baseCartographer.lua"

POSE_GRAPH.constraint_builder.sampling_ratio = 0
POSE_GRAPH.global_sampling_ratio = 0
POSE_GRAPH.optimize_every_n_nodes = 0

return options
