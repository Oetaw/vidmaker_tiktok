import praw


def get_reddit_content(thread_url, num_posts=5):
    # Ustawienia aplikacji na stronie Reddit: https://www.reddit.com/prefs/apps
    reddit = praw.Reddit(client_id='h-iyjSq2sYdvLo8QcVbu-g',
                         client_secret='oeU1y3X8bGiOipZ5J2DJL8tkQfQPTA',
                         user_agent='web app')

    # Wyciąganie zawartości z subredditu
    submission = reddit.submission(url=thread_url)
    print(f'Tytuł wątku: {submission.title}\n')
    print(f'Treść pierwotnego postu: {submission.selftext}')


# Przykład użycia
reddit_url = 'https://www.reddit.com/r/stories/comments/17yonnz/one_of_my_dogs_ran_after_god_knows_what_at_night/?utm_source=share&utm_medium=web2x&context=3'  # Możesz zastąpić 'python' nazwą interesującego cię subredditu
get_reddit_content(reddit_url)
def reddit_stories():
    Story = input("give me a Story")