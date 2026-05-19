# Mental Health Knowledge Base

This directory contains sample mental health educational documents to populate your Pinecone Assistant knowledge base.

## Documents Included

1. **01_crisis_resources.txt** - Emergency hotlines and crisis support information
2. **02_understanding_anxiety.txt** - Information about anxiety disorders and management
3. **03_understanding_depression.txt** - Comprehensive guide to depression
4. **04_coping_strategies.txt** - Practical techniques for managing difficult emotions
5. **05_stress_management.txt** - Strategies for managing and reducing stress
6. **06_seeking_professional_help.txt** - Guide to therapy and mental health professionals
7. **07_self_care_wellness.txt** - Self-care practices across multiple dimensions

## How to Use These Documents

### Option 1: Upload to Pinecone Console (Easiest)

1. Log in to your Pinecone account at https://app.pinecone.io/
2. Navigate to your Assistant
3. Go to the "Knowledge Base" or "Upload" section
4. Upload all `.txt` files from this directory
5. Wait for Pinecone to process and index the documents
6. Test queries to ensure the knowledge base is working

### Option 2: Upload via Pinecone API

```python
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
import os

# Initialize Pinecone
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
assistant = pc.assistant.Assistant(assistant_name=os.environ["ASSISTANT_NAME"])

# Upload documents
knowledge_base_dir = "knowledge_base"
for filename in os.listdir(knowledge_base_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(knowledge_base_dir, filename)
        with open(file_path, 'r') as f:
            content = f.read()
            # Use Pinecone's document upload method
            assistant.upload_document(
                document_name=filename,
                content=content
            )
```

### Option 3: Create Custom RAG System

If you prefer to build your own retrieval system:
- Use these documents as training data
- Implement embeddings (OpenAI, Cohere, etc.)
- Store in vector database of choice
- Build custom retrieval logic

## Integrating with Your Agent

Once uploaded to Pinecone, update `agent.py`:

1. Uncomment the Pinecone imports (lines 18-19):
```python
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
```

2. Uncomment the Pinecone initialization (lines 24-25):
```python
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
assistant = pc.assistant.Assistant(assistant_name=os.environ["ASSISTANT_NAME"])
```

3. Update the `ask_knowledge_base` function (around line 32):
```python
@function_tool
async def ask_knowledge_base(question: str) -> str:
    """Query the mental health knowledge base for information."""
    try:
        msg = Message(content=question)
        response = assistant.chat(messages=[msg])
        return response.message.content
    except Exception as e:
        return "I'm here to provide general mental health information and support. For specific medical advice or crisis situations, please contact a licensed mental health professional or crisis hotline."
```

4. Add your API keys to `.env`:
```bash
PINECONE_API_KEY=your_api_key_here
ASSISTANT_NAME=your_assistant_name_here
```

## Important Notes

### Legal & Ethical Considerations

- ⚠️ **These documents are for educational purposes only**
- ⚠️ **Not a replacement for professional medical/mental health advice**
- ⚠️ **Always include appropriate disclaimers in your agent's responses**
- ⚠️ **Ensure compliance with healthcare regulations (HIPAA, etc.)**
- ⚠️ **Have clear crisis protocols and referral pathways**

### Content Guidelines

These documents:
- Are general educational resources
- Include appropriate disclaimers
- Encourage professional help when needed
- Provide crisis resources
- Use non-judgmental, supportive language
- Are based on evidence-based practices

### Updating Content

You should regularly:
- Review and update information
- Add new topics as needed
- Verify crisis hotlines are current
- Ensure content remains evidence-based
- Tailor to your specific use case and audience

### Additional Topics to Consider

Expand your knowledge base with:
- PTSD and trauma
- Eating disorders
- Substance use disorders
- Sleep disorders
- ADHD and learning differences
- Autism spectrum
- Bipolar disorder
- OCD and related disorders
- Grief and loss
- Relationship issues
- Parenting and family dynamics
- Cultural considerations in mental health
- LGBTQ+ mental health
- Youth mental health
- Older adult mental health
- Workplace mental health

## Testing Your Knowledge Base

After uploading, test with queries like:
- "What are signs of anxiety?"
- "How can I manage stress?"
- "What should I do if I'm in crisis?"
- "When should I seek professional help?"
- "What are some coping strategies for difficult emotions?"

## Need Help?

- Pinecone Documentation: https://docs.pinecone.io/
- Pinecone Assistant Guide: https://docs.pinecone.io/guides/assistant
- Mental Health Resources: https://www.nimh.nih.gov/
- Crisis Support: Call 988 or text HOME to 741741

## License & Usage

These sample documents are provided as-is for educational purposes. You may:
- Modify and adapt for your use case
- Add to or remove content
- Customize for your audience
- Use as templates for additional content

Always ensure your use complies with relevant laws and ethical guidelines for mental health support.

---

**Disclaimer**: This is sample educational content. For actual deployment of a mental health support system, consult with licensed mental health professionals, legal advisors, and ensure compliance with all applicable regulations.
