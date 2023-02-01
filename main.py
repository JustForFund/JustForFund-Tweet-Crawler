from load_global import load_todo
from analyse_compiled_tweets import sentiment_analysis
from tweet_informant import get_tweets
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess as cmd


def job():
	load_todo()
	sentiment_analysis()
	get_tweets()


if __name__ == '__main__':
	while True:
		job()