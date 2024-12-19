# Overview

If you wish to have your applications powered by Agent using GAME, you may use GAME python SDK to build your application. 

<aside>
💡 To best understand this walkthrough, please go through the previous section on 
	[agent configurations in GAME](https://www.notion.so/1592d2a429e98016b389ea26b53686a3) to better understand the configurable components.

</aside>

## Create an API key

Open the [Virtuals Platform](https://app.virtuals.io/) and create/get an API key from the Virtuals Sandbox by clicking “Access G.A.M.E API” 

![Screenshot 2024-12-19 at 7.43.26 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/12f7bb5a-d953-4ff0-8718-ebe6b3499c01/b7be714a-a3e7-4f30-a7dd-5ac8e7c17066/Screenshot_2024-12-19_at_7.43.26_PM.png)

Store the key in a safe location, like a `.bashrc` or a `.zshrc` file. 

```bash
export VIRTUALS_API_KEY="your_virtuals_api_key"
```

Alternatively, you can also use a `.env` file ([`python-dotenv` package](https://github.com/theskumar/python-dotenv) to store and load the key) if you are using the Virtuals Python SDK.

## Installation

install our python SDK using pip

```bash
pip install virtuals_sdk
```

## Usage (GAME)

SDK can be used for multiple use cases: 

1. Update the existing Agent in Twitter environment 
2. Build on other platforms using GAME. 

### Update the existing Agent in Twitter environment

The SDK provides another interface to configure agents that is more friendly to developers. This is similar to configuring your agent in the [Agent Sandbox](https://game-lite.virtuals.io/).

```python
from virtuals_sdk.game import Agent

# Create agent with just strings for each component
agent = Agent(
		api_key=VIRTUALS_API_KEY,
    goal="Autonomously analyze crypto markets and provide trading insights",
    description="HODL-9000: A meme-loving trading bot powered by hopium and ramen",
    world_info="Virtual crypto trading environment where 1 DOGE = 1 DOGE"
)
```

You can also initialize the agent first with just the API key and set the goals, descriptions and world information separately and check the current agent descriptions if needed. 

```python

agent = Agent(api_key=VIRTUALS_API_KEY)

# check what is current goal, descriptions and world_info
agent.get_goal()
agent.get_description()
agent.get_world_info()

# Set components individually - set change the agent goal/description/worldinfo
agent.set_goal("Autonomously analyze crypto markets and provide trading insights")
agent.set_description("HODL-9000: A meme-loving trading bot powered by hopium and ramen")
agent.set_world_info("Virtual crypto trading environment where 1 DOGE = 1 DOGE")

# check what is current goal, descriptions and world_info
agent.get_goal()
agent.get_description()
agent.get_world_info()
```

### Functions

By default, there are no functions enabled when the agent is initialized (i.e. the agent has no actions/functions it can execute). There are a list of available and provided functions for the Twitter/X platform and you can set them.

```python
print(agent.list_available_default_twitter_functions())

# enable some functions for the agent to use
agent.use_default_twitter_functions(["wait", "reply_tweet"])
```

You can then equip the agent with some custom functions as follows:

```python

search_function = game.Function(
        fn_name="custom_search_internet",
        fn_description="search the internet for the best songs",
        args=[
            game.FunctionArgument(
                name="query",
                type="string",
                description="The query to search for"
            )
        ],
        config=game.FunctionConfig(
            method="get",
            url="https://google.com",
            platform="twitter", # specify which platform this function is for, in this case this function is for twitter only
            success_feedback="I found the best songs",
            error_feedback="I couldn't find the best songs",
        )
    )

# adding custom functions only for platform twitter
agent.add_custom_function(search_function)
```

### Evaluate with Simulate, Deploy

You can simulate one step of the agentic loop on Twitter/X with your new configurations and see the outputs. This is similar to the simulate button on the [Agent Sandbox](https://game-lite.virtuals.io/). Hence, when running

```python
# Simulate one step of the full agentic loop on Twitter/X from the HLP -> LLP -> action (NOTE: supported for Twitter/X only now)
response = agent.simulate_twitter(session_id="123")

# To more realistically simulate deployment you can
```

```python
# Simulate response to a certain event
response = agent.react(
	session_id="567", # string identifier that you decide
	task_description="",
	context="",
	platform="",
)
```

Once you are happy, `deploy_twitter` will push your agent configurations to production and run your agent on Twitter/X autonomously.

```python
# deploy agent! (NOTE: supported for Twitter/X only now)
agent.deploy_twitter()
```

## Build on other platforms using GAME

`simulate_twitter` and `deploy_twitter` runs through the entire GAME stack from HLP → LLP→ action/function selected. However, these agent functionalities are currently for the Twitter/X platform. You may utilize Task-based Agent with Low-Level Planner and Reaction Module to develop applications that are powered by GAME. The Low Level Planner (LLP) of the agent (please see [documentation](https://www.notion.so/1592d2a429e98016b389ea26b53686a3?pvs=21) for more details on GAME and LLP) can separately act as a decision making engine based on a task description and event occurring. This agentic architecture is simpler but also sufficient for many applications. 

We are releasing this simpler setup as a more generalised/platform agnostic framework (not specific to Twitter/X). The entire GAME stack along with the HLP will be opened up to be fully configurable and platform agnostic in the coming weeks.

<aside>
🖥️ Low-Level Planner (LLP) as a Task-based Agent

![llp.png](/llp.png)

</aside>

After configuring the agent’s character card or description and setting up the agents functions, we can then use the `react` method to get an agent to respond and execute a sequence of actions based on the task description provided and the context. Between each action in the sequence, the agent only receives the `success_feedback` and `error_feedback` of each function executed.

```python
# React/respond to a certain event
response = agent.react(
	session_id="567", # string identifier that you decide
	task_description="",
	context="Hi how are you?",
	platform="TELEGRAM",
)
```

<aside>
⚠️ Remember that the `platform` tag determines what functions are available to the agent. The agent will have access to functions that have the same `platform` tag. All the default available functions listed on `agent.list_available_default_twitter_functions()` and set via `agent.use_default_twitter_functions()` have the `platform` tag of “twitter”.

</aside>

## Arguments Definition

### Session ID

The session ID is an identifier for an instance of the agent. When using the same session ID, it maintains and picks up from where it last left off, continuing the session/instance. It should be split per user/ conversation that you are maintaining on your platform. For different platforms, different session ID can be used. 

### Platform Tag

When adding custom functions, and when calling the react agent (i.e. LLP), there is a platform tag that can be defined. This acts like a filter for the functions available that is passed to the agent. You should define the platform when passing in the events.

### Task Description

Task description serves as the prompt for the agent to respond. Since the reaction can be platform-based, you can define task description based on the platforms. In the task description, you should pass in any related info that require agent to make decision. That should include:

- User message
- Conversation history
- Instructions
