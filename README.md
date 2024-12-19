# Virtuals Python API Library
The Virtuals Python API Library is a Python library that provides a simple way to interact with the Virtuals API. 

Currently, this library supports the GAME API for configuring and deploying agents on the [Virtuals Platform](https://virtuals.io). This complements and extends the functionality of the [Agent Sandbox](https://sandbox.virtuals.io) by providing another way to evaluate and develop agents on Virtuals. With more programmatic interactions, this opens up more functionalities and possibilities to integrate it into your own applications.

## Documentation
For a walkthrough of some documentation and SDK and usage, please refer to the notion [documentation]() page.

## Installation
```bash
pip install virtuals_sdk
```

## Usage
```python
from virtuals_sdk.game import Agent

# Create agent with just strings for each component
agent = Agent(
		api_key=VIRTUALS_API_KEY,
    goal="Autonomously analyze crypto markets and provide trading insights",
    description="HODL-9000: A meme-loving trading bot powered by hopium and ramen",
    world_info="Virtual crypto trading environment where 1 DOGE = 1 DOGE"
)

# list available functions that can be added to agent
print(agent.list_available_default_twitter_functions()) # ['wait', 'reply_tweet', 'retweet', 'like_tweet', ...]

# selects functions to be enabled
agent.use_default_twitter_functions(["wait", "reply_tweet"])

# Simulate one step of the full agentic loop on Twitter/X from the HLP -> LLP -> action
response = agent.simulate_twitter(session_id="123")

# deploy agent! (NOTE: supported for Twitter/X only now)
agent.deploy_twitter()
```