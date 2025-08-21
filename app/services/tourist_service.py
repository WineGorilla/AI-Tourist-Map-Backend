from app.models.text_model import text_pipe
from app.models.image_model import image_pipe
from app.utils.extract import extract_recommendation, extract_schedule
from app.utils.image_helper import image_to_base64

def generate_info(prompt_location):
    prompt = f"Please describe the information of {prompt_location} for visitors."
    output = text_pipe(prompt, max_new_tokens=128, do_sample=True, temperature=0.7)[0]["generated_text"]
    return output[len(prompt):].strip()

def generate_recommendation_locations(prompt_location, preference):
    prompt = (
        f"Please return a list of 3 to 4 popular tourist places in {prompt_location} "
        f"that are suitable for tourists interested in {preference}. Return only like ['Place 1', 'Place 2', ...]"
    )
    output = text_pipe(prompt, max_new_tokens=128, do_sample=True, temperature=0.5, top_p=0.9, top_k=50)[0]["generated_text"]
    return output[len(prompt):].strip() if output.startswith(prompt) else output.strip()

def generate_schedule_json(prompt_location, recommendation=None):
    base_prompt = f"""You are a local travel expert. Please generate a helpful one-day tourist itinerary for visiting {prompt_location}."""
    if recommendation:
        places_str = ', '.join(recommendation)
        base_prompt += f"\nTry to include the: {places_str}."

    base_prompt += """
Please strictly return a well-formatted JSON object with *three* keys: "Morning", "Afternoon", and "Evening".

Example format:
{
  "Morning": [{"time": "9:00am - 10:00am", "activity": "Breakfast at Clinton St. Baking Company"}],
  "Afternoon": [],
  "Evening": []
}
Return ONLY the JSON object. No explanation. No code formatting.
"""

    result = text_pipe(base_prompt, max_new_tokens=512, do_sample=True, temperature=0.7, top_p=0.9, top_k=50)[0]["generated_text"]
    content = result[len(base_prompt):].strip() if result.startswith(base_prompt) else result.strip()
    return content

def generate_image(prompt_location):
    prompt = f"A photorealistic scenic image of {prompt_location}, detailed"
    return image_pipe(prompt=prompt, num_inference_steps=30, guidance_scale=7.5).images[0]

def generate_tourist_info(city, street, location=None, preference=None, return_base64=False):
    prompt_location = f"{location}, {street}, {city}" if location else f"{street}, {city}"
    print(f"Generating for: {prompt_location}")

    info = generate_info(prompt_location)

    recommendation = None
    if preference:
        pref_text = ", ".join(preference) if isinstance(preference, (list, tuple)) else str(preference)
        recommendation = generate_recommendation_locations(prompt_location, pref_text)

    schedule = generate_schedule_json(prompt_location, recommendation)

    if isinstance(recommendation, str):
        print(recommendation)
        recommendation = extract_recommendation(recommendation)

    if isinstance(schedule, str):
        print(schedule)
        schedule = extract_schedule(schedule)

    image_data = image_to_base64(generate_image(prompt_location)) if return_base64 else None

    return {
        "location": prompt_location,
        "info": info,
        "recommendation": recommendation,
        "schedule": schedule,
        "image": image_data
    }
