---
title: LLaMA-Factory+Ollama：本地部署大模型流程详解
date: '2024-10-13'
summary: 第一次搭建属于自己的本地对话大模型，挺有意思。
tags:
  - 笔记
share: false
---

一共分为两个步骤，**利用LLaMA-Factory训练(微调)模型** 和 **利用Ollama部署模型**，两个步骤是相互独立的，可以根据需要阅读对应部分。

# LLaMA-Factory训练模型

## LLaMA-Factory 安装

**这部分在LLaMA-Factory的文档里已有详细介绍，可直接参考:** https://llamafactory.readthedocs.io/zh-cn/latest/#

在安装 LLaMA-Factory 之前，确保安装了下列依赖:

运行以下指令以安装 LLaMA-Factory 及其依赖:

```bash
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"
```

如果出现环境冲突，请尝试使用 `pip install --no-deps -e .` 解决。

## LLaMA-Factory 校验

完成安装后，可以通过使用 `llamafactory-cli version` 来快速校验安装是否成功。

如果能成功看到类似 **"Welcome to LLaMA Factory, version ······"** 的字样，说明安装成功。

## HuggingFace镜像

由于无法访问HuggingFace，容易出现 **OSError: We couldn't connect to 'https://huggingface.co' to load this file.** 类似的报错(如果在WebUI上看到的就是 **"训练错误"** 的字样)，所以需要在命令行输入以下指令后再进行接下来的步骤：

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

## WebUI

LLaMA-Factory 支持通过 WebUI 零代码微调大语言模型。 在完成安装后，通过以下指令进入 WebUI:

```bash
llamafactory-cli webui
```

**WebUI 主要分为四个界面：训练、评估与预测、对话、导出。**

## 训练

![image-20241010201410184](image-20241010201410184.png)

在开始训练模型之前，需要指定的参数有：

1. 模型名称及路径
2. 训练阶段
3. 微调方法
4. 训练数据集
5. 学习率、训练轮数等训练参数
6. 微调参数等其他参数
7. 输出目录及配置路径

比如说，我选择的就是Llama-3.1-8B的中文对话模型，数据集也选择的是alpaca的中文数据集。

**随后，可以点击 `开始` 按钮开始训练模型。**

**若使用CPU训练可能会报Warning，忽略即可**

![image-20241011094129601](image-20241011094129601.png)

## 评估预测与对话

模型训练完毕后，通过在评估与预测界面通过指定 **模型** 及 **适配器** 的路径在指定数据集上进行评估。

也可以通过在对话界面指定 **模型**、 **适配器** 及 **推理引擎** 后输入对话内容与模型进行对话观察效果。

## 导出

在导出界面通过指定 **模型**、 **适配器**、 **分块大小**、 **导出量化等级及校准数据集**、 **导出设备**、 **导出目录** 等参数后，**点击 `导出` 按钮导出模型。**

**(如果需要部署到Ollama上，请一定记得把模型导出)**

## 示例：微调中文对话大模型

### 使用alpaca_zh_demo数据集微调Llama-3-8B-Chinese-Chat模型

**训练过程的Loss曲线如下：**

![training_loss](training_loss.png)

**导出模型：**

![image-20241013090539536](image-20241013090539536.png)

**利用模型进行对话：**

![image-20241013091037404](image-20241013091037404.png)

### 使用自定义的custom_chinese_dataset数据集微调模型

**自定义的数据集需要添加到data文件夹中，并在data_info.json中添加相应的内容：**

![image-20241013091259201](image-20241013091259201.png)

![image-20241013091305972](image-20241013091305972.png)

**保存之后，就能在数据集选项中看到自定义数据集了。**

![image-20241012234348318](image-20241012234348318.png)

**测试微调后的对话效果：**

![image-20241013151000341](image-20241013151000341.png)

# Ollama部署模型

**Ollama安装完成后，可以将模型部署在本地。**

### 部署模型库中的模型

**首先下载Ollama：**

![image-20241013091941292](image-20241013091941292.png)

**安装完成后，即可通过命令直接下载使用模型库中的模型，这里以llama3.1为例:**

```bash
ollama run llama3.1
```

![image-20241013092846274](image-20241013092846274.png)

**输入/?可以调出提示：**

![image-20241013093004760](image-20241013093004760.png)

### 部署自定义模型

由于**通过LlaMA-Factory导出的模型与Ollama所需格式有区别**，需要**借助Llama.cpp的代码进行转换**。

**仓库地址：**https://github.com/ggerganov/llama.cpp

**git clone仓库之后，下载相关依赖：**

```bash
pip install -r requirements.txt
```

**接着就可以进行转换了：**

```bash
python convert_hf_to_gguf.py /home/yyx/LLaMA-Factory/saves/Llama-3-8B-Chinese-Chat/output-100 \
--outfile /home/yyx/output-100.gguf \
--outtype q8_0
```

**以下图的模型为例，其名称是output-100：**

![image-20241013125435028](image-20241013125435028.png)

**运行代码后会把safetensors格式转换为gguf格式，名称是output-100.gguf。**

**接下来创建Modelfile，用于将模型导入Ollama中：**

```bash
FROM /path/to/your_model.gguf
```

**(先创建Modelfile.txt，在文档中填入内容，保存后把后缀.txt去掉即可，记得把/path/to/your_model.gguf替换为模型的实际路径)**

**在Ollama中创建相应的模型：**

```bash
ollama create model_name -f /path/to/Modelfile
```

**查看Ollama中所有的本地模型：**

```bash
ollama list
```

![image-20241013174005062](image-20241013174005062.png)

**在Ollama中运行模型进行对话：**

```bash
ollama run model_name
```

**至此，就已实现了在本地部署自定义微调模型，当然也可以利用docker运行webui，进行更好地可视化。**

**Tips：如果你发现你的模型在回复时逻辑不那么通顺流利，类似下图这样，说明你的微调似乎不够成功 :)**

![image-20241013161918357](image-20241013161918357.png)

**Enjoy it ~**