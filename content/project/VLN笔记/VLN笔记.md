---
title: 从零开始的VLN之旅
date: '2024-08-23'
summary: 视觉语言导航(Vision-and-Language Navigation)の笔记，记录看代码过程中的一些疑问。
tags:
  - 笔记
share: false
---

## VLN任务中的数据集 Room-to-Room (R2R) 

### 1. 数据集概览

- **发布年份**: 2018
- **创建者**: 由 Peter Anderson 等人发布，属于 VLN 任务的基准数据集之一。
- **应用场景**: 室内导航任务，要求智能体根据给定的自然语言指令从起点导航到终点。

### 2. 数据集结构

#### a. **自然语言指令**

- **描述**: 每个导航任务都有多条自然语言指令，描述了从起点到终点的导航路径。指令通常包含视觉描述、方向指示等信息。
- **数量**: 每个路径通常有3条不同的指令，整个数据集包含 21,567 条指令。
- **格式**: 文本字符串，通常是描述性的短语。例如：`"从房间的角落出发，经过红色的地毯，穿过门口，进入厨房，站在桌子旁边。"`

#### b. **导航路径**

- **描述**: 从起点到终点的最优路径，由一系列视点（viewpoints）构成。路径反映了指令所描述的移动轨迹。
- **数量**: 数据集中包含 7,189 条导航路径。
- **格式**: 每条路径由多个视点ID构成的列表。例如：`["34eVHcdvn", "a84UIG9p", "b89HJfvk"]`。

#### c. **视点图像**

- **描述**: R2R 使用 Matterport3D 环境中的视点图像。这些图像覆盖了场景中的 360 度全景视角。
- **格式**: 每个视点有 36 张图像，视角分别覆盖水平360度和垂直90度。

#### d. **视点连接关系**

- **描述**: 每个视点之间的可达性（connectivity），即视点间是否存在可直接导航的路径。R2R 利用 Matterport3D 提供的图结构表示视点之间的连接关系。

### 3. 数据分割

R2R 数据集分为三个部分，用于训练、验证和测试模型：

- **训练集（Training Set）**: 包含大部分路径和指令，供模型训练使用。
- **验证集（Validation Set）**:
  - **Seen**: 包含训练集中出现的场景，但指令不同。
  - **Unseen**: 包含在训练集中未出现的新场景，测试模型在未见过的环境中的泛化能力。
- **测试集（Test Set）**: 包含未公开的新场景，用于最终评估模型的性能。

### 4. 数据集输入输出

#### 输入数据格式

- **自然语言指令**: 输入给模型的自然语言描述，作为导航依据。
- **当前视点图像**: 智能体当前所在位置的视点图像，通常是全景图或某个视角的RGB图像。
- **视点连接关系**: 当前视点与邻近视点的可达性信息。
- **历史路径信息**（可选）: 智能体已走过的路径，用于更复杂的导航策略。

#### 输出数据格式

- **下一个视点ID**: 模型根据输入数据决定的下一步要移动到的视点。
- **导航路径**: 从起点到终点的完整路径，模型最终输出的导航决策。

### 5. 数据集应用

R2R 数据集被广泛用于以下任务：

- **训练和评估 VLN 模型**: 数据集为训练智能体在复杂环境中根据自然语言指令导航提供了标准化数据。
- **研究语言与视觉的对齐**: 模型需要理解并将自然语言指令与视觉输入对齐，以执行正确的导航动作。
- **评估泛化能力**: 特别是在未见过的场景中，测试智能体的泛化能力。

### 6. 评估指标

- **成功率（Success Rate, SR）**: 测试智能体是否成功到达目标视点。
- **路径长度（Path Length, PL）**: 智能体导航路径的总长度。
- **航向偏差（Trajectory Length, TL）**: 智能体实际行走的路径与最优路径之间的距离差异。
- **导航误差（Navigation Error, NE）**: 最终目标与预期目标之间的距离。

#### 1. 成功率 (Success Rate, SR)

- **描述**: 智能体是否成功到达目标视点。若智能体到达目标视点的距离小于某个阈值（通常是1米），则视为成功。
- **计算方式**:
  - 对每个导航任务，检查智能体是否在规定的步数内成功到达目标视点。
  - 计算成功任务数与总任务数的比例。
- **格式**:
  - **Success Rate** = Number of Successful TrialsTotal Number of Trials\frac{\text{Number of Successful Trials}}{\text{Total Number of Trials}}Total Number of TrialsNumber of Successful Trials
  - **示例**: `0.85`（表示85%的任务成功完成）

#### 2. 路径长度 (Path Length, PL)

- **描述**: 智能体实际走过的路径的总长度。
- **计算方式**:
  - 计算从起点到终点的实际行走距离。
- **格式**:
  - **Path Length** = Total Distance Traveled by the Agent
  - **示例**: `15.2 meters`

#### 3. 航向偏差 (Trajectory Length, TL)

- **描述**: 智能体实际行走的路径与最优路径之间的距离差异。衡量实际路径与理想路径之间的偏差。
- **计算方式**:
  - 计算智能体实际走过的路径与最短路径之间的距离差异。
- **格式**:
  - **Trajectory Length** = Distance of Actual Path - Distance of Optimal Path
  - **示例**: `5.4 meters`（表示实际路径比最优路径长5.4米）

#### 4. 导航误差 (Navigation Error, NE)

- **描述**: 智能体最终到达的位置与目标位置之间的距离误差。
- **计算方式**:
  - 在智能体到达目标视点后，计算其与目标视点之间的欧几里得距离。
- **格式**:
  - **Navigation Error** = Euclidean Distance between Final Position and Target Position
  - **示例**: `0.8 meters`（表示最终位置距离目标位置0.8米）

### 7. 重要性与挑战

R2R 数据集推动了 VLN 研究的发展，因为它要求模型具备将语言理解与视觉感知相结合的能力。在真实场景中（如机器人导航、智能助理等），这项能力至关重要。挑战在于如何让模型在未见过的场景中，准确执行复杂的指令，同时处理视觉和语言之间的模糊性和歧义性。

### 8. 典型模型

- **Speaker-Follower 模型**: 这是一个基准模型，它通过生成器（Speaker）生成指令，随后使用导航器（Follower）在环境中进行导航。
- **Reinforcement Learning (RL) 和 Imitation Learning (IL)**: 常用来训练模型，模拟智能体如何在环境中进行决策。

------

> At any time the simulator state can be returned by calling `getState`. The returned state contains a list of objects (one for each agent in the batch), with attributes as in the following example:

```javascript
[
  {
    "scanId" : "2t7WUuJeko7"  // Which building the agent is in
    "step" : 5,               // Number of frames since the last newEpisode() call
    "rgb" : <image>,          // 8 bit image (in BGR channel order), access with np.array(rgb, copy=False)
    "depth" : <image>,        // 16 bit single-channel image containing the pixel's distance in the z-direction from the camera center 
                              // (not the euclidean distance from the camera center), 0.25 mm per value (divide by 4000 to get meters). 
                              // A zero value denotes 'no reading'. Access with np.array(depth, copy=False)
    "location" : {            // The agent's current 3D location
        "viewpointId" : "1e6b606b44df4a6086c0f97e826d4d15",  // Viewpoint identifier
        "ix" : 5,                                            // Viewpoint index, used by simulator
        "x" : 3.59775996208,                                 // 3D position in world coordinates
        "y" : -0.837355971336,
        "z" : 1.68884003162,
        "rel_heading" : 0,                                   // Robot relative coords to this location
        "rel_elevation" : 0,
        "rel_distance" : 0
    }
    "heading" : 3.141592,     // Agent's current camera heading in radians
    "elevation" : 0,          // Agent's current camera elevation in radians
    "viewIndex" : 0,          // Index of the agent's current viewing angle [0-35] (only valid with discretized viewing angles)
                              // [0-11] is looking down, [12-23] is looking at horizon, is [24-35] looking up
    "navigableLocations": [   // List of viewpoints you can move to. Index 0 is always the current viewpoint, i.e. don't move.
        {                     // The remaining valid viewpoints are sorted by their angular distance from the image centre.
            "viewpointId" : "1e6b606b44df4a6086c0f97e826d4d15",  // Viewpoint identifier
            "ix" : 5,                                            // Viewpoint index, used by simulator
            "x" : 3.59775996208,                                 // 3D position in world coordinates
            "y" : -0.837355971336,
            "z" : 1.68884003162,
            "rel_heading" : 0,                                   // Robot relative coords to this location
            "rel_elevation" : 0,
            "rel_distance" : 0
        },
        {
            "viewpointId" : "1e3a672fa1d24d668866455162e5b58a",  // Viewpoint identifier
            "ix" : 14,                                           // Viewpoint index, used by simulator
            "x" : 4.03619003296,                                 // 3D position in world coordinates
            "y" : 1.11550998688,
            "z" : 1.65892004967,
            "rel_heading" : 0.220844170027,                      // Robot relative coords to this location
            "rel_elevation" : -0.0149478448723,
            "rel_distance" : 2.00169944763
        },
        {...}
    ]
  }
]
```

------

### 视图网格的结构

```python
heading = math.radians(30) * (view_index % 12)
elevation = math.radians(30) * (view_index // 12 - 1)
```

在视觉语言导航任务中，通常会将每个视点的视图划分为 36 个方向，具体结构如下：

- **水平角度（heading）**：将 360 度划分为 12 个视图，每个视图覆盖 30 度的水平视角。因此，`view_index % 12` 计算出的是水平方向的索引，对应的是水平视角上的12个方向（即 0°，30°，60°，...，330°）。
- **垂直角度（elevation）**：垂直方向上有 3 层：下方、水平和上方。`view_index // 12` 用来确定这 3 个层次，对应 `view_index` 的范围如下：
  - `view_index // 12 == 0`：表示下方的 12 个视图（`view_index` 取值 0 到 11）。
  - `view_index // 12 == 1`：表示水平的 12 个视图（`view_index` 取值 12 到 23）。
  - `view_index // 12 == 2`：表示上方的 12 个视图（`view_index` 取值 24 到 35）。

#### 举例说明

假设 `view_index` 是某个值，那么它的计算结果如下：

- 如果 `view_index` 是 5，`view_index // 12 == 0`，表示下方的第 5 个视图。
- 如果 `view_index` 是 17，`view_index // 12 == 1`，表示水平的第 5 个视图。
- 如果 `view_index` 是 29，`view_index // 12 == 2`，表示上方的第 5 个视图。

#### 关键点

- **水平角度（heading）** 由 `view_index % 12` 决定，这会给出 0 到 11 的值，对应 12 个水平角度。
- **垂直角度（elevation）** 由 `view_index // 12` 决定，这会给出 0，1，2 这三个值，对应下方、水平和上方三个层次。

因此，通过 `view_index // 12`，代码可以区分出视图的垂直层次，并结合 `view_index % 12` 的结果，智能体就能知道当前正在朝向哪个水平角度和垂直角度。这对于导航任务中的视觉感知和决策至关重要。