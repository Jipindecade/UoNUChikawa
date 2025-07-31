from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import pandas as pd
# from transformers import AutoModelForCausalLM, AutoTokenizer

class VectorDB:
    def __init__(self):
        self.vec_database = self.get_vector_db()
        self.data = pd.read_csv("./DB.csv", encoding="utf-8")
        self.data = self.data.drop_duplicates()
        self.QA_dict = dict(zip(self.data["Question"].tolist(), self.data["Answer"].tolist()))
    # 保存
    def save_vector_store(self, textChunks, embeddings):
        db = FAISS.from_texts(textChunks, embeddings)
        db.save_local('faiss_vec')

    def make_db(self):
        q_list = self.data["Question"].tolist()
        self.save_vector_store(q_list, self.load_embed())

    # 加载
    def load_vector_store(self, embeddings):
        return FAISS.load_local('faiss_vec', embeddings, allow_dangerous_deserialization=True)


    # 加载embedding模型
    def load_embed(self):
        embeddings = HuggingFaceEmbeddings(model_name='./bert_similarity_english')
        return embeddings


    # 加载数据集
    def load_data(self):
        return self.data["Question"].tolist()

    # 获取向量数据库
    def get_vector_db(self):
        embeddings = self.load_embed()
        vector_store = self.load_vector_store(embeddings)
        return vector_store

    def match_question(self, question, name):
        similarity = self.vec_database.similarity_search_with_score(question)
        score = similarity[0][1]
        print(score)
        content = similarity[0][0].page_content
        try:
            if score<33:
                answer = self.QA_dict[content].replace("[NAME]", name)
                print(answer)
            else:
                answer = ""
        except:
            answer = ""
        return answer

class SmallAI:
    def __init__(self):
        # checkpoint = "HuggingFaceTB/SmolLM2-360M-Instruct"
        # device = "cpu"  # for GPU usage or "cpu" for CPU usage
        # self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        # for multiple GPUs install accelerate and do `model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto")`
        # # self.model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)
        self.vec = VectorDB()

    def answer(self, question, name, messages_history):
        answer_result = self.vec.match_question(question, name)
        if answer_result != "":
            pass
        else:
            answer_result = "Data Base has no such answer!"
            # # messages_history.append({"role": "user", "content": question})
            # messages_history = [{"role": "user", "content": question}]
            # input_text = self.tokenizer.apply_chat_template(messages_history, tokenize=False)
            # # print(input_text)
            # inputs = self.tokenizer.encode(input_text, return_tensors="pt").to("cpu")
            # outputs = self.model.generate(inputs, max_new_tokens=100, temperature=0.2, top_p=0.9, do_sample=True)
            # answer_result = (
            #     self.tokenizer.decode(outputs[0]).replace(input_text, "").replace("<|im_start|>assistant\n", "").replace(
            #         "<|im_end|>", ""))
        messages_history.append({"role": "assistant", "content": answer_result})
        return answer_result, messages_history
# if __name__ == "__main__":
#     v = VectorDB()
#     v.make_db()