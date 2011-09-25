import  markdown, time, re
import logging as log
from git import *
from pygments import highlight
from pygments.lexers import PythonLexer, guess_lexer
from pygments.formatters import HtmlFormatter
from utils import *

class Model:
    def __init__(self, base_dir = 'articles'):
        self.repo = Repo(base_dir, odbt=GitCmdObjectDB)

        if self.repo.is_dirty() :
            log.warning("Your repo is a little bit dirty, commit your changes")
            log.warning("We will work with the latest commit")


        # our database
        # in a hash format so we can do db['my_id'] to get the post
        self.db = {}
        self.chex = ''
        self._load_db()

    def _load_db(self):
        """
        Loads the articles into a single dictionary "db"
        such as db['my_id'] contains the data of the article with "my_id" as name
        """
        master = self.repo.heads.master
        self.chex = master.commit.hexsha

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

            self.db[id] = {
                'title' : title,
                'author': author,
                'date': date,
                'time_stamp': time_stamp,
                'html': html
            }

    def _reload_db(self):
        """
        when the sha codes are different it means that there were a update
        of the repository, we should then re-load the posts
        """
        master = self.repo.heads.master
        if master.commit.hexsha != self.chex:
            self.db = {}
            _load_db()
            self.chex = master.commit.hexsha

    def get_posts(self):
        self._reload_db()

        #convert to list first
        db_list = []
        for k, v in self.db.iteritems():
            temp = v
            temp['id'] = k
            db_list.append(temp)
            # sort the database by date
        db_list.sort(key=lambda e: e['time_stamp'],reverse=True)
        return db_list




    def get_post(self, id):
        self._reload_db()

        post = self.db[id]
        post['id'] = id
        try:
            return post
        except KeyError:
            return None

    def search(self, terms, where='all'):
        self._reload_db()

        #for security reasons, I don't trust verry much the git.execute()
        #replace the ';' that ends a command
        re.sub("[;\'\"\%\?]", ' ', terms)
        result = self.repo.git.execute(["git", "grep","-i",terms])
        result = result.split("\n")
        articles = [article.split('.md')[0] for article in result]
        articles = uniquify(articles)
        posts = [get_post(id) for id in articles]
        posts.sort(key=lambda e: e['time_stamp'],reverse=True)
        return posts
