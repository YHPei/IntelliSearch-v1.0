/**
 * SmartSearch.jsx
 * Professional AI Search Engine Component
 * Perfect Centered Layout
 */

import React, { useState } from 'react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/smart_search';

const SmartSearch = () => {
  // State Management
  const [query, setQuery] = useState('');
  const [searchEngine, setSearchEngine] = useState('google');
  const [llmProvider, setLlmProvider] = useState('openai');
  
  const [useCustomSearchKey, setUseCustomSearchKey] = useState(false);
  const [searchcansApiKey, setSearchcansApiKey] = useState('');
  const [useCustomLlmKey, setUseCustomLlmKey] = useState(false);
  const [llmApiKey, setLlmApiKey] = useState('');
  
  const [isLoading, setIsLoading] = useState(false);
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [metadata, setMetadata] = useState(null);
  const [error, setError] = useState('');

  // Load saved config
  React.useEffect(() => {
    const savedLlmProvider = localStorage.getItem('llmProvider');
    const savedUseCustomSearchKey = localStorage.getItem('useCustomSearchKey');
    const savedSearchcansKey = localStorage.getItem('searchcansApiKey');
    const savedUseCustomLlmKey = localStorage.getItem('useCustomLlmKey');
    const savedLlmKey = localStorage.getItem('llmApiKey');
    
    if (savedLlmProvider) setLlmProvider(savedLlmProvider);
    if (savedUseCustomSearchKey) setUseCustomSearchKey(savedUseCustomSearchKey === 'true');
    if (savedSearchcansKey) setSearchcansApiKey(savedSearchcansKey);
    if (savedUseCustomLlmKey) setUseCustomLlmKey(savedUseCustomLlmKey === 'true');
    if (savedLlmKey) setLlmApiKey(savedLlmKey);
  }, []);

  const saveConfig = () => {
    localStorage.setItem('llmProvider', llmProvider);
    localStorage.setItem('useCustomSearchKey', useCustomSearchKey.toString());
    localStorage.setItem('useCustomLlmKey', useCustomLlmKey.toString());
    
    if (useCustomSearchKey && searchcansApiKey) {
      localStorage.setItem('searchcansApiKey', searchcansApiKey);
    } else {
      localStorage.removeItem('searchcansApiKey');
    }
    
    if (useCustomLlmKey && llmApiKey) {
      localStorage.setItem('llmApiKey', llmApiKey);
    } else {
      localStorage.removeItem('llmApiKey');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const trimmedQuery = query.trim();
    if (!trimmedQuery) {
      setError('Please enter your question');
      return;
    }

    setError('');
    setAnswer('');
    setSources([]);
    setMetadata(null);
    setIsLoading(true);
    saveConfig();

    try {
      const requestData = {
        query: trimmedQuery,
        search_engine: searchEngine,
        llm_provider: llmProvider,
      };

      if (useCustomSearchKey && searchcansApiKey) {
        requestData.searchcans_api_key = searchcansApiKey;
      }

      if (useCustomLlmKey && llmApiKey) {
        requestData.llm_api_key = llmApiKey;
      }

      const response = await axios.post(API_URL, requestData, {
        headers: { 'Content-Type': 'application/json' },
        timeout: 30000,
      });

      const { answer: aiAnswer, sources: sourcesData, metadata: metaData } = response.data;
      setAnswer(aiAnswer);
      setSources(sourcesData || []);
      setMetadata(metaData || null);

    } catch (err) {
      console.error('API error:', err);
      
      if (err.response) {
        const errorMessage = err.response.data?.detail || err.response.data?.error || 'Server error';
        setError(`Error (${err.response.status}): ${errorMessage}`);
      } else if (err.request) {
        setError('Cannot connect to server. Check network or backend status.');
      } else {
        setError(`Request failed: ${err.message}`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setQuery('');
    setAnswer('');
    setSources([]);
    setMetadata(null);
    setError('');
  };

  const handleExampleClick = (exampleQuery) => {
    setQuery(exampleQuery);
    setError('');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Centered Container */}
      <div className="flex-1 flex items-center justify-center py-8">
        <div className="w-full max-w-3xl mx-auto px-4">
          
          {/* Header */}
          <header className="text-center mb-6">
            <div className="inline-flex items-center justify-center gap-2 mb-2">
              <span className="text-xl">🔍</span>
              <h1 className="text-2xl font-bold text-gray-900">
                AI Search Engine
              </h1>
            </div>
            <p className="text-sm text-gray-600">
              Real-time web search powered by AI
            </p>
          </header>

          {/* Main Card */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-4">
            <form onSubmit={handleSubmit} className="p-5">
              
              {/* Query Input */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Your Question
                </label>
                <textarea
                  className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:ring-1 focus:ring-blue-200 transition-colors outline-none resize-none"
                  rows="3"
                  placeholder="What are the latest AI developments in 2024?"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  disabled={isLoading}
                />
              </div>

              {/* Config Grid */}
              <div className="grid grid-cols-2 gap-4 mb-4">
                
                {/* Search Engine */}
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-2">
                    Search Engine
                  </label>
                  <div className="flex gap-2">
                    {['google', 'bing'].map((engine) => (
                      <label key={engine} className="flex-1">
                        <input
                          type="radio"
                          name="search-engine"
                          value={engine}
                          checked={searchEngine === engine}
                          onChange={(e) => setSearchEngine(e.target.value)}
                          disabled={isLoading}
                          className="sr-only"
                        />
                        <div className={`px-3 py-2 rounded-md text-center text-sm font-medium cursor-pointer transition-all ${
                          searchEngine === engine
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        }`}>
                          {engine.charAt(0).toUpperCase() + engine.slice(1)}
                        </div>
                      </label>
                    ))}
                  </div>
                </div>

                {/* LLM Provider */}
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-2">
                    AI Model
                  </label>
                  <div className="flex gap-2">
                    {[
                      { value: 'openai', label: 'OpenAI' },
                      { value: 'qwen', label: 'Qwen' }
                    ].map((provider) => (
                      <label key={provider.value} className="flex-1">
                        <input
                          type="radio"
                          name="llm-provider"
                          value={provider.value}
                          checked={llmProvider === provider.value}
                          onChange={(e) => setLlmProvider(e.target.value)}
                          disabled={isLoading}
                          className="sr-only"
                        />
                        <div className={`px-3 py-2 rounded-md text-center text-sm font-medium cursor-pointer transition-all ${
                          llmProvider === provider.value
                            ? 'bg-purple-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        }`}>
                          {provider.label}
                        </div>
                      </label>
                    ))}
                  </div>
                </div>
              </div>

              {/* API Keys (Collapsible) */}
              <details className="mb-4">
                <summary className="text-xs font-medium text-gray-600 cursor-pointer hover:text-gray-900 select-none">
                  API Configuration (Optional) ▼
                </summary>
                
                <div className="mt-3 bg-gray-50 rounded-md p-3 border border-gray-200 space-y-3">
                  
                  {/* SearchCans Key */}
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <label className="text-xs font-medium text-gray-600">SearchCans API</label>
                      <button
                        type="button"
                        onClick={() => setUseCustomSearchKey(!useCustomSearchKey)}
                        className={`text-xs px-2 py-0.5 rounded text-xs ${
                          useCustomSearchKey
                            ? 'bg-blue-100 text-blue-700'
                            : 'bg-gray-200 text-gray-600'
                        }`}
                        disabled={isLoading}
                      >
                        {useCustomSearchKey ? 'Custom' : 'Default'}
                      </button>
                    </div>
                    {useCustomSearchKey && (
                      <input
                        type="password"
                        value={searchcansApiKey}
                        onChange={(e) => setSearchcansApiKey(e.target.value)}
                        placeholder="vcans_xxx..."
                        className="w-full px-2 py-1.5 text-xs border border-gray-300 rounded focus:border-blue-500 focus:ring-1 focus:ring-blue-200 outline-none"
                        disabled={isLoading}
                      />
                    )}
                  </div>

                  {/* LLM Key */}
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <label className="text-xs font-medium text-gray-600">
                        {llmProvider === 'openai' ? 'OpenAI' : 'Qwen'} API
                      </label>
                      <button
                        type="button"
                        onClick={() => setUseCustomLlmKey(!useCustomLlmKey)}
                        className={`text-xs px-2 py-0.5 rounded ${
                          useCustomLlmKey
                            ? 'bg-purple-100 text-purple-700'
                            : 'bg-gray-200 text-gray-600'
                        }`}
                        disabled={isLoading}
                      >
                        {useCustomLlmKey ? 'Custom' : 'Default'}
                      </button>
                    </div>
                    {useCustomLlmKey && (
                      <input
                        type="password"
                        value={llmApiKey}
                        onChange={(e) => setLlmApiKey(e.target.value)}
                        placeholder="sk-..."
                        className="w-full px-2 py-1.5 text-xs border border-gray-300 rounded focus:border-purple-500 focus:ring-1 focus:ring-purple-200 outline-none"
                        disabled={isLoading}
                      />
                    )}
                  </div>
                </div>
              </details>

              {/* Buttons */}
              <div className="flex gap-2 mb-3">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white font-medium py-2.5 px-4 rounded-md transition-colors text-sm"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <span className="flex items-center justify-center gap-2">
                      <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Searching...
                    </span>
                  ) : (
                    'Search'
                  )}
                </button>
                
                <button
                  type="button"
                  onClick={handleClear}
                  className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2.5 px-4 rounded-md transition-colors text-sm"
                  disabled={isLoading}
                >
                  Clear
                </button>
              </div>

              {/* Examples */}
              <div className="pt-3 border-t border-gray-100">
                <p className="text-xs text-gray-500 mb-2">Examples:</p>
                <div className="flex flex-wrap gap-1.5">
                  {[
                    'Latest AI breakthroughs 2024',
                    'ChatGPT vs other LLMs',
                    'React 19 features',
                  ].map((example, index) => (
                    <button
                      key={index}
                      onClick={() => handleExampleClick(example)}
                      className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-600 px-2 py-1 rounded transition-colors"
                      disabled={isLoading}
                    >
                      {example}
                    </button>
                  ))}
                </div>
              </div>
            </form>
          </div>

          {/* Error */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
              <div className="flex items-start gap-2">
                <span className="text-red-600 text-sm">⚠</span>
                <div>
                  <h3 className="text-red-800 font-medium text-sm">Error</h3>
                  <p className="text-red-700 text-xs mt-0.5">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Answer */}
          {answer && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-4">
              <div className="flex items-start gap-3 mb-3">
                <span className="text-lg">💡</span>
                <div className="flex-1">
                  <h2 className="text-base font-bold text-gray-900 mb-1">AI Answer</h2>
                  {metadata && (
                    <div className="flex flex-wrap gap-1.5 text-xs text-gray-600">
                      <span className="bg-gray-100 px-1.5 py-0.5 rounded">
                        {metadata.llm_provider === 'openai' ? 'OpenAI' : 'Qwen'}
                      </span>
                      <span className="bg-gray-100 px-1.5 py-0.5 rounded">
                        {metadata.search_engine}
                      </span>
                      <span className="bg-gray-100 px-1.5 py-0.5 rounded">
                        {metadata.processing_time_ms}ms
                      </span>
                      <span className="bg-gray-100 px-1.5 py-0.5 rounded">
                        {metadata.results_found} sources
                      </span>
                    </div>
                  )}
                </div>
              </div>
              
              <div className="bg-gray-50 rounded-md p-3 border border-gray-100">
                <p className="text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">
                  {answer}
                </p>
              </div>
            </div>
          )}

          {/* Sources */}
          {sources && sources.length > 0 && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-4">
              <h2 className="text-sm font-bold text-gray-900 mb-3 flex items-center gap-1.5">
                <span>📚</span>
                Sources
              </h2>
              
              <div className="space-y-1.5">
                {sources.map((source, index) => (
                  <a
                    key={index}
                    href={source}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-start gap-2 p-2 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded transition-colors group text-xs"
                  >
                    <span className="flex-shrink-0 w-5 h-5 bg-blue-600 text-white rounded flex items-center justify-center text-xs font-bold">
                      {index + 1}
                    </span>
                    <span className="flex-1 text-gray-700 group-hover:text-blue-600 break-all transition-colors">
                      {source}
                    </span>
                    <span className="text-gray-400">↗</span>
                  </a>
                ))}
              </div>
            </div>
          )}

          {/* Footer */}
          <footer className="text-center mt-6 pt-4 border-t border-gray-200">
            <p className="text-xs text-gray-600">
              Powered by <span className="font-medium text-purple-600">OpenAI / Qwen</span> + 
              <span className="font-medium text-blue-600"> SearchCans API</span>
            </p>
            <p className="text-xs text-gray-500 mt-1">
              RAG Architecture · Open Source
            </p>
          </footer>
        </div>
      </div>
    </div>
  );
};

export default SmartSearch;
