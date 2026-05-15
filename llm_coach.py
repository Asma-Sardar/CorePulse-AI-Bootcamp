from groq import Groq

client = Groq(api_key="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")

def get_coaching_advice(recovery_score, rag_context):
    message = client.chat.completions.create(
       model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""You are a personal fitness and recovery coach.
                
The user's recovery score is: {recovery_score}/100

Based on this recovery data:
{rag_context}

Give personalized coaching advice in 3-4 sentences."""
            }
        ]
    )
    return message.choices[0].message.content

# Test
if __name__ == "__main__":
    score = 65
    context = "User slept 6 hours, workout intensity was high yesterday"
    advice = get_coaching_advice(score, context)
    print(advice)
