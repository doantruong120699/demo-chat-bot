"""
LLM Service - A unified service for switching between different LLM providers
Supports OpenAI, Claude, Ngrok, and other providers
"""

import os
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
from enum import Enum
from dataclasses import dataclass
from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import requests
import json


class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    CLAUDE = "claude"
    NGROK = "ngrok"
    CUSTOM = "custom"


@dataclass
class LLMConfig:
    """Configuration for LLM service"""
    provider: LLMProvider
    model: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    streaming: bool = True
    callbacks: Optional[List[BaseCallbackHandler]] = None
    kwargs: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self._llm = None
    
    @property
    def llm(self) -> BaseLanguageModel:
        """Get the configured LLM instance"""
        if self._llm is None:
            self._llm = self._create_llm()
        return self._llm
    
    @abstractmethod
    def _create_llm(self) -> BaseLanguageModel:
        """Create the LLM instance"""
        pass
    
    def invoke(self, messages: Union[str, List[BaseMessage]], **kwargs) -> Any:
        """Invoke the LLM with messages"""
        if isinstance(messages, str):
            messages = [HumanMessage(content=messages)]
        return self.llm.invoke(messages, **kwargs)
    
    def stream(self, messages: Union[str, List[BaseMessage]], **kwargs):
        """Stream responses from the LLM"""
        if isinstance(messages, str):
            messages = [HumanMessage(content=messages)]
        return self.llm.stream(messages, **kwargs)
    
    def get_llm_instance(self) -> BaseLanguageModel:
        """Get the raw LLM instance for direct use"""
        return self.llm


class OpenAIProvider(BaseLLMProvider):
    """OpenAI provider implementation"""
    
    def _create_llm(self) -> BaseLanguageModel:
        """Create OpenAI ChatOpenAI instance"""
        return ChatOpenAI(
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            openai_api_key=self.config.api_key or os.getenv("OPENAI_API_KEY"),
            streaming=self.config.streaming,
            callbacks=self.config.callbacks,
            **self.config.kwargs
        )


class ClaudeProvider(BaseLLMProvider):
    """Claude (Anthropic) provider implementation"""
    
    def _create_llm(self) -> BaseLanguageModel:
        """Create Claude ChatAnthropic instance"""
        return ChatAnthropic(
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            anthropic_api_key=self.config.api_key or os.getenv("ANTHROPIC_API_KEY"),
            streaming=self.config.streaming,
            callbacks=self.config.callbacks,
            **self.config.kwargs
        )


class NgrokProvider(BaseLLMProvider):
    """Ngrok provider implementation for custom endpoints"""
    
    def _create_llm(self) -> BaseLanguageModel:
        """Create a custom LLM that uses Ngrok endpoint"""
        # This is a simplified implementation
        # You might need to create a custom LLM class for more complex scenarios
        return ChatOpenAI(
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            openai_api_key=self.config.api_key or "dummy-key",  # Not used for custom endpoints
            openai_api_base=self.config.base_url,
            streaming=self.config.streaming,
            callbacks=self.config.callbacks,
            **self.config.kwargs
        )


class CustomProvider(BaseLLMProvider):
    """Custom provider implementation for any custom LLM service"""
    
    def _create_llm(self) -> BaseLanguageModel:
        """Create a custom LLM instance"""
        # This can be extended to support any custom LLM service
        # For now, we'll use OpenAI with custom base URL
        return ChatOpenAI(
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            openai_api_key=self.config.api_key or "dummy-key",
            openai_api_base=self.config.base_url,
            streaming=self.config.streaming,
            callbacks=self.config.callbacks,
            **self.config.kwargs
        )


class LLMService:
    """Main LLM service that manages different providers"""
    
    def __init__(self, default_provider: LLMProvider = LLMProvider.OPENAI, default_config: Optional[LLMConfig] = None):
        self.default_provider = default_provider
        self.default_config = default_config or self._get_default_config()
        self._providers: Dict[LLMProvider, BaseLLMProvider] = {}
        self._current_provider = None
    
    def _get_default_config(self) -> LLMConfig:
        """Get default configuration based on environment"""
        return LLMConfig(
            provider=self.default_provider,
            model="gpt-4o-mini" if self.default_provider == LLMProvider.OPENAI else "claude-3-sonnet-20240229",
            temperature=0.7,
            streaming=True
        )
    
    def get_provider(self, provider: Optional[LLMProvider] = None) -> BaseLLMProvider:
        """Get a provider instance"""
        provider = provider or self.default_provider
        
        if provider not in self._providers:
            config = self.default_config
            if provider != self.default_provider:
                config = LLMConfig(
                    provider=provider,
                    model=self._get_default_model(provider),
                    temperature=0.7,
                    streaming=True
                )
            
            self._providers[provider] = self._create_provider(provider, config)
        
        return self._providers[provider]
    
    def _get_default_model(self, provider: LLMProvider) -> str:
        """Get default model for provider"""
        models = {
            LLMProvider.OPENAI: "gpt-4o-mini",
            LLMProvider.CLAUDE: "claude-3-sonnet-20240229",
            LLMProvider.NGROK: "gpt-3.5-turbo",
            LLMProvider.CUSTOM: "custom-model"
        }
        return models.get(provider, "gpt-4o-mini")
    
    def _create_provider(self, provider: LLMProvider, config: LLMConfig) -> BaseLLMProvider:
        """Create a provider instance"""
        provider_classes = {
            LLMProvider.OPENAI: OpenAIProvider,
            LLMProvider.CLAUDE: ClaudeProvider,
            LLMProvider.NGROK: NgrokProvider,
            LLMProvider.CUSTOM: CustomProvider
        }
        
        provider_class = provider_classes.get(provider)
        if not provider_class:
            raise ValueError(f"Unsupported provider: {provider}")
        
        return provider_class(config)
    
    def switch_provider(self, provider: LLMProvider, config: Optional[LLMConfig] = None):
        """Switch to a different provider"""
        if config:
            self._providers[provider] = self._create_provider(provider, config)
        self._current_provider = provider
    
    def invoke(self, messages: Union[str, List[BaseMessage]], provider: Optional[LLMProvider] = None, **kwargs) -> Any:
        """Invoke LLM with messages"""
        provider_instance = self.get_provider(provider)
        return provider_instance.invoke(messages, **kwargs)
    
    def stream(self, messages: Union[str, List[BaseMessage]], provider: Optional[LLMProvider] = None, **kwargs):
        """Stream responses from LLM"""
        provider_instance = self.get_provider(provider)
        return provider_instance.stream(messages, **kwargs)
    
    def get_llm(self, provider: Optional[LLMProvider] = None) -> BaseLanguageModel:
        """Get the LLM instance for direct use"""
        provider_instance = self.get_provider(provider)
        return provider_instance.get_llm_instance()
    
    def create_agent_llm(self, provider: Optional[LLMProvider] = None, **kwargs) -> BaseLanguageModel:
        """Create LLM instance specifically for agents"""
        provider_instance = self.get_provider(provider)
        config = provider_instance.config
        
        # Filter out parameters that are explicitly set to avoid conflicts
        explicit_params = {'model', 'temperature', 'max_tokens', 'api_key', 'base_url', 'streaming', 'callbacks'}
        filtered_kwargs = {k: v for k, v in kwargs.items() if k not in explicit_params}
        
        # Override config with agent-specific parameters
        agent_config = LLMConfig(
            provider=config.provider,
            model=kwargs.get('model', config.model),
            temperature=kwargs.get('temperature', config.temperature),
            max_tokens=kwargs.get('max_tokens', config.max_tokens),
            api_key=kwargs.get('api_key', config.api_key),
            base_url=kwargs.get('base_url', config.base_url),
            streaming=kwargs.get('streaming', config.streaming),
            callbacks=kwargs.get('callbacks', config.callbacks),
            kwargs={**config.kwargs, **filtered_kwargs}
        )
        
        return self._create_provider(provider or self.default_provider, agent_config).get_llm_instance()


# Global LLM service instance
llm_service = LLMService()


def get_llm_service() -> LLMService:
    """Get the global LLM service instance"""
    return llm_service


def create_llm_config(
    provider: LLMProvider,
    model: str,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    streaming: bool = True,
    callbacks: Optional[List[BaseCallbackHandler]] = None,
    **kwargs
) -> LLMConfig:
    """Create LLM configuration"""
    return LLMConfig(
        provider=provider,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key,
        base_url=base_url,
        streaming=streaming,
        callbacks=callbacks,
        kwargs=kwargs
    )
