import streamlit as st
import json
from orchestrator import run_pipeline

# Configure the Streamlit page
st.set_page_config(
    page_title="AI Blog Orchestrator",
    layout="wide",
    page_icon="🤖"
)

# Main UI Header
st.title("🤖 AI Blog Orchestrator")
st.subheader("An autonomous multi-agent engine that researches, drafts, and SEO-optimizes blog content.")

# Sidebar Configuration
with st.sidebar:
    st.header("Content Settings")
    
    # Input field for target keyword
    target_keyword = st.text_input("Target Keyword", placeholder="e.g. 'autonomous AI agents'")
    
    # Action button
    generate_btn = st.button("Generate Blog Post", type="primary", use_container_width=True)

# Main Execution Logic
if generate_btn:
    if not target_keyword.strip():
        st.sidebar.error("Error: Please provide a Target Keyword.")
    else:
        # Show spinner while the pipeline is executing
        with st.spinner("Orchestrating AI Agents... This may take a minute."):
            
            # Mock Data Hook: Hardcoded input dictionary injecting the target_keyword
            mock_input_data = {
                "primary_keyword": target_keyword.strip(),
                "secondary_keywords": [
                    f"{target_keyword} guide", 
                    f"best {target_keyword} tools", 
                    f"how to implement {target_keyword}"
                ],
                "search_intent": f"Informational - Users are looking for comprehensive details on {target_keyword}.",
                "serp_gaps": ["lack of actionable examples", "low content depth on advanced topics"]
            }
            
            # Execute the multi-agent backend pipeline
            result = run_pipeline(mock_input_data)
            
            if result:
                st.success("Pipeline Execution Complete! 🎉")
                
                # Output Display
                title = result.get("title", "No Title Generated")
                meta_desc = result.get("meta_description", "No Meta Description Generated")
                html_content = result.get("html_content", "<p>No HTML Content Generated.</p>")
                faq_schema = result.get("faq_schema", {})
                
                # Render Title and Meta Description
                st.header(title)
                st.info(f"**Meta Description:** {meta_desc}")
                
                # Render HTML Body Content directly
                st.markdown("---")
                st.markdown(html_content, unsafe_allow_html=True)
                st.markdown("---")
                
                # Render Raw FAQ JSON-LD Database snippet in an accordion module
                with st.expander("View JSON-LD Schema (FAQ)"):
                    if isinstance(faq_schema, str):
                        try:
                            # Parse it if it accidentally comes back as a string
                            st.json(json.loads(faq_schema))
                        except Exception:
                            st.code(faq_schema, language='json')
                    else:
                        st.json(faq_schema)
            else:
                st.error("The orchestration engine encountered an error generating the pipeline. Check terminal logs.")
