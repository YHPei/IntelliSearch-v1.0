"""
AI Search Engine Backend - Powered by SearchCans API

A production-ready RAG (Retrieval-Augmented Generation) implementation
integrating real-time web search with Large Language Models.

Author: Your Name
License: MIT
"""

import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv
import requests
from openai import OpenAI

# ============================================================================
# Logging Configuration
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# Environment Variables
# ============================================================================
load_dotenv()

# Optional default API Keys (users can provide their own in frontend)
DEFAULT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_QWEN_API_KEY = os.getenv("DASHSCOPE_API_KEY")
SEARCHCANS_API_KEY = os.getenv("SEARCHCANS_API_KEY")
SEARCHCANS_API_ENDPOINT = os.getenv("SEARCHCANS_API_ENDPOINT", "https://global.searchcans.com/api/search")

# SearchCans API Key is now optional (users can provide their own)
if not SEARCHCANS_API_KEY:
    logger.warning("SEARCHCANS_API_KEY not found in .env file - users must provide their own key")

# LLM API Keys are optional - users can provide their own
if DEFAULT_OPENAI_API_KEY:
    logger.info("Default OpenAI API Key detected")
if DEFAULT_QWEN_API_KEY:
    logger.info("Default Qwen API Key detected")

# ============================================================================
# Application Lifecycle Management
# ============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle events"""
    # Startup
    logger.info("=" * 60)
    logger.info("AI Search Engine Backend - Starting Up")
    logger.info("=" * 60)
    logger.info(f"SearchCans API: {'Configured' if SEARCHCANS_API_KEY else 'Not Configured'}")
    logger.info(f"Supported Search Engines: Google, Bing")
    logger.info("Supported LLM Providers:")
    logger.info(f"  - OpenAI (Default Key: {'Yes' if DEFAULT_OPENAI_API_KEY else 'No'}, Custom Key: Supported)")
    logger.info(f"  - Qwen (Default Key: {'Yes' if DEFAULT_QWEN_API_KEY else 'No'}, Custom Key: Supported)")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("AI Search Engine Backend - Shutting Down...")

# ============================================================================
# FastAPI Application
# ============================================================================
app = FastAPI(
    title="AI Search Engine API",
    description="RAG-based intelligent search assistant powered by SearchCans API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# ============================================================================
# CORS Configuration
# ============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # React default port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        # Add your production domain here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Pydantic Models
# ============================================================================

class SearchQuery(BaseModel):
    """Request model for search queries"""
    query: str = Field(..., min_length=1, description="Search query text")
    search_engine: str = Field(default="google", description="Search engine: google or bing")
    llm_provider: str = Field(default="openai", description="LLM provider: openai or qwen")
    llm_api_key: Optional[str] = Field(default=None, description="User's custom LLM API key")
    llm_model: Optional[str] = Field(default=None, description="Specific LLM model to use")
    searchcans_api_key: Optional[str] = Field(default=None, description="User's custom SearchCans API key")
    
    @field_validator('query')
    @classmethod
    def validate_query(cls, v):
        """Validate query is not empty"""
        v = v.strip()
        if not v:
            raise ValueError('Query cannot be empty')
        return v
    
    @field_validator('search_engine')
    @classmethod
    def validate_search_engine(cls, v):
        """Validate search engine type"""
        v = v.lower().strip()
        if v not in ['google', 'bing']:
            raise ValueError('Search engine must be google or bing')
        return v
    
    @field_validator('llm_provider')
    @classmethod
    def validate_llm_provider(cls, v):
        """Validate LLM provider"""
        v = v.lower().strip()
        if v not in ['openai', 'qwen']:
            raise ValueError('LLM provider must be openai or qwen')
        return v


class SearchResponse(BaseModel):
    """Response model for search results"""
    answer: str = Field(..., description="AI-generated intelligent answer")
    sources: List[str] = Field(
        default_factory=list, 
        description="List of source URLs"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional metadata"
    )


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error description")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ============================================================================
# Core Business Logic
# ============================================================================

def fetch_searchcans_results(query: str, search_engine: str = "google", page: int = 1, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch search results from SearchCans API
    
    Args:
        query: Search query string
        search_engine: Search engine type (google or bing)
        page: Page number (default 1)
        api_key: Optional custom API key from user
    
    Returns:
        JSON response from SearchCans API
        
    Raises:
        HTTPException: When API call fails
    """
    try:
        # Use custom key if provided, otherwise use server default
        search_api_key = api_key if api_key else SEARCHCANS_API_KEY
        
        if not search_api_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SearchCans API key is required. Please provide your API key or configure server default."
            )
        
        logger.info(f"Calling SearchCans API - Query: '{query}', Engine: {search_engine}, Key: {'Custom' if api_key else 'Server Default'}")
        
        headers = {
            "Authorization": f"Bearer {search_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "s": query,
            "t": search_engine,  # google or bing
            "d": 10000,  # Maximum API wait time (milliseconds) - increased for Google
            "p": page,
            "maxCache": 7200  # Maximum cache hit time (seconds)
        }
        
        response = requests.post(
            SEARCHCANS_API_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=15
        )
        
        # Check HTTP status code
        if response.status_code != 200:
            logger.error(f"SearchCans API returned error status: {response.status_code}")
            error_msg = response.text[:200] if response.text else "Unknown error"
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Search service temporarily unavailable (Status: {response.status_code}, Message: {error_msg})"
            )
        
        data = response.json()
        
        # Validate response structure
        if not isinstance(data, dict):
            logger.error(f"SearchCans API returned unexpected data format")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Search service returned invalid data format"
            )
        
        # Check SearchCans API response code
        api_code = data.get('code', 0)
        api_msg = data.get('msg', '')
        
        if api_code != 0:
            # SearchCans API returned an error
            logger.error(f"SearchCans API error: code={api_code}, msg={api_msg}")
            
            # Provide user-friendly error messages
            if api_code == -2010:
                error_detail = "Invalid SearchCans API key. Please check your API key at https://global.searchcans.com/"
            elif api_code == -2011:
                error_detail = "SearchCans API key quota exceeded. Please check your account balance."
            elif api_code == -2012:
                error_detail = "SearchCans API key expired. Please renew your subscription."
            else:
                error_detail = f"SearchCans API error: {api_msg} (code: {api_code})"
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_detail
            )
        
        # Check if results exist (SearchCans uses 'data' field)
        search_results = data.get('data', [])
        if search_results is None:
            search_results = []
        results_count = len(search_results)
        logger.info(f"SearchCans API call successful - Retrieved {results_count} results")
        return data
        
    except requests.exceptions.Timeout:
        logger.error("SearchCans API request timeout")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Search service timeout, please try again"
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"SearchCans API request exception: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Search service connection failed: {str(e)}"
        )


def extract_search_context(search_data: Dict[str, Any]) -> tuple[str, List[str]]:
    """
    Extract context and source links from SearchCans results
    
    Args:
        search_data: JSON data from SearchCans API
    
    Returns:
        (context_text, source_links): Formatted context and list of source URLs
    """
    # SearchCans uses 'data' field for search results
    search_results = search_data.get("data", [])
    
    # Handle None case
    if search_results is None:
        search_results = []
    
    if not search_results:
        logger.warning("No valid search results found")
        return "", []
    
    context_parts = []
    source_links = []
    
    for idx, result in enumerate(search_results, 1):
        # SearchCans result format: title, url, content
        title = result.get("title", "No title")
        content = result.get("content", "")  # SearchCans uses 'content' field
        url = result.get("url", "")
        
        # Only process results with valid content
        if content and url:
            # Build formatted context entry
            context_entry = f"[Source {idx}] {title}\n{content}\nURL: {url}"
            context_parts.append(context_entry)
            source_links.append(url)
            
            logger.debug(f"Extracted result {idx}: {title[:50]}...")
    
    # Deduplicate source links (maintain order)
    unique_sources = []
    seen = set()
    for link in source_links:
        if link not in seen:
            unique_sources.append(link)
            seen.add(link)
    
    # Combine all context
    context_text = "\n\n".join(context_parts)
    
    logger.info(f"Successfully extracted {len(context_parts)} context entries, {len(unique_sources)} unique sources")
    
    return context_text, unique_sources


def build_enhanced_prompt(user_query: str, context: str) -> List[Dict[str, str]]:
    """
    Build enhanced prompt with search context (Prompt Engineering)
    
    Args:
        user_query: User's original query
        context: Context extracted from search results
    
    Returns:
        List of message dictionaries for LLM API
    """
    system_prompt = """You are an intelligent search assistant. Your task is to provide accurate, comprehensive, and well-structured answers based on real-time web search results.

Guidelines:
1. Base your answer strictly on the provided search results
2. Synthesize information from multiple sources
3. Use clear, professional language
4. Structure your response logically
5. If information is insufficient, acknowledge it
6. Never fabricate information not present in the sources

Response Format:
- Start with a direct answer to the question
- Provide detailed explanation if needed
- Use bullet points for clarity when appropriate
- Keep the tone professional yet accessible"""

    user_prompt = f"""Question: {user_query}

Search Results:
{context}

Based on the search results above, please provide a comprehensive and accurate answer to the question. Structure your response clearly and cite the relevant information from the sources."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    return messages


def generate_ai_answer(
    messages: List[Dict[str, str]], 
    llm_provider: str = "openai",
    llm_api_key: Optional[str] = None,
    llm_model: Optional[str] = None
) -> str:
    """
    Generate AI answer using specified LLM provider
    
    Args:
        messages: List of message dictionaries
        llm_provider: LLM provider (openai or qwen)
        llm_api_key: Optional custom API key from user
        llm_model: Optional specific model name
    
    Returns:
        AI-generated answer text
        
    Raises:
        HTTPException: When LLM API call fails
    """
    try:
        # Determine which API key to use
        if llm_api_key:
            # User provided their own key
            api_key = llm_api_key
            logger.info(f"Using user-provided API key for {llm_provider}")
        else:
            # Use default key from server
            if llm_provider == "openai":
                api_key = DEFAULT_OPENAI_API_KEY
            elif llm_provider == "qwen":
                api_key = DEFAULT_QWEN_API_KEY
            else:
                raise ValueError(f"Unsupported LLM provider: {llm_provider}")
            
            if not api_key:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No API key available for {llm_provider}. Please provide your own API key."
                )
            
            logger.info(f"Using default server API key for {llm_provider}")
        
        # Configure client based on provider
        if llm_provider == "openai":
            client = OpenAI(api_key=api_key)
            model = llm_model or "gpt-4o-mini"
        elif llm_provider == "qwen":
            client = OpenAI(
                api_key=api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            model = llm_model or "qwen-plus"
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")
        
        logger.info(f"Calling {llm_provider} API with model: {model}")
        
        # Call LLM API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        answer = response.choices[0].message.content.strip()
        
        logger.info(f"{llm_provider} API call successful - Generated answer length: {len(answer)} characters")
        
        return answer
        
    except Exception as e:
        logger.error(f"LLM API call failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service error: {str(e)}"
        )


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information"""
    return {
        "message": "AI Search Engine API",
        "version": "1.0.0",
        "description": "RAG-based intelligent search powered by SearchCans API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Search Engine",
        "version": "1.0.0",
        "searchcans_configured": bool(SEARCHCANS_API_KEY),
        "llm_providers": {
            "openai": {
                "default_key_configured": bool(DEFAULT_OPENAI_API_KEY),
                "supports_custom_key": True
            },
            "qwen": {
                "default_key_configured": bool(DEFAULT_QWEN_API_KEY),
                "supports_custom_key": True
            }
        },
        "supported_search_engines": ["google", "bing"]
    }


@app.post(
    "/api/smart_search",
    response_model=SearchResponse,
    responses={
        200: {"description": "Successful response with AI-generated answer"},
        400: {"description": "Invalid request parameters"},
        503: {"description": "Service temporarily unavailable"}
    },
    tags=["Search"]
)
async def smart_search(search_query: SearchQuery):
    """
    Intelligent search endpoint with RAG architecture
    
    Process:
    1. Call SearchCans API for real-time web search
    2. Extract relevant context from search results
    3. Build enhanced prompt with context
    4. Generate AI answer using LLM
    5. Return answer with source citations
    
    Args:
        search_query: SearchQuery model containing query and options
    
    Returns:
        SearchResponse with AI answer, sources, and metadata
    """
    start_time = datetime.now()
    
    try:
        logger.info(f"Received search request: '{search_query.query}' (Engine: {search_query.search_engine}, LLM: {search_query.llm_provider})")
        
        # Step 1: Fetch search results from SearchCans API
        search_data = fetch_searchcans_results(
            query=search_query.query,
            search_engine=search_query.search_engine,
            api_key=search_query.searchcans_api_key
        )
        
        # Step 2: Extract context and sources
        context, sources = extract_search_context(search_data)
        
        if not context:
            logger.warning(f"No valid context extracted for query: {search_query.query}")
            return SearchResponse(
                answer="Sorry, no relevant search results found. Please try different keywords.",
                sources=[],
                metadata={
                    "query": search_query.query,
                    "search_engine": search_query.search_engine,
                    "llm_provider": search_query.llm_provider,
                    "results_found": 0,
                    "processing_time_ms": int((datetime.now() - start_time).total_seconds() * 1000)
                }
            )
        
        # Step 3: Build enhanced prompt
        messages = build_enhanced_prompt(search_query.query, context)
        
        # Step 4: Generate AI answer
        answer = generate_ai_answer(
            messages=messages,
            llm_provider=search_query.llm_provider,
            llm_api_key=search_query.llm_api_key,
            llm_model=search_query.llm_model
        )
        
        # Step 5: Return response
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        logger.info(f"Search request completed successfully - Processing time: {processing_time}ms")
        
        return SearchResponse(
            answer=answer,
            sources=sources,
            metadata={
                "query": search_query.query,
                "search_engine": search_query.search_engine,
                "llm_provider": search_query.llm_provider,
                "llm_model": search_query.llm_model,
                "results_found": len(sources),
                "processing_time_ms": processing_time
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in search endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"Starting server on port {port}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,  # Enable auto-reload in development
        log_level="info"
    )
