from agents.watch_agent import Watch8004Agent

class MyCustomAgent(Watch8004Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capabilities.append("sentiment_analysis")
    
    def analyze_sentiment(self, text):
        # Your custom logic here
        return {"sentiment": "positive", "score": 0.85}

# Use it
agent = MyCustomAgent(name="MySentimentBot")
result = agent.analyze_sentiment("Bitcoin is going to the moon!")
