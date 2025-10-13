"""
LLM Service Configuration
"""

import os
from typing import Dict, Any, Optional
from common.services.llm_service import LLMProvider, LLMConfig, create_llm_config


class LLMServiceConfig:
    """Configuration manager for LLM service"""
    
    def __init__(self):
        self.default_provider = self._get_default_provider()
        self.provider_configs = self._load_provider_configs()
    
    def _get_default_provider(self) -> LLMProvider:
        """Get default provider from environment"""
        provider_name = os.getenv("DEFAULT_LLM_PROVIDER", "openai").lower()
        provider_map = {
            "openai": LLMProvider.OPENAI,
            "claude": LLMProvider.CLAUDE,
            "ngrok": LLMProvider.NGROK,
            "custom": LLMProvider.CUSTOM
        }
        return provider_map.get(provider_name, LLMProvider.OPENAI)
    
    def _load_provider_configs(self) -> Dict[LLMProvider, LLMConfig]:
        """Load configurations for all providers"""
        configs = {}
        
        # OpenAI configuration
        configs[LLMProvider.OPENAI] = create_llm_config(
            provider=LLMProvider.OPENAI,
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "0")) or None,
            api_key=os.getenv("OPENAI_API_KEY"),
            streaming=os.getenv("OPENAI_STREAMING", "true").lower() == "true"
        )
        
        # Claude configuration
        configs[LLMProvider.CLAUDE] = create_llm_config(
            provider=LLMProvider.CLAUDE,
            model=os.getenv("CLAUDE_MODEL", "claude-3-sonnet-20240229"),
            temperature=float(os.getenv("CLAUDE_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("CLAUDE_MAX_TOKENS", "0")) or None,
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            streaming=os.getenv("CLAUDE_STREAMING", "true").lower() == "true"
        )
        
        # Ngrok configuration
        configs[LLMProvider.NGROK] = create_llm_config(
            provider=LLMProvider.NGROK,
            model=os.getenv("NGROK_MODEL", "gpt-3.5-turbo"),
            temperature=float(os.getenv("NGROK_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("NGROK_MAX_TOKENS", "0")) or None,
            api_key=os.getenv("NGROK_API_KEY"),
            base_url=os.getenv("NGROK_BASE_URL"),
            streaming=os.getenv("NGROK_STREAMING", "true").lower() == "true"
        )
        
        # Custom configuration
        configs[LLMProvider.CUSTOM] = create_llm_config(
            provider=LLMProvider.CUSTOM,
            model=os.getenv("CUSTOM_MODEL", "custom-model"),
            temperature=float(os.getenv("CUSTOM_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("CUSTOM_MAX_TOKENS", "0")) or None,
            api_key=os.getenv("CUSTOM_API_KEY"),
            base_url=os.getenv("CUSTOM_BASE_URL"),
            streaming=os.getenv("CUSTOM_STREAMING", "true").lower() == "true"
        )
        
        return configs
    
    def get_config(self, provider: LLMProvider) -> LLMConfig:
        """Get configuration for a specific provider"""
        return self.provider_configs.get(provider, self.provider_configs[LLMProvider.OPENAI])
    
    def update_config(self, provider: LLMProvider, **kwargs) -> LLMConfig:
        """Update configuration for a provider"""
        current_config = self.get_config(provider)
        updated_config = create_llm_config(
            provider=provider,
            model=kwargs.get('model', current_config.model),
            temperature=kwargs.get('temperature', current_config.temperature),
            max_tokens=kwargs.get('max_tokens', current_config.max_tokens),
            api_key=kwargs.get('api_key', current_config.api_key),
            base_url=kwargs.get('base_url', current_config.base_url),
            streaming=kwargs.get('streaming', current_config.streaming),
            callbacks=kwargs.get('callbacks', current_config.callbacks),
            **kwargs
        )
        self.provider_configs[provider] = updated_config
        return updated_config
    
    def get_available_providers(self) -> list[LLMProvider]:
        """Get list of available providers based on API keys"""
        available = []
        
        for provider, config in self.provider_configs.items():
            if provider == LLMProvider.OPENAI and config.api_key:
                available.append(provider)
            elif provider == LLMProvider.CLAUDE and config.api_key:
                available.append(provider)
            elif provider == LLMProvider.NGROK and config.base_url:
                available.append(provider)
            elif provider == LLMProvider.CUSTOM and (config.api_key or config.base_url):
                available.append(provider)
        
        return available


# Global configuration instance
llm_config = LLMServiceConfig()


def get_llm_config() -> LLMServiceConfig:
    """Get the global LLM configuration instance"""
    return llm_config
