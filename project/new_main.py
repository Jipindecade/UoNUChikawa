from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import numpy as np

class SimliarityBasedTalk:
    def __init__(self):
        self.embed_model = self.load_embed()
        self.text_list = [
            "Hi",
            "Hello",
            "What is my name?",
            "How are you",
            "what can you do",
            "What are stocks and bonds"
        ]
        self.data = {
            "Hi": "Hello, [NAME]",
            "Hello": "Hello, [NAME]",
            "What is my name?": "Your name is [NAME]",
            "How are you": "Fine thank you",
            "what can you do": "I can help you to generate some poet, book a ticket, answer some question about history and science",
            "What are stocks and bonds":"Stocks and bonds are two types of financial instruments that are central to the financial markets and are used by corporations and governments to raise capital.",
        }
        self.simple_db = self.make_tmp_vec_db()


    # load embedding model
    def load_embed(self):
        embeddings = HuggingFaceEmbeddings(model_name='./bert_similarity_english')
        return embeddings

    def embed_text(self, text):
        """ transpose word to vector """
        word_vec = self.embed_model.embed_query(text)
        return word_vec

    def cosine_similarity(self, vec1, vec2):
        """ compute cosine similarity between two vectors """
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def make_tmp_vec_db(self):
        simple_db = []
        for text in self.text_list:
            text_vec = self.embed_text(text)
            simple_db.append(text_vec)
        return simple_db

    def find_top_similar_texts(self, input_text, top_n=1):
        """ return top n similar texts """
        input_vec = self.embed_text(input_text)
        similarities = []
        idx = 0
        for text_vec in self.simple_db:
            similarity = self.cosine_similarity(input_vec, text_vec)
            similarities.append((idx, similarity))
            idx += 1

        # sort and return top n similar texts
        similarities.sort(key=lambda x: x[1], reverse=True)
        print(similarities)
        return similarities[:top_n]

    def answer(self, name, input):
        # find the most similar text
        top_similar_texts = ai.find_top_similar_texts(input_text)

        # return result
        for text, similarity in top_similar_texts:
            return self.data[self.text_list[text]].replace('[NAME]', name)
# # load embedding model
# embed_model = HuggingFaceEmbeddings(model_name="iic/nlp_bert_sentence-similarity_english-base")
#
# # get the word vector
# embeddings = embed_model.embed_query("hello world")
# print(len(embeddings))
# print(embeddings)
if __name__ == '__main__':
    ai = SimliarityBasedTalk()



    name = input("pleas input your name:")
    while True:
        # input user answer
        input_text = input("USER:")
        answer = ai.answer(name, input_text)
        print("AI:", answer)

