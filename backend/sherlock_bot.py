import chromadb
from openai import OpenAI
from sentence_transformers import SentenceTransformer

class SherlockBot:
    def __init__(self, api_key, chroma_path="backend\sherlock_chromadb"):
        """Initialize SherlockBot with necessary components"""
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.chroma_client = chromadb.PersistentClient(path=chroma_path)
        self.collection = self.chroma_client.get_collection(name="sherlock_holmes")
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def retrieve_sherlock_response(self, query, top_k=3):
        """Retrieves Sherlock Holmes knowledge from ChromaDB and generates a response"""
        query_embedding = self.embedding_model.encode(query).tolist()

        # Search ChromaDB for relevant documents
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        # Handle empty results properly
        retrieved_texts = []
        if results["metadatas"] and len(results["metadatas"][0]) > 0:
            retrieved_texts = [metadata["text"] for metadata in results["metadatas"][0]]
        else:
            retrieved_texts = ["I could not deduce anything useful from my sources."]  # Default response

        context = "\n\n".join(retrieved_texts)

        prompt = f"""
        You are Sherlock Holmes, the world's greatest detective from Sir Arthur Conan Doyle's stories. 
        Stay true to your character, knowledge, and investigative methods. 
        Answer the question using the retrieved knowledge below:

        {context}

        Question: {query}

        Answer in Sherlock Holmes' deduction style:
        """

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are Sherlock Holmes, the master detective. Stay within the lore of the books."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content  # ✅ FIXED: Corrected API response extraction

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

    def reset_conversation(self, conversation_id):
        """Resets conversation history (if tracking is implemented)"""
        print(f"Resetting conversation: {conversation_id}")







