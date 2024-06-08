

async def generate_content_async(model, prompt):
    # Your asynchronous content generation logic
    response = await model.generate_content_async(prompt)
    return response.text
