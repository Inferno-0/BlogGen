import os
import json
import time
import google.generativeai as genai

# Initialize the Gemini client
api_key = os.environ.get("LLM_API_KEY")
if not api_key:
    raise ValueError("LLM_API_KEY not found in environment variables.")

genai.configure(api_key=os.environ.get("LLM_API_KEY"))

# CRITICAL: Use exactly this model string
MODEL_NAME = "gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)


def agent_research_outline(input_data: dict) -> str:
    """
    Function 1: Prompts the Gemini model to create a highly detailed blog outline 
    based on the keywords and search intent.
    """
    print("Agent 1: Drafting outline...")
    start_time = time.time()
    
    prompt = f"""
    Act as a Senior Technical SEO Architect.
    Create a highly detailed blog outline based on the following input, optimized for High Semantic Richness:
    - Primary Keyword: {input_data.get('primary_keyword')}
    - Secondary Keywords: {', '.join(input_data.get('secondary_keywords', []))}
    - Search Intent: {input_data.get('search_intent')}
    - SERP Gaps: {', '.join(input_data.get('serp_gaps', []))}

    Please provide a structured outline with headings and subheadings.
    You MUST explicitly include specific H2s for 'Search Intent Satisfaction' and H3s for addressing the SERP Gaps.
    """
    
    response = model.generate_content(prompt)
    
    end_time = time.time()
    print(f"Agent 1: Outline drafted in {end_time - start_time:.2f} seconds.")
    
    return response.text


def agent_draft_content(outline: str) -> str:
    """
    Function 2: Prompts the Gemini model to write the full blog. 
    Instructs it to write concise, 40-60 word answers directly after headings 
    to secure 'Position 0' featured snippets.
    """
    print("Agent 2: Drafting full content...")
    start_time = time.time()
    
    prompt = f"""
    Write a full blog post based on the following outline:
    
    {outline}

    Write with strong E-E-A-T signals (Expertise, Experience, Authoritativeness, Trustworthiness).
    Enforce short, punchy paragraphs (max 3 sentences).
    Require the use of bulleted lists, bolded key concepts, and high-engagement transition hooks.

    CRITICAL INSTRUCTION:
    Write concise, 40-60 word answers directly after each main heading to secure 'Position 0' featured snippets.
    """
    
    response = model.generate_content(prompt)
    
    end_time = time.time()
    print(f"Agent 2: Content drafted in {end_time - start_time:.2f} seconds.")
    
    return response.text


def agent_optimize_seo(draft: str, serp_gaps: list) -> str:
    """
    Function 3: Prompts the Gemini model to format the text into clean HTML, 
    fix the SERP gaps, ensure the Flesch-Kincaid readability score is natural, 
    and append an FAQ schema at the bottom.
    Forces the model to return a raw JSON string containing exactly these keys: 
    title, meta_description, html_content, and faq_schema.
    """
    print("Agent 3: Optimizing SEO and formatting to JSON...")
    start_time = time.time()
    
    prompt = f"""
    Act as a Technical HTML SEO Master.
    Take the following blog draft and optimize it for SEO:
    
    DRAFT:
    {draft}
    
    SERP GAPS TO FIX:
    {', '.join(serp_gaps)}
    
    INSTRUCTIONS:
    1. Fix the provided SERP gaps (e.g., expand word count where necessary, add missing details).
    2. Format the text into strict Semantic HTML5 (use tags like <article>, <section>, <aside>, <h2>, <h3>, <p>, <ul>, etc.).
    3. Ensure the Flesch-Kincaid readability score is natural and conversational.
    4. Generate FAQ data, but DO NOT put the <script> tag inside the HTML.
    
    OUTPUT FORMAT:
    You MUST return ONLY a JSON object containing EXACTLY these keys:
    "title" - The SEO-optimized title of the blog post.
    "meta_description" - A compelling meta description (under 160 characters).
    "html_content" - The fully formatted HTML content ONLY. CRITICAL: Do NOT wrap the HTML in markdown code blocks (e.g., no ```html and no ```). Return the raw string starting directly with the first HTML tag.
    "faq_schema" - A nested, raw JSON object representing the FAQ data (Do not format it as a string).
    """
    
    # Use response_mime_type to guarantee a JSON string output
    generation_config = genai.GenerationConfig(
        response_mime_type="application/json",
    )
    
    response = model.generate_content(prompt, generation_config=generation_config)
    
    end_time = time.time()
    print(f"Agent 3: SEO optimization completed in {end_time - start_time:.2f} seconds.")
    
    return response.text


def run_pipeline(input_data: dict) -> dict:
    """
    Main pipeline controller that processes data sequentially through 3 agent functions.
    """
    print("Starting Blog Orchestrator Pipeline...\n")
    print(f"Input Data: {json.dumps(input_data, indent=2)}\n")
    
    try:
        # Agent 1: Research Outline
        outline = agent_research_outline(input_data)
        
        # Agent 2: Draft Content
        draft = agent_draft_content(outline)
        
        # Agent 3: Optimize SEO
        seo_json_string = agent_optimize_seo(draft, input_data.get('serp_gaps', []))
        
        # Parse output JSON to ensure adherence to contract
        final_output = json.loads(seo_json_string, strict=False)
        print("\nPipeline execution completed successfully!")
        
        return final_output
        
    except json.JSONDecodeError as e:
        print(f"\nError: Model did not return valid JSON. {e}")
        print(f"Raw output: {seo_json_string}")
        return {}
    except Exception as e:
        print(f"\nPipeline execution failed: {e}")
        return {}


if __name__ == "__main__":
    # Mock input data to test the pipeline execution immediately
    mock_input = {
        "primary_keyword": "autonomous AI agents",
        "secondary_keywords": ["AI orchestration", "multi-agent systems", "AI workflows"],
        "search_intent": "Informational - Users want to understand how autonomous AI agents work together in workflows.",
        "serp_gaps": ["lack of real-world examples", "insufficient word count on technical architectures"]
    }
    
    result = run_pipeline(mock_input)
    
    print("\n--- FINAL OUTPUT VALIDATION ---")
    if result:
        print(f"Keys returned: {list(result.keys())}")
        print(f"TITLE: {result.get('title')}")
        print(f"META DESCRIPTION: {result.get('meta_description')}")
        
        html_preview = str(result.get('html_content', ''))
        print(f"HTML CONTENT PREVIEW: {html_preview[:200]}...")
        
        print("FAQ SCHEMA PRESENT: ", 'faq_schema' in result)
    else:
        print("Pipeline returned no valid output.")
