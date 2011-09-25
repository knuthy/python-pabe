import  markdown, time, re
import logging as log
from git import *
from pygments import highlight
from pygments.lexers import PythonLexer, guess_lexer
from pygments.formatters import HtmlFormatter
from utils import *


__author__ = 'knuthy'

repo = Repo('articles', odbt=GitCmdObjectDB)

if repo.is_dirty() :
    log.warning("Your repo is a little bit dirty, commit your changes")
    log.warning("We will work with the latest commit")


# our database
# in a hash format so we can do db['my_id'] to get the post
db = {}
chex = ''

def _load_db():
    global db
    global chex

    master = repo.heads.master
    chex = master.commit.hexsha

    blobs = master.commit.tree.blobs
    for blob in blobs:
        content = blob.data_stream.read()
        parts = content.split("\n")

        try:
            #just to check that it's a markdown file
            blob.name.index('.md')
            id = blob.name.split('.md')[0]
        except:
            log.error("File %s is not a markdown file. Move it from here!"% blob.name)
            continue

        md = "\n".join(parts[6:])

        # replace <pre><code>...<code></pre> by <pre class="prettyprint">...</pre>
        codes = re.findall("(?:\n\n|^)((?:(?:[ ]{4}|\t).*\n+)+)(\n*[ ]{0,3}[^ \t\n]|(?=~0))", md)
        for c in codes:
            code = c[0]
            lexer = guess_lexer(code)
            pret = highlight(code, lexer, HtmlFormatter(style='colorful', cssclass='code'))
            md = md.replace(code, pret)

        html = markdown.markdown(md)
        title = ""
        author = ""
        date = ""
        tags = []
        categories = []

        try:
            title = parts[0].split(':')[1].strip()
            author = parts[1].split(':')[1].strip()
            date = ':'.join(parts[2].split(':')[1:]).strip()
            time_stamp = time.strptime(date, "%H:%M %d/%m/%Y")
        except Exception as err:
            log.error("parsing failed with %s"%blob.name)
            log.error("err.message")
            #we were unable to parse it correctly then skip it
            continue

        db[id] = {
            'title' : title,
            'author': author,
            'date': date,
            'time_stamp': time_stamp,
            'html': html
        }



_load_db()


def get_posts():
    global chex
    master = repo.heads.master
    if master.commit.hexsha != chex:
        global db
        db = {}
        _load_db()
        print db
        chex = master.commit.hexsha

    #convert to list first
    db_list = []
    for k, v in db.iteritems():
        temp = v
        v['id'] = k
        db_list.append(v)
    # sort the database by date
    db_list.sort(key=lambda e: e['time_stamp'],reverse=True)
    return db_list

def get_post(id):
    global chex
    master = repo.heads.master
    if repo.head.commit.hexsha != chex:
        _load_db()
        chex = master.commit.hexsha

    post = db[id]
    post['id'] = id
    try:
        return post
    except KeyError:
        return None

def search(terms, where='all'):
    global chex
    master = repo.heads.master
    if repo.head.commit.hexsha != chex:
        _load_db()
        chex = master.commit.hexsha

    #for security reasons, I don't trust verry much the git.execute()
    #replace the ';' that ends a command
    re.sub("[;\'\"\%\?]", ' ', terms)
    result = repo.git.execute(["git", "grep","-i",terms])
    result = result.split("\n")
    articles = [article.split('.md')[0] for article in result]
    articles = uniquify(articles)
    posts = [get_post(id) for id in articles]
    posts.sort(key=lambda e: e['time_stamp'],reverse=True)
    return posts
