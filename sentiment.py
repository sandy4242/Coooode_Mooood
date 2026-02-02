from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import defaultdict

class CommitSentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze_commit(self, message):
        """Analyze single commit message"""
        scores = self.analyzer.polarity_scores(message)
        
        # Determine dominant emotion
        compound = scores['compound']
        if compound >= 0.05:
            emotion = 'positive'
        elif compound <= -0.05:
            emotion = 'negative'
        else:
            emotion = 'neutral'
            
        return {
            'emotion': emotion,
            'compound': compound,
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu']
        }
    
    def analyze_commits(self, commits):
        """Analyze multiple commits"""
        results = []
        for commit in commits:
            sentiment = self.analyze_commit(commit['message'])
            results.append({
                **commit,
                **sentiment
            })
        return results
    
    def get_mood_summary(self, analyzed_commits):
        """Get overall mood statistics"""
        emotions = [c['emotion'] for c in analyzed_commits]
        mood_counts = defaultdict(int)
        for emotion in emotions:
            mood_counts[emotion] += 1
        
        total = len(emotions)
        return {
            'total_commits': total,
            'positive': mood_counts['positive'],
            'negative': mood_counts['negative'],
            'neutral': mood_counts['neutral'],
            'positive_pct': round(mood_counts['positive']/total*100, 1) if total else 0,
            'negative_pct': round(mood_counts['negative']/total*100, 1) if total else 0
        }

# Test function
if __name__ == "__main__":
    analyzer = CommitSentimentAnalyzer()
    test_messages = [
        "Fixed annoying bug finally!",
        "WIP: struggling with authentication",
        "Added new feature for users"
    ]
    for msg in test_messages:
        result = analyzer.analyze_commit(msg)
        print(f"{msg} -> {result['emotion']} ({result['compound']:.2f})")
