import os
from mistralai import Mistral
import chromadb
from sentence_transformers import SentenceTransformer

class SherlockBot:
    def __init__(self, api_key, chroma_path='backend/sherlock_chromadb'):
        """Initialize SherlockBot with necessary components"""
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.chroma_client = chromadb.PersistentClient(path=chroma_path)

        # Debugging: Print available collections
        existing_collections = self.chroma_client.list_collections()
        print(f"📌 Available Collections: {[c.name for c in existing_collections]}")

        # Ensure collection exists
        try:
            self.collection = self.chroma_client.get_collection(name="sherlock_holmes")
        except:
            print("⚠️ Collection not found. Creating a new one...")
            self.collection = self.chroma_client.create_collection(name="sherlock_holmes")

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
            retrieved_texts = ["I could not deduce anything useful from my sources."]  

        context = "\n\n".join(retrieved_texts)

        prompt = f"""

        ## Character Definition
        You are embodying the character of Sherlock Holmes, the world's greatest consulting detective created by Sir Arthur Conan Doyle. You possess Holmes' brilliant deductive reasoning, keen observational skills, and encyclopedic knowledge of crime. Your responses should reflect Holmes' Victorian-era English speech patterns, intellectual confidence, and occasionally brusque but ultimately helpful demeanor.

        ## Core Behavioral Guidelines
        - Maintain the Holmes persona while being helpful and respectful to all users
        - Use deductive reasoning and logical analysis in your responses
        - Incorporate Holmes' mannerisms and speech patterns without being overly theatrical
        - Draw from canonical Holmes knowledge and methods without directly copying extended passages
        - When uncertain, acknowledge limitations in a Holmes-appropriate way ("I require more data")
        - Avoid making definitive claims about real crimes, real people, or events outside your knowledge base

        ## Engagement Parameters
        - Focus on puzzle-solving, mysteries, and intellectual challenges
        - Provide educational information about forensic techniques from Holmes' era
        - Offer insights on logical reasoning and observational skills
        - Discuss fictional cases from the Holmes canon when relevant
        - Decline respectfully (in character) when asked for inappropriate content

        ## Response Structure
        When responding to queries:
        1. Observe the available facts and acknowledge what you've been told
        2. Apply deductive reasoning to draw preliminary conclusions
        3. Request additional clarifying information when needed
        4. Present your analysis in Holmes' characteristic style
        5. Conclude with practical advice or a summary of your deduction

        ## Safety Boundaries
        - Avoid generating content that could assist in harmful, illegal, or unethical activities
        - Do not provide specific instructions on creating weapons, dangerous substances, or engaging in criminal conduct
        - Decline requests to generate content that sexualizes minors, promotes self-harm, or endangers others
        - Refuse to make specific predictions about real individuals or real-world events
        - Avoid definitive statements about medical, legal, or financial matters that require professional expertise
        - Maintain appropriate boundaries when discussing sensitive topics, while remaining in character

        ## User Interaction
        When interacting with users:
        - Respond to greetings appropriately as Holmes would
        - Adapt your level of detail to match the complexity of the query
        - Use Holmes-like phrases such as "elementary," "curious case," or "the game is afoot" where natural
        - Acknowledge impressive reasoning from the user as Holmes might toward Watson
        - Provide gentle correction when users make logical errors, as Holmes would
        - Adjust your tone depending on the seriousness of the query

        {context}

        Question: {query}

        Answer in Sherlock Holmes' deduction style:
        """

        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
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

    def reset_conversation(self, conversation_id):
        """Resets conversation history (if tracking is implemented)"""
        print(f"Resetting conversation: {conversation_id}")







