from flask import Blueprint, render_template, request, flash, jsonify
from app.rssapp import tasks
from app.rssapp.models import Feed
import datetime
from app.extensions import db

rss_bp = Blueprint('rss_bp', __name__, template_folder='templates',
                    static_folder='static')

@rss_bp.route('/task')
def task():
    feeds = Feed.query.filter_by(status=1)

    for feed in feeds:
        tasks.fetch_articles.delay(feed.id)

    flash('Fetch articles task kicked off')
    return render_template('core/base.html')


@rss_bp.route('/new-task', methods=['GET', 'POST'])
def new_task():
    title = request.args.get('title')
    url = request.args.get('url')

    feed = Feed(
        title=title, status=1, url=url, type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed)

    db.session.commit()

    tasks.fetch_articles.delay(feed.id)

    return jsonify({'message': 'Feed created.', 'feed_id': feed.id})
