""" Basic blog using webpy 0.3 """
import web
import model
__author__ = 'knuthy'


### Url mappings

urls = (
    '^/?', 'Index',
    '^/article/(.+)/?$', 'Article',
    '^/search/$', 'Search',
)


### Templates
t_globals = {
    'datestr': web.datestr
}

render = web.template.render('templates', base='base', globals=t_globals)
mod = model.Model()


class Index:

    def GET(self):
        """ Show page """
        posts = mod.get_posts()
        return render.index(posts)

class Article:

    def GET(self, id):
        """ Show an article
        """
        post = mod.get_post(id)
        return render.article(post)

class Search:

    def GET(self):
        terms = web.ctx.query[1:].split('q=')[1]
        # replace + by spaces
        terms = terms.replace('+', ' ')
        print terms
        posts = mod.search(terms)
        return render.index(posts)

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()