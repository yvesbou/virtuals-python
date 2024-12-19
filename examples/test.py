import os
from virtuals_sdk import game

agent = game.Agent(
    api_key=os.environ.get("VIRTUALS_API_KEY"),
    goal="search for best songs",
    description="Test Description",
    world_info="Test World Info"
)

# applicable only for twitter
agent.list_available_default_twitter_functions()
agent.use_default_twitter_functions(["wait", "reply_tweet"])

# adding custom functions only for platform twitter
agent.add_custom_function(
    game.Function(
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
)

# running reaction module only for platform twitter
print(agent.react(session_id="session-twitter",
      platform="twitter",
      tweet_id="1869281466628349975"))
print(agent.simulate_twitter(session_id="session-twitter"))


# running reaction module only for other platforms
# adding custom functions only for other platforms
agent.add_custom_function(
    game.Function(
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
            # this function will only be used for telegram
            platform="telegram",
            success_feedback="I found the best songs",
            error_feedback="I couldn't find the best songs",
        )
    )
)

# running reaction module only for platform telegram
print(agent.react(session_id="session-telegram",
      platform="telegram",  # specify the platform telegram
      event="message from user: give me some great music?",
      task="reply with a music recommendation"))
