先clone仓库或pip安装：

```bash
pip install hcgf
```

需要的依赖在`requirements.txt`中，通过下面命令安装：

```
pip install -r requirements.txt
```

注意：不支持PyTorch2.0，历史版本请参考下面链接安装：

https://pytorch.org/get-started/previous-versions/



## 微调

### 准备数据

每一行一个json，必须包含`prompt`和`completion`两个字段。示例如下：

```bash
{"prompt": "你是谁？\n", "completion": "不告诉你。"}
```


### 正常微调

至少需要一张16G显存的卡。如果不指定显卡，默认为`cuda`。

```python
#===== 微调 =====#
import hcgf
gl = hcgf.GlmLora("THUDM/chatglm-6b", device="cuda:0")
gl.load_data("/path/to/data.json").tune()

#===== 推理 =====#
gl = hcgf.GlmLora("THUDM/chatglm-6b", device="cuda:0")
gl.load_pretrained("/path/to/lora_pt").eval()
gl.chat("你是谁?")

#===== 切换模式 =====#
gl = hcgf.GlmLora("THUDM/chatglm-6b", device="cuda:0")
gl.load_data("/path/to/data.json").tune()
# 切换到推理模式
gl.eval()
gl.chat("你是谁？")
# 切换回微调模式，还是用原来的数据重新跑
gl.tune()
# 如果有新的数据集，参考上面的写法，先加载数据
gl.load_data("/path/to/new_data.json").tune()
```


### 8bit微调

至少需要一张12G显存的卡。不指定device。

需要安装依赖: `bitsandbytes`

只需要初始化时改一下即可，其他操作和上面正常微调一样。

```python
gl = hcgf.GlmLora("THUDM/chatglm-6b", load_in_8bit=True)
```

### 继续微调

先加载之前的`pt`文件，然后加载数据微调。

```python
gl.load_pretrained("/path/to/lora_pt").load_data("/path/to/new_data").tune()
```

### 参数说明

主要有三个方法的参数，有值的表示默认值。

```python
load_data(
    data_path: str, 
    max_seq_len: int = 512, # 句子最大长度，超过会截断
)
tune(
    batch_size: int = 1,
    lr: float = 2e-4,
    num_epochs: int = 10,
    warmup_steps: Optional[int] = None,     # 为None时会用第一个Epoch进行warmup
    accumulate_steps: Optional[int] = 32,
    out_dir: str = "./output/",
    print_every: int = 10,                  # 每隔多少个Step打印一次输出（Step、Loss、LearningRate）
)
chat(
    inp: str, 
    history: List[Tuple[str, str]] = None,  # (问，答)Pair对
    max_len: int = 512,                     # 上下文的最大长度，超过就不生成了
    stop: List[str] = []                    # 停止文本，可以是标点、特定词或句子等
)

```

### 配置

有几个影响显存的参数可以配置：`max_seq_len`，`batch_size`。


```python
(
gl
.load_data("./data/chatgpt_finetune_faq.json", max_seq_len=128)
.tune(batch_size=1)
)

```

不同配置 `8bit` 资源占用：

| max_seq_len | batch_size | memory |
| ----------- | ---------- | ------ |
| `64`        | 1          | 11G    |
| `128`       | 1          | 12G    |
| `512`       | 1          | 22G    |
| 128         | `2`        | 15G    |
| 128         | `4`        | 21G    |

不同配置正常资源占用：

| max_seq_len | batch_size | memory |
| ----------- | ---------- | ------ |
| `64`        | 1          | 15G    |
| `128`       | 1          | 16G    |
| `512`       | 1          | 30G    |
| 128         | `2`        | 19G    |
| 128         | `4`        | 25G    |


## RM

使用小模型（如BERT等）训练。

### 训练

### 准备数据

需要pair对数据，计算logits过程和普通预训练模型一样（一个Batch多个pair对）；计算loss时属于同一个pair对的logits放一块算。

推理时直接用logits就行。

### 推理


## 测试

```bash
# 全部测试
python -m pytest
# 测试训练和推理，比较慢
python -m pytest -s -m slow
# 测试其他的
python -m pytest -m "not slow"
```