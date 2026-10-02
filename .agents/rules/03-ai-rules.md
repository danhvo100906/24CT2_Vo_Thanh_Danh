# AI DEVELOPMENT RULES
Current main AI remains:
PyTorch + Bag of Words + Neural Network + Intent Classification.

Do not replace it automatically.

AI improvements must be evidence-driven:
1. inspect current behavior;
2. inspect failing examples/tests;
3. identify root cause;
4. propose the smallest improvement;
5. test before/after.

Semantic Search, Embedding, RAG, Vector DB and advanced AI are roadmap items unless explicitly authorized.

For chatbot behavior:
- stay on the user's topic;
- use trusted data where available;
- do not fabricate school information;
- preserve source/update metadata;
- use fallback when evidence is insufficient;
- context should remain limited and relevant.
