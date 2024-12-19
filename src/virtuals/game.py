from typing import List, Dict, Optional, Union, Set
from dataclasses import dataclass, asdict
import json
import uuid
import sdk


@dataclass
class FunctionArgument:
    name: str
    description: str
    type: str
    id: str = None
    
    def __post_init__(self):
        self.id = self.id or str(uuid.uuid4())


@dataclass
class FunctionConfig:
    method: str = "get"
    url: str = ""
    headers: Dict = None
    payload: Dict = None
    success_feedback: str = ""
    error_feedback: str = ""
    isMainLoop: bool = False
    isReaction: bool = False
    headersString: str = "{}"  # Added field
    payloadString: str = "{}"  # Added field
    platform: str = None

    def __post_init__(self):
        self.headers = self.headers or {}
        self.payload = self.payload or {}

        self.headersString = json.dumps(self.headers, indent=4)
        self.payloadString = json.dumps(self.payload, indent=4)


@dataclass
class Function:
    fn_name: str
    fn_description: str
    args: List[FunctionArgument]
    config: FunctionConfig
    hint: str = ""
    id: str = None

    def __post_init__(self):
        self.id = self.id or str(uuid.uuid4())
        
    def toJson(self):
        return {
            "id": self.id,
            "fn_name": self.fn_name,
            "fn_description": self.fn_description,
            "args": [asdict(arg) for arg in self.args],
            "hint": self.hint,
            "config": asdict(self.config)
        }

class Agent:
    def __init__(
        self,
        api_key: str,
        goal: str = "",
        description: str = "",
        world_info: str = "",
    ):
        self.game_sdk = sdk.GameSDK(api_key)
        self.goal = goal
        self.description = description
        self.world_info = world_info
        self.enabled_functions: List[str] = []
        self.custom_functions: List[Function] = []

    def set_goal(self, goal: str):
        self.goal = goal
        return True
    
    def set_description(self, description: str):
        self.description = description
        return True
    
    def set_world_info(self, world_info: str):
        self.world_info = world_info
        return True

    def get_goal(self) -> str:
        return self.goal
    
    def get_description(self) -> str:
        return self.description
    
    def get_world_info(self) -> str:
        return self.world_info

    def list_available_default_twitter_functions(self) -> Dict[str, str]:
        """
        List all of the default functions (currently default functions are only available for Twitter/X platform)
        TODO: will be moved to another layer of abstraction later
        """
        # Combine built-in and custom function descriptions
        return self.game_sdk.functions()

    def use_default_twitter_functions(self, functions: List[str]):
        """
        Enable built-in functions by default
        """
        self.enabled_functions = functions
        return True

    def add_custom_function(self, custom_function: Function) -> bool:
        """
        Add a custom function to the agent
        Custom functions are automatically added and enabled
        """
        # Add to custom functions list
        self.custom_functions.append(custom_function)

        return True

    def simulate_twitter(self, session_id: str):
        """
        Simulate the agent configuration for Twitter
        """
        return self.game_sdk.simulate(
            session_id,
            self.goal,
            self.description,
            self.world_info,
            self.enabled_functions,
            self.custom_functions
        )

    def react(self, session_id: str, platform: str, tweet_id: str = None, event: str = None, task: str = None):
        """
        React to a tweet
        """
        return self.game_sdk.react(
            session_id=session_id,
            platform=platform,
            event=event,
            task=task,
            tweet_id=tweet_id,
            goal=self.goal,
            description=self.description,
            world_info=self.world_info,
            functions=self.enabled_functions,
            custom_functions=self.custom_functions
        )

    def deploy_twitter(self):
        """
        Deploy the agent configuration
        """
        return self.game_sdk.deploy(
            self.goal,
            self.description,
            self.world_info,
            self.enabled_functions,
            self.custom_functions
        )

    def export(self) -> str:
        """Export the agent configuration as JSON string"""
        export_dict = {
            "goal": self.goal,
            "description": self.description,
            "worldInfo": self.world_info,
            "functions": self.enabled_functions,
            "customFunctions": [
                {
                    "id": func.id,
                    "fn_name": func.fn_name,
                    "fn_description": func.fn_description,
                    "args": [asdict(arg) for arg in func.args],
                    "hint": func.hint,
                    "config": asdict(func.config)
                }
                for func in self.custom_functions
            ]
        }
        agent_json = json.dumps(export_dict, indent=4)

        # save to file
        with open('agent.json', 'w') as f:
            f.write(agent_json)

        return agent_json
