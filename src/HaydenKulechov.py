import os
import time
from typing import Optional, Dict, Any
import json
from virtuals_sdk.game import Agent

class AgentRunner:
    def __init__(
        self,
        api_key: str,
        goal: str,
        description: str,
        world_info: str,
        platform: str = "telegram",
        session_id: Optional[str] = None,
        state_file: str = "agent_state.json"
    ):
        self.agent = Agent(
            api_key=api_key,
            goal=goal,
            description=description,
            world_info=world_info
        )
        self.platform = platform
        self.session_id = session_id or f"session-{int(time.time())}"
        self.state_file = state_file
        self.state: Dict[str, Any] = self.load_state()

    def load_state(self) -> Dict[str, Any]:
        """Load agent state from file if exists"""
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_state(self):
        """Save current agent state to file"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)

    def setup_functions(self):
        """Configure agent functions - customize this based on your needs"""
        if self.platform == "telegram":
            # Example: Set up Telegram functions
            from virtuals_sdk.functions.telegram import TelegramClient
            tg_client = TelegramClient(bot_token=os.getenv("TELEGRAM_BOT_TOKEN"))
            
            # Add required functions
            self.agent.add_custom_function(tg_client.get_function("send_message"))
            self.agent.add_custom_function(tg_client.get_function("create_poll"))
        
        elif self.platform == "twitter":
            # Example: Set up Twitter functions
            self.agent.use_default_twitter_functions(["wait", "reply_tweet"])
            
    def run_forever(self, interval: int = 60):
        """Run the agent in an infinite loop"""
        self.setup_functions()
        
        print(f"Starting agent loop for platform: {self.platform}")
        print(f"Session ID: {self.session_id}")
        
        while True:
            try:
                if self.platform == "twitter":
                    response = self.agent.simulate_twitter(self.session_id)
                else:
                    # For other platforms, use the react method
                    response = self.agent.react(
                        session_id=self.session_id,
                        platform=self.platform,
                        task="Monitor and engage with users appropriately",
                        event=None  # You might want to fetch events from your platform here
                    )
                
                # Process response if needed
                print(f"Agent response: {response}")
                
                # Save state
                self.state['last_response'] = response
                self.state['last_run'] = time.time()
                self.save_state()
                
                # Wait before next iteration
                time.sleep(interval)
                
            except Exception as e:
                print(f"Error in agent loop: {e}")
                time.sleep(interval)  # Continue loop even after error

def main():
    # Initialize and run agent
    runner = AgentRunner(
        api_key=os.getenv("VIRTUALS_API_KEY"),
        goal="Help users and provide valuable interactions",
        description="A helpful assistant that engages with users",
        world_info="A digital environment where the agent helps users with their queries",
        platform="telegram"  # or "twitter"
    )
    
    runner.run_forever(interval=60)

if __name__ == "__main__":
    main()