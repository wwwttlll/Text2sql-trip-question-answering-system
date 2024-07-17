from typing import Union
from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from langchain import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains import LLMChain

import datetime
import json
import uvicorn
import zhipuai
import re

app = FastAPI()

from model import CodeLlamaSqlLLM
model_path = "/root/autodl-tmp/DB-GPT-Hub/dbgpt_hub/output/CodeLlama-7b-sql-sft"
llm = CodeLlamaSqlLLM(model_path)
# prompt_template = PromptTemplate(  
#     input_variables=["question"],
    
            
# )
# chain = LLMChain(llm=llm)
# memory = ConversationBufferMemory()

# prompt_template = PromptTemplate(  
#     template="I want you to act as a SQL terminal in front of an example database, you need only to return the sql command to me.Below is an instruction that describes a task, Write a response that appropriately completes the request.  ##Instruction: geo database contains tables such as province, scenic_area, specialty, hotel, and user. The province table has columns such as province. province is the primary key. The scenic_area table has columns such as view_id, view_name, level, latitude, longitude, province, city, county. view_id is the primary key. The specialty table has columns such as specialty_id, specialty_name, specialty_link, province_area, province, city, county. specialty_id is the primary key. The hotel table has columns such as hotel_id, hotel_name, hotel_ads, score, province, city, county. hotel_id is the primary key. The user table has columns such as user_name, user_id, password. user_id is the primary key."
# )

# conversation = ConversationChain(
#         llm=llm,
#         memory=memory,
#         prompt=prompt_template,
#         verbose=True  # 设置为 True 可以打印出链的中间状态
#     )


class QuestionRequest(BaseModel):
    question: str

@app.post("/api/sql")
async def generate_sql(request: Request):
    print(request)
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw,ensure_ascii=False)
    json_post_list = json.loads(json_post,strict=False)
    question = json_post_list.get("question")
    
    # sql_query = "SELECT view_name FROM scenic_area WHERE province = '河北省'"
    # print(question)
    result = llm(question)
    # print(result)
   
    print(result.split("###Output:")[1])
  
    response = {
        "sql": result.split("###Output:")[1]
    }
    # print(matches)
    return response

@app.post("/api/text")
async def create_item(request: Request):
    print("aaa")
    json_post_raw = await request.json()
    print("bbb")
    print(json_post_raw)
    json_post = json.dumps(json_post_raw,ensure_ascii=False)
    json_post_list = json.loads(json_post,strict=False)
    prompt = json_post_list.get("question")
    
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    zhipuai.api_key = "bd030d2acb22b8e5658cf965b39b2fbb.Xt4PbIeFXqDagEbp"
    response = zhipuai.model_api.invoke(
        model="chatglm_6b",
        prompt=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.7
    )
    RESPONSE = response['data']['choices'][0]['content'].replace("\\n", "\n")
    answer = {
        "sql": RESPONSE,
        "status": 200,
        "time": time
    }
    return answer




if __name__ == "__main__":
    uvicorn.run(app='main:app', host='0.0.0.0', port=8443, reload=False)