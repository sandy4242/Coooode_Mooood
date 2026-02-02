import click
from rich.console import Console
from rich.table import Table
from git_parser import get_commits
from sentiment import CommitSentimentAnalyzer
from spotify_api import SpotifyMoodPlaylist
from datetime import datetime

console = Console()

@click.group()
def cli():
    """CodeMood - Emotion-based playlist generator from git commits"""
    pass

@cli.command()
@click.option('--days', default=30, help='Number of days to analyze')
@click.option('--repo', default='.', help='Repository path')
def analyze(days, repo):
    """Analyze commit emotions"""
    console.print(f"[bold cyan]Analyzing commits from last {days} days...[/bold cyan]")
    
    # Get commits
    commits = get_commits(repo, days)
    if not commits:
        console.print("[red]No commits found![/red]")
        return
    
    # Analyze sentiment
    analyzer = CommitSentimentAnalyzer()
    analyzed = analyzer.analyze_commits(commits)
    summary = analyzer.get_mood_summary(analyzed)
    
    # Display results
    console.print(f"\n[bold]Total commits:[/bold] {summary['total_commits']}")
    console.print(f"[green]Positive:[/green] {summary['positive']} ({summary['positive_pct']}%)")
    console.print(f"[red]Negative:[/red] {summary['negative']} ({summary['negative_pct']}%)")
    console.print(f"[yellow]Neutral:[/yellow] {summary['neutral']}")
    
    # Show recent commits with emotions
    table = Table(title="\nRecent Commits")
    table.add_column("Date", style="cyan")
    table.add_column("Message", style="white")
    table.add_column("Emotion", style="bold")
    
    for c in analyzed[:10]:
        emotion_color = {'positive': 'green', 'negative': 'red', 'neutral': 'yellow'}
        table.add_row(
            c['date'].strftime('%Y-%m-%d'),
            c['message'][:50],
            f"[{emotion_color[c['emotion']]}]{c['emotion']}[/{emotion_color[c['emotion']]}]"
        )
    
    console.print(table)

@cli.command()
@click.option('--days', default=30, help='Number of days to analyze')
@click.option('--repo', default='.', help='Repository path')
def playlist(days, repo):
    """Generate Spotify playlist from commit emotions"""
    console.print("[bold cyan]Generating mood playlist...[/bold cyan]")
    
    # Analyze commits
    commits = get_commits(repo, days)
    if not commits:
        console.print("[red]No commits found![/red]")
        return
    
    analyzer = CommitSentimentAnalyzer()
    analyzed = analyzer.analyze_commits(commits)
    summary = analyzer.get_mood_summary(analyzed)
    
    # Determine dominant mood
    if summary['positive_pct'] > 50:
        dominant_mood = 'positive'
    elif summary['negative_pct'] > 30:
        dominant_mood = 'negative'
    else:
        dominant_mood = 'neutral'
    
    console.print(f"[bold]Dominant mood:[/bold] {dominant_mood}")
    
    # Create playlist
    sp = SpotifyMoodPlaylist()
    tracks = sp.get_mood_tracks(dominant_mood, count=20)
    
    playlist_name = f"CodeMood - {datetime.now().strftime('%b %Y')}"
    description = f"Generated from {summary['total_commits']} commits ({summary['positive_pct']}% positive)"
    
    url = sp.create_mood_playlist(playlist_name, description, tracks)
    
    console.print(f"\n[green]✓ Playlist created![/green]")
    console.print(f"[link={url}]{url}[/link]")

if __name__ == '__main__':
    cli()
