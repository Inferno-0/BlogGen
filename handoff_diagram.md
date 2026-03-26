erDiagram
    SERP_API ||--o{ ORGANIC_RESULT : "provides"
    ORGANIC_RESULT }o--|| RESEARCH_AGENT : "parsed_by"
    RESEARCH_AGENT ||--|| OUTPUT_PAYLOAD : "generates"
    OUTPUT_PAYLOAD ||--o{ SERP_GAP : "contains"
    
    SERP_API {
        Array organic_results
    }
    
    ORGANIC_RESULT {
        String title
        String link
        Integer word_count
        String date
    }
    
    RESEARCH_AGENT {
        String script_name "research_agent.py"
        String role "Role 2"
    }
    
    OUTPUT_PAYLOAD {
        String primary_keyword
        Array secondary_keywords
        String search_intent
        Array serp_gaps
    }
    
    SERP_GAP {
        String title
        String url
        Array reasons
    }