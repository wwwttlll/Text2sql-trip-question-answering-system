from typing import Optional, List, Any
from langchain.llms.base import LLM
from langchain import PromptTemplate, LLMChain
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from transformers import GenerationConfig
from safetensors import safe_open

class CodeLlamaSqlLLM(LLM):
    tokenizer: AutoTokenizer = None
    model: AutoModelForCausalLM = None

    def __init__(self, model_path: str ,device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        # model_path: CodeLlama模型路径
        # 从本地初始化模型
        super().__init__()
        print("正在从本地加载模型...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True, torch_dtype=torch.bfloat16, device_map="auto")
#         tensors = {}
#         with safe_open(f"{model_path}/model-00001-of-00002.safetensors", framework="pt", device='cpu') as f:
#             for k in f.keys():
#                 tensors[k] = f.get_tensor(k)
#         with safe_open(f"{model_path}/model-00002-of-00002.safetensors", framework="pt", device='cpu') as f:
#             for k in f.keys():
#                 tensors[k] = f.get_tensor(k)
#         self.model.load_state_dict(tensors, strict=False)
        
#         self.model.generation_config = GenerationConfig.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True, torch_dtype=torch.bfloat16, device_map="auto")
        # self.model = self.model.to(device)
        self.model = self.model.eval()
        print("完成本地模型的加载")

    def _call(self,prompt:str, stop: Optional[List[str]] = None, **kwargs: Any):
        # 重写调用函数
        template="I want you to act as a SQL terminal in front of an example database, you need only to return the sql command to me.Below is an instruction that describes a task, Write a response that appropriately completes the request.  ##Instruction: geo database contains tables such as province, scenic_area, specialty, hotel, and user. The province table has columns such as province. province is the primary key. The scenic_area table has columns such as view_id, view_name, level, latitude, longitude, province, city, county. view_id is the primary key. The specialty table has columns such as specialty_id, specialty_name, specialty_link, province_area, province, city, county. specialty_id is the primary key. The hotel table has columns such as hotel_id, hotel_name, hotel_ads, score, province, city, county. hotel_id is the primary key. The user table has columns such as user_name, user_id, password. user_id is the primary key.###Input: "
        inputs = self.tokenizer(template + prompt + " ###Output:", return_tensors="pt")
        output_ids = self.model.generate(**inputs, max_new_tokens=1024, pad_token_id=self.tokenizer.eos_token_id)
        response = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)[0]
        return response

    @property
    def _llm_type(self) -> str:
        return "codellama_sql_llm"

