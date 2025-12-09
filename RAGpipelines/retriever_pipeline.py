import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


load_dotenv()

def get_api_key():
    key = os.getenv("GOOGLE_API_KEY")
    if key and key.strip():
        return key.strip()
    return key


class ChatClient:
    def __init__(self, api_key: str = None, model_name: str = 'gemini-2.5-flash', temperature: float = 0.6):
        self.api_key = api_key or get_api_key()
        self.model_name = model_name
        self.temperature = temperature

        self.model = ChatGoogleGenerativeAI(
            model = self.model_name,
            api_key = self.api_key,
            temperature = self.temperature
        )

    def send(self, prompt: str) -> str:
        """Send a single-user prompt and return the response text."""
        if not isinstance(prompt, str):
            raise ValueError("prompt must be string.")
        response = self.model.invoke(prompt)
        # Many LangChain wrappers return an object with `.content`; adapt if necessary.
        return getattr(response, "content", str(response))
    
    def send_with_roles(self, system_prompt: str, user_prompt: str) -> str:
        """
        Send a role-based request (system + human)
        Example: system -> "You are a helpful assistant."
                 user -> "Explain X in simple terms."
        """

        messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
        response = self.model.invoke(messages)
        return getattr(response, "content", str(response))
    
    def     1(self, messages_list: list) -> str:
        """
        Send a list of langchain_core.messages objects (SystemMessage, HumanMessage, AIMessage).
        Example:
            messages = [
                SystemMessage(content="You're a helpful assistant."),
                HumanMessage(content="Who won the world cup?"),
            ]
        """
        if not isinstance(messages_list, list):
            raise ValueError("messages_list must be a list of message objects")
        response = self.model.invoke(messages_list)
        return getattr(response, "content", str(response))
    
    def stream(self, prompt: str):
        """
        Stream token-by-token (or chunk-by-chunk) responses.
        Yields chunks (strings). Caller can print them progressively.
        """
        for chunk in self.model.stream(prompt):
            # chunk may be a message-like object; extract textual content if possible
            text = getattr(chunk, "content", None)
            if text is None:
                # If chunk is a primitive or dict
                try:
                    text = str(chunk)
                except Exception:
                    text = ""
            yield text
    
    def interactive_cli(self):
        """Minimal interactive CLI loop (supports '/stream' prefix for streaming)."""
        print("Gemini Chat CLI — type your prompt and press Enter.")
        print("Commands: /exit to quit, /stream <prompt> to stream, /role to send with system prompt")
        while True:
            try:
                user_input = input("\nYou: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting.")
                break

            if not user_input:
                continue

            if user_input.lower() in ("/exit", "exit", "quit"):
                print("Goodbye.")
                break

            if user_input.startswith("/stream "):
                prompt = user_input[len("/stream ") :].strip()
                print("Streaming response:")
                try:
                    for piece in self.stream(prompt):
                        print(piece, end="", flush=True)
                    print()  # newline after stream completes
                except Exception as e:
                    print(f"\n[stream error] {e}")
                continue

            if user_input.startswith("/role "):
                # usage: /role System instruction || user prompt
                payload = user_input[len("/role ") :].split("||", 1)
                if len(payload) != 2:
                    print("Usage: /role <system prompt> || <user prompt>")
                    continue
                system_prompt, user_prompt = payload[0].strip(), payload[1].strip()
                try:
                    reply = self.send_with_roles(system_prompt, user_prompt)
                    print("\nAI:", reply)
                except Exception as e:
                    print(f"[error] {e}")
                continue

            # default: basic send
            try:
                reply = self.send(user_input)
                print("\nAI:", reply)
            except Exception as e:
                print(f"[error] {e}")


if __name__ == "__main__":
    # Example usage
    try:
        api_key = get_api_key()
        client = ChatClient(api_key=api_key, model_name="gemini-2.5-flash", temperature=0.6)

        # quick demo: single prompt
        demo_prompt = "Explain the OSI model in simple terms (short)."
        print("Demo prompt ->", demo_prompt)
        print("Response:\n", client.send(demo_prompt))

        # start interactive CLI after demo
        client.interactive_cli()

    except Exception as exc:
        print("Initialization error:", exc)
        raise
