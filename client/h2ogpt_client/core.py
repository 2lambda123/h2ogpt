import asyncio
from enum import Enum
from typing import Optional

import gradio_client  # type: ignore


class PromptType(Enum):
    """Prompt type"""

    DAI_FAQ = "dai_faq"
    HUMAN_BOT = "human_bot"
    HUMAN_BOT_ORIGINAL = "human_bot_orig"
    INSTRUCT = "instruct"
    INSTRUCT_SIMPLE = "instruct_simple"
    INSTRUCT_VICUNA = "instruct_vicuna"
    INSTRUCT_WITH_END = "instruct_with_end"
    OPEN_ASSISTANT = "open_assistant"
    PLAIN = "plain"
    PROMPT_ANSWER = "prompt_answer"
    QUALITY = "quality"
    SIMPLE_INSTRUCT = "simple_instruct"
    SUMMARIZE = "summarize"
    WIZARD_LM = "wizard_lm"
    WIZARD_MEGA = "wizard_mega"


class LangChainMode(Enum):
    """LangChain mode"""

    ALL = "All"
    CHAT_LLM = "ChatLLM"
    DISABLED = "Disabled"
    GITHUB_H2OGPT = "github h2oGPT"
    H2O_DAI_DOCS = "DriverlessAI docs"
    LLM = "LLM"
    MY_DATA = "MyData"
    USER_DATA = "UserData"
    WIKI = "wiki"
    WIKI_FULL = "wiki_full"


class Client:
    def __init__(self, server_url: str, huggingface_token: Optional[str] = None):
        self._client = gradio_client.Client(
            src=server_url, hf_token=huggingface_token, verbose=False
        )
        self._text_completion = TextCompletion(self)

    @property
    def text_completion(self) -> "TextCompletion":
        return self._text_completion

    def _predict(self, *args, api_name: str) -> str:
        return self._client.submit(*args, api_name=api_name).result()

    async def _predict_async(self, *args, api_name: str) -> str:
        return await asyncio.wrap_future(self._client.submit(*args, api_name=api_name))


class TextCompletion:
    def __init__(self, client: Client):
        self._client = client

    def create(
        self,
        prompt: str,
        prompt_type: PromptType = PromptType.PLAIN,
        input_context_for_instruction: str = "",
        enable_sampler=False,
        temperature: float = 1.0,
        top_p: float = 1.0,
        top_k: int = 40,
        beams: float = 1.0,
        early_stopping: bool = False,
        min_output_length: int = 0,
        max_output_length: int = 128,
        max_time: int = 180,
        repetition_penalty: float = 1.07,
        number_returns: int = 1,
        system_pre_context: str = "",
        langchain_mode: LangChainMode = LangChainMode.DISABLED,
    ) -> str:
        """
        Creates a new text completion.

        :param prompt: text prompt to generate completions for
        :param prompt_type: type of the prompt
        :param input_context_for_instruction: input context for instruction
        :param enable_sampler: enable or disable the sampler, required for use of
                temperature, top_p, top_k
        :param temperature: What sampling temperature to use, between 0 and 3.
                Lower values will make it more focused and deterministic, but may lead
                to repeat. Higher values will make the output more creative, but may
                lead to hallucinations.
        :param top_p: cumulative probability of tokens to sample from
        :param top_k: number of tokens to sample from
        :param beams: Number of searches for optimal overall probability.
                Higher values uses more GPU memory and compute.
        :param early_stopping: whether to stop early or not in beam search
        :param min_output_length: minimum output length
        :param max_output_length: maximum output length
        :param max_time: maximum time to search optimal output
        :param repetition_penalty: penalty for repetition
        :param number_returns:
        :param system_pre_context: directly pre-appended without prompt processing
        :param langchain_mode: LangChain mode
        :return: response from the model
        """
        # Not exposed parameters.
        instruction = ""  # empty when chat_mode is False
        input = ""  # only chat_mode is True
        stream_output = False
        prompt_dict = ""  # empty as prompt_type cannot be 'custom'
        chat_mode = False
        langchain_top_k_docs = 4  # number of document chunks; not public
        langchain_enable_chunk = True  # whether to chunk documents; not public
        langchain_chunk_size = 512  # chunk size for document chunking; not public
        langchain_document_choice = ["All"]

        return self._client._predict(
            instruction,
            input,
            system_pre_context,
            stream_output,
            prompt_type.value,
            prompt_dict,
            temperature,
            top_p,
            top_k,
            beams,
            max_output_length,
            min_output_length,
            early_stopping,
            max_time,
            repetition_penalty,
            number_returns,
            enable_sampler,
            chat_mode,
            prompt,
            input_context_for_instruction,
            langchain_mode.value,
            langchain_top_k_docs,
            langchain_enable_chunk,
            langchain_chunk_size,
            langchain_document_choice,
            api_name="/submit_nochat",
        )

    async def create_async(
        self,
        prompt: str,
        prompt_type: PromptType = PromptType.PLAIN,
        input_context_for_instruction: str = "",
        enable_sampler=False,
        temperature: float = 1.0,
        top_p: float = 1.0,
        top_k: int = 40,
        beams: float = 1.0,
        early_stopping: bool = False,
        min_output_length: int = 0,
        max_output_length: int = 128,
        max_time: int = 180,
        repetition_penalty: float = 1.07,
        number_returns: int = 1,
        system_pre_context: str = "",
        langchain_mode: LangChainMode = LangChainMode.DISABLED,
    ) -> str:
        """
        Creates a new text completion asynchronously.

        :param prompt: text prompt to generate completions for
        :param prompt_type: type of the prompt
        :param input_context_for_instruction: input context for instruction
        :param enable_sampler: enable or disable the sampler, required for use of
                temperature, top_p, top_k
        :param temperature: What sampling temperature to use, between 0 and 3.
                Lower values will make it more focused and deterministic, but may lead
                to repeat. Higher values will make the output more creative, but may
                lead to hallucinations.
        :param top_p: cumulative probability of tokens to sample from
        :param top_k: number of tokens to sample from
        :param beams: Number of searches for optimal overall probability.
                Higher values uses more GPU memory and compute.
        :param early_stopping: whether to stop early or not in beam search
        :param min_output_length: minimum output length
        :param max_output_length: maximum output length
        :param max_time: maximum time to search optimal output
        :param repetition_penalty: penalty for repetition
        :param number_returns:
        :param system_pre_context: directly pre-appended without prompt processing
        :param langchain_mode: LangChain mode
        :return: response from the model
        """
        # Not exposed parameters.
        instruction = ""  # empty when chat_mode is False
        input = ""  # only chat_mode is True
        stream_output = False
        prompt_dict = ""  # empty as prompt_type cannot be 'custom'
        chat_mode = False
        langchain_top_k_docs = 4  # number of document chunks; not public
        langchain_enable_chunk = True  # whether to chunk documents; not public
        langchain_chunk_size = 512  # chunk size for document chunking; not public
        langchain_document_choice = ["All"]

        return await self._client._predict_async(
            instruction,
            input,
            system_pre_context,
            stream_output,
            prompt_type.value,
            prompt_dict,
            temperature,
            top_p,
            top_k,
            beams,
            max_output_length,
            min_output_length,
            early_stopping,
            max_time,
            repetition_penalty,
            number_returns,
            enable_sampler,
            chat_mode,
            prompt,
            input_context_for_instruction,
            langchain_mode.value,
            langchain_top_k_docs,
            langchain_enable_chunk,
            langchain_chunk_size,
            langchain_document_choice,
            api_name="/submit_nochat",
        )
