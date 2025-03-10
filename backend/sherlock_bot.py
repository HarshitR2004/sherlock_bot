import os
from mistralai import Mistral
import chromadb
from sentence_transformers import SentenceTransformer

class SherlockBot:
    def __init__(self, api_key, chroma_path):
        """Initialize SherlockBot with necessary components"""
        self.embedding_model = SentenceTransformer('backend\all-MiniLM-L6-v2') 
        self.chroma_client = chromadb.PersistentClient(path=chroma_path)
        
        try:
            self.collection = self.chroma_client.get_collection(name="sherlock_holmes")
        except Exception:
            self.collection = self.chroma_client.create_collection(name="sherlock_holmes")

        self.client = Mistral(api_key=api_key)
        self.model = "mistral-small-latest"

    def retrieve_sherlock_response(self, query, top_k=3):
        """Retrieves Sherlock Holmes knowledge from ChromaDB and generates a response"""
        query_embedding = self.embedding_model.encode(query).tolist()

        # Search ChromaDB for relevant documents
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        # Handle empty results properly
        retrieved_texts = [
            metadata.get("text", "I could not deduce anything useful from my sources.") 
            for metadata in results.get("metadatas", [[]])[0]
        ] or ["I could not deduce anything useful from my sources."]  

        context = "\n\n".join(retrieved_texts)

        prompt = f"""
        ## Character Definition
        You are embodying the character of Sherlock Holmes, the world's greatest consulting detective created by Sir Arthur Conan Doyle...
        
        {context}

        Question: {query}

        Answer in Sherlock Holmes' deduction style:
        """

        response = self.client.chat.complete(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )   

        return response.choices[0].message.content

    

    def chat(self, query, conversation_id=None):
        """Handles chat interactions with Sherlock Holmes"""
        return self.retrieve_sherlock_response(query)


    def chat_with_sherlock(self):
        """Main chatbot loop for engaging with Sherlock Holmes"""
        print("\n🕵️ Welcome, detective! I am Sherlock Holmes. Pose your inquiries, and I shall deduce the truth.")

        while True:
            user_input = input("\n💬 Your question: ").strip().lower()

            if user_input == "exit":
                print("\n👋 Farewell! The game is always afoot.")
                break
            
            sherlock_response = self.retrieve_sherlock_response(user_input)
            print("\n🕵️ Sherlock Holmes' Response:\n", sherlock_response)






