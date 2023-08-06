# almoststatic
import datetime
import os
import copy
import glob
import time
import json

import yaml
import markdown
import flask

from jinja2 import Environment, FileSystemLoader


class Almoststatic():
    """Almoststatic uses Jinja2 template system to build web pages and web
    sites.

    Pages are declared in yaml files and rendered with Jinja2 template files,
    the "content" directory contain all is needed to do the job, the
    "config.yaml" is used to share global parameters and to tune configuration.
    """

    # list of names of metadata recognized for each page
    meta_names = ['filename', 'pagename', 'title', 'description', 'author',
                  'templ_name', 'extends', 'cacheable', 'date', 'blog']

    def __init__(self):

        # ------------------------------------------------------ config fields
        self.content = "content"
        """str: root directory for content"""

        self.templates = "templates"
        """str: folder used by jinja3 to fin templates"""

        self.templ_name = "page.html"
        """str: default template used to render pages"""

        self.pages = "pages"
        """str: subfolder which contain yaml page files"""

        self.media = "media"
        """str: subfolder used to store media files"""

        self.static_url = ""
        """str: default url prefix for static pages"""

        self.cache = True
        """bool: global enable or disable cache"""

        self.quote_escape = '^^'
        """str: sequence for quote escape in markdown translation"""

        # ------------------------------------------------------ runtime fields
        self.media_prefix = None
        """str | None: starting directory name to force url location for media
                       files when writing static pages"""

        self.cached = {}
        """dict: list of cached pages, recalculated only once"""

        self.vars = {}
        """dict: shortcut for self.env.globals, used to store global vars for
                 templates"""

        self.was_cached = False
        """bool: tell if the last rendered page was cached (mainly for debug
                 reasons)"""

        self.extra_args = {}
        """dict: extra args for current page, internally used to render extra
                 args passed to build_page method"""

        self.page = {}
        """dict: current page during rendering"""

    def load_config(self, config_file="./content/config.yaml"):
        """Load the yaml config file and set some configuration settings.

        It is mandatory to use it at least once. It can update default
        configuration values and config page globals.

        During development config file can change often, so can be useful to
        call it each time the page is reloaded.

        It also configure the environment for Jinja2 and setup some utilities
        that can be used in templates.

        Args:
            config_file (str): name and path of config file
        """

        # read config fields
        with open(config_file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        if 'config' not in config:
            config['config'] = {}
        self.content = config['config'].get("content", self.content)
        self.templates = config['config'].get("templates", self.templates)
        self.templ_name = config['config'].get("templ_name", self.templ_name)
        self.pages = config['config'].get("pages", self.pages)
        self.media = config['config'].get("media", self.media)
        self.static_url = config['config'].get("static_url", self.static_url)
        self.cache = config['config'].get("cache", self.cache)

        # set the environment and add globals
        self.env = Environment(
            loader=FileSystemLoader(self.templates),
            autoescape=False
        )
        # set globals shortcut
        self.vars = self.env.globals

        # load global vars from config.yaml
        self.vars['meta'] = {}
        for k, v in config.items():
            self.env.globals[k] = v
        # and add config as a dict
        self.vars['config'] = config

        # global configuration
        self.vars['is_static'] = False
        """bool: method write_static set this to True and this let to know to
                 templates when we are writing static pages."""

        self.vars['url_prefix'] = ""
        """str: prefix for url's by default it is the root of site, but during
                writing static pages this change to site url."""

        self.vars['url_suffix'] = ""
        """str: suffix for url's by default is empty, but during writing static
                pages it will be changed to ".html" """

        # functions added to templates
        self.vars['enum_list'] = enumerate
        self.vars['len_list'] = len
        self.vars['iif'] = iif
        self.vars['if_in'] = if_in
        self.vars['get_markdown'] = self.get_markdown
        self.vars['get_media'] = self.get_media
        self.vars['include'] = self._import_file
        self.vars['embed'] = self.render_content
        self.vars['particle'] = self.particle
        self.vars['get_url'] = self.get_url
        self.vars['query_blog'] = self.query_blog
        self.vars['pages_id'] = self.pages_id

    def build_page(self, pagename, **kwargs):
        """This is the main method used to render pages. The pagename is the
        url used to search yaml file into ./content/pages directory and sub
        folders. The page is rendered building it from "content" key of yaml
        file and if required contents can be embedded recursively into other
        contents or can be read including files. The result is the rendered
        page. If cache is enabled, the page is rendered only once.

        In Flask this method must be called within a route, and the method
        write_static call it for every pages of site.

        Args:
            pagename (str): the name of page (url) to build.
            **kwargs: optional parameters used to pass dynamic contents

        Returns:
            str: the text of rendered page
        """

        # Store metadata of pages into global vars and save them in json file
        # to be accessible during the page rendering and on client side by
        # scripts. This can be useful for collecting pages by metadata
        if not self.vars.get('meta_pages', None):
            self.vars['meta_pages'] = self.meta_pages()
            filename = os.path.join(
                self.content, self.media, 'site_meta.json')
            jmeta = json.dumps(self.vars['meta_pages'],
                               indent=4, default=_json_date_encoder)
            with open(filename, "w") as f:
                f.write(jmeta)
                f.close()

        filename, page = self.load_yaml_page(pagename)
        if not page:
            return page

        # if the page was already cached and not newer the file it is not
        # rendered again
        self.was_cached = False
        content = None
        if self.cache and page.get('cacheable', True):
            cached = self.cached.get(pagename)
            if cached and cached[0] > os.stat(filename).st_mtime:
                content = cached[1]
                self.was_cached = True

        # the main render logic
        if not content:
            self.extra_args = kwargs
            self.page = page
            templ_name = page.get('templ_name', None)
            content = self.render_content(
                page['content'], page.get('widgets_envelope'))
            content = self.render_template(
                templ_name=templ_name, content=content)
            # template commands can be embedded within html and md and this is
            # the last rendering which evaluate them
            template = self.env.from_string(content)
            content = template.render(page=page, **kwargs)
            if self.cache and page.get('cacheable', True):
                self.cached[pagename] = (time.time(), content)
        return content

    def write_static(self, pages=None, destination='.', media_prefix=None,
                     static_url=None, out_pages=[]):
        """Write html pages on disk! If pages is None, all pages declared in
        content/pages folder are rendered as html and written on disk.

        The suffix of url is set to ".html" and the value is stored into
        global vars so internal links during rendering can be changed from
        "page" to "page.html", in the same way, prefix of pages can be changed
        form "/" to whatever is needed in the target static site.

        This method change some internal parameters that are different from
        dynamic and static pages.

        Destination indicate the folder where save files and media_prefix lets
        you to modify url's for media files to point to real data location.

        Args:
            pages (list): If None all pages are written as static, else only
                pages in the list are rendered.
            destination (str): insert the destination path folder where pages
                will be written
            media_prefix (str): This optional parameter let to change the
                pathname for media contents which can differ from development
                environment and destination site.
            static_url (str): This optional parameter let to change the url
                prefix for local links, so if the destination is
                https://www.example.com/mysite with prefix /mysite/ all links
                works fine
            out_pages (list): list of pages excluded from writing
        """
        self.vars['is_static'] = True
        self.vars['url_suffix'] = ".html"
        url_prefix = self.vars['url_prefix']
        if static_url is None:
            static_url = self.static_url
        self.vars['url_prefix'] = static_url
        self.media_prefix = self.vars['url_prefix'] + media_prefix

        if pages is None:
            files, pages = self.get_site_pages()

        if not isinstance(pages, list):
            pages = [pages]

        for page in pages:
            if page in out_pages:
                continue
            s = self.build_page(page)
            filename = os.path.join(
                destination, page + self.env.globals['url_suffix'])
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                f.write(s)
                f.close()

        self.media_prefix = None
        self.vars['url_prefix'] = url_prefix
        self.vars['url_suffix'] = ""
        self.vars['is_static'] = False

    def write_json_meta(self, filename='site_meta.json', destination='.'):
        """Write metadata of pages as json file to disk. So if needed
        javascript can read them to build client side logics.

        Note:
            This method usually is not needed, because each time Almoststatic
            starts and the first page is rendered, metadata are written on:
            ./content/media/site_meta.json so metadata can be found there.

        Args:
            filename (list): Name of json file to write
            destination (str): destination path folder for json file
        """
        meta = self.meta_pages()
        jmeta = json.dumps(meta, indent=4, default=_json_date_encoder)
        filename = os.path.join(destination, filename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write(jmeta)
            f.close()

    def invalidate_cache(self):
        """Delete all cached pages to force re rendering... if needed, simple!
        """
        self.cached = {}

    def get_media(self, media_obj):
        """Used inside templates, get the filename of static media file.
        Start point of media files usually is: ./content/media

        Args:
            media_obj (str): media object to retrive with the local path from
                             media starting point

        Returns:
            str: the pathname of media object
        """
        if self.media_prefix is None:
            media_prefix = '/'.join([self._relative_url(),
                                     self.content, self.media])
        else:
            media_prefix = self._relative_url() + self.media
        filename = '/'.join([media_prefix, media_obj])
        return filename

    def get_url(self, page):
        """Build the url for local links adding prefix and suffix to the page,
        used inside templates write local url's consistent in dynamic and
        static sites. Recognize the anchor separator to add suffix before it.

        Args:
            page (str): local url

        Returns:
            str: the url for internal link
        """
        try:
            i = page.index('#')
            anchor = page[i:]
            page = page[:i]
        except ValueError:
            anchor = ''
        suffix = self.vars['url_suffix']
        return f"{self._relative_url()}{page}{suffix}{anchor}"

    def get_markdown(self, text):
        """convert markdown to html with tables extension.

        double quote and single quotes by default can be escaped with "^^"
        sequence, this let to insert Jinja2 commands within links.
        In markdown `[My Page]({{get_url("mylink")}})` produce an error because
        markdown uses quotes to identify title attribute. So it can be
        substituted with `[My Page]({{get_url(``mylink``)}})`. This mean that
        you can use the sequence "``" only for links.

        Args:
            text (str): the text in markdown format
        Returns:
            str: the converted text
        """
        quote_marker = '\\:'
        text = text.replace(self.quote_escape, quote_marker)
        text = markdown.markdown(text, extensions=['tables', 'fenced_code'])
        return text.replace(quote_marker, "'")

    def _relative_url(self):
        """"""
        if self.vars['url_prefix']:
            return self.vars['url_prefix']
        return '../' * self.page['pagename'].count('/')

    def meta_pages(self, subfolder=''):
        """Read metadata of all pages declared in ./content/pages folder. The
        folder parameter is used to read only a sub folder, this can be
        useful for collecting metadata of only one folder i.e. "blog"

        Args:
            subfolder (str): if present limit metadata reading to the folder
        Returns:
            dict: all metadata required
        """
        files, pages = self.get_site_pages(subfolder)
        meta = {}
        for i, pagename in enumerate(pages):
            filename, page = self.load_yaml_page(pagename)
            m = {}
            for k, v in page.items():
                if k in self.meta_names:
                    m[k] = v
            m['id'] = i
            meta[m['pagename']] = m
        return meta

    def query_blog(self, categories=[], tags=[], empty_ok=False):
        """Query blog pages against categories and tags. Each page can have
        many tags and belong to many categories. This method query pages by
        list of categories and list of tags and return the list of pages
        which matches all criteria and pages for categories and tags. Usually
        pages with no tags or no categories are not accepted, but if parameter
        empty_ok is true are accepted at least in list of all pages.

        Args:
            categories (list): list of categories to search, if empty accept
                all
            tags (list): list of tags to search, if empty accept all
            empty_ok (bool): if true accept pages without categories or tags

        Returns:
            tuple: list of all pages, list of pages matching categories, list
            of pages matching tags
        """
        pages = []
        cat_dict = {}
        tag_dict = {}
        for k, v in self.vars['meta_pages'].items():
            if 'blog' not in v:
                continue
            if v['blog'].get('disabled', False):
                continue

            def _check(lquery, ldata):
                """check if page belongs to categories or tags in query. return
                a list with found keys
                """
                dest = []
                ll = copy.copy(lquery) if lquery else ldata
                for i in ll:
                    try:
                        ldata.index(i)
                        dest.append(i)
                    except ValueError:
                        pass
                return dest

            def _add_page(keys, dest):
                """Add al keys in det dict and append the page to all"""
                for i in keys:
                    if i not in dest.keys():
                        dest[i] = []
                    dest[i].append(v)

            cat = _check(categories, v['blog'].get('categories', []))
            tag = _check(tags, v['blog'].get('tags', []))
            # accept pages with empty categories or tags, or not
            if categories or empty_ok:
                _add_page(cat, cat_dict)
            if tags or empty_ok:
                _add_page(tag, tag_dict)
            if categories or tags or empty_ok:
                pages.append(v)

        # order categories and tag first by priority and then by date
        for k in cat_dict.keys():
            def _sort(page):
                if page['blog'].get('categ_order'):
                    t = page['blog']['categ_order'].get(k, 0)
                else:
                    t = 0
                x = f"{t:0>10} {page['date']}"
                return x
            cat_dict[k].sort(key=_sort, reverse=True)
        for k in tag_dict.keys():
            def _sort(page):
                if page['blog'].get('tag_order'):
                    t = page['blog']['tag_order'].get(k, 0)
                else:
                    t = 0
                x = f"{t:0>10} {page['date']}"
                return x
            tag_dict[k].sort(key=_sort, reverse=True)

        return (pages, cat_dict, tag_dict)

    def pages_id(self, pages):
        """Return a list of the id's of pages passed as argument. This is
        useful to give list of pages to scripts at runtime that can be searched
        in file './content/media/site_meta.json'

        Args:
            pages (list): list pages metadata
        Returns:
            list: list of id's of passed pages
        """
        dest = []
        for page in pages:
            dest.append(page['id'])
        return dest

    def get_site_pages(self, subfolder=''):
        """Read the pages folder and return the list of yaml files and the list
        of pages url's

        Args:
            subfolder (str): used to restrict reading to only a sub folder.
        Returns:
            tuple: list of files and list of page url's
        """
        base_path = os.path.join(self.content, self.pages, '')
        path = os.path.join(base_path, subfolder, '')
        files = glob.glob(path + '**/*.yaml', recursive=True)
        pages = [s.replace(base_path, '').replace('.yaml', '') for s in files]
        return files, pages

    def load_yaml_page(self, pagename):
        """Load page form yaml file on disk and return the filename and the
        page as dict.

        The page can contain some metadata that are often used into head and
        body of pages, the omitted metadata are filled with default values.

        Metadata recognized are:

        filename = full pathname of file
        pagename = name of page (same of url)
        title = title of page
        description = description of page
        author = author of page
        templ_name = template name used to render the page
        extends = base page to extend
        cacheable = if page is cacheable it is rendered only once
        date = date of page if not present takes the modification time of file
        blog = blog data of page if present

        Args:
            pagename (str): name of page to read
        Returns:
            tuple: the filename of page and the dict with page data and
                metadata
        """
        filename = self.get_filename(pagename)
        if not os.path.isfile(filename):
            return None, None
        with open(filename) as f:
            page = yaml.load(f, Loader=yaml.FullLoader)
            f.close()
        # page metadata
        page['filename'] = filename
        page['pagename'] = pagename

        def default_meta(key, value):
            t = self.env.globals['meta'].get(key, value)
            page[key] = page.get(key, t)
        default_meta('title', '')
        default_meta('description', '')
        default_meta('author', '')

        page['templ_name'] = page.get('templ_name', self.templ_name)
        page['extends'] = page.get('extends', None)
        page['cacheable'] = page.get('cacheable', True)
        page['date'] = page.get('date', datetime.datetime.fromtimestamp(
            os.stat(filename).st_mtime))
        return filename, page

    def get_filename(self, pagename):
        """return the yaml file from pagename"""
        return os.path.join(self.content, self.pages, pagename + '.yaml')

    def render_content(self, content, widgets_envelope=None):
        """Render the content of page, the content is a a key of the page and
        can be a single widget or a list of widgets, widgets_envelope is the
        default evelope for each widgets which can be passed by page
        """
        if not isinstance(content, list):
            content = [content]
        result = ""
        for widget in content:
            # each widgets must have a key 'type' which indicate the name of
            # template to render, if the type id 'include', a file of widgets
            # is included
            disabled = widget.get('disabled', False)
            if not disabled:
                if widget['type'] == 'include':
                    text = self._import_file(widget['file'])
                else:
                    widget = self.eval_widget(widget)
                    text = self.render_template(
                        widget['type'] + '.html', widget=widget)
                envelope = widget.get('envelope') or widgets_envelope
                if envelope:
                    text = "%s\n%s\n%s" % (envelope[0], text, envelope[1])
                result += text
        return result

    def particle(self, name, key='particles'):
        """A particle is a widget that can be embedded everywhere into a a text
        field. The widget is declared into page in a section called "particles"
        or whatever you want, and the "id" field is used to select the widget
        to render.

        Args:
            name (str): the id to search
            key (str, optional): The section containing the particle to search.
              Defaults to 'particles'.

        Returns:
            str: the rendered text
        """
        for content in self.page[key]:
            if content['id'] == name:
                return self.render_content(content)

    def eval_widget(self, value, key=''):
        """Eval a single widget searching for a 'text' key which contain the
        text render. If the text is a string it is always rendered as markdown,
        if text is a dict, it can contain the key 'include' which allow to
        include a file and/or 'content' which is rendered as a page content
        """
        if isinstance(value, list):
            for i, v in enumerate(value):
                value[i] = self.eval_widget(v)
        if isinstance(value, dict):
            for k, v in value.items():
                value[k] = self.eval_widget(v, k)
        if key == 'text':
            if isinstance(value, dict):
                text = ""
                if value.get('include'):
                    text += self._import_file(value['include'])
                if value.get('content'):
                    text += self.render_content(value['content'])
                value = text
            else:
                value = self.get_markdown(value)
        return value

    def _import_file(self, filename):
        """Allow the inclusion of files containg widgets or plain html or
        markdown files. Nested inclusions are allowed and the limit is only
        the python call stack, so you have only to avoid circular inclusions.
        the recognized extensions are: '.html' or '.htm' for plain html text,
        '.md' for markdown text and '.yaml' which can contain widgets under
        'content' key
        """
        fname = os.path.join(self.content, filename)
        if not os.path.isfile(fname):
            return f'The file: {filename} does not exists.'
        with open(fname) as f:
            s = f"File: {filename} not recognized type."
            if fname.endswith('.html') or fname.endswith('.htm'):
                s = f.read()
            elif fname.endswith('.md'):
                s = f.read()
                s = self.get_markdown(s)
            elif fname.endswith('.yaml'):
                content = yaml.load(f, Loader=yaml.FullLoader)
                s = self.render_content(content)
            f.close()
            return s

    def render_template(self, templ_name=None, **kwargs):
        """Render the template and return the text rendered"""
        if templ_name is None:
            templ_name = self.templ_name
        template = self.env.get_template(templ_name)
        s = template.render(page=self.page, **self.extra_args, **kwargs)
        return s


class FlaskAlmoststatic(Almoststatic):
    """Almoststatic can be integrated into Flask web framework. This lets to
    write dynamic sites with some static contents and/or for the development of
    static sites.

    Args:
        app (flask.app): the flask app where Almoststtic is attached.
    """

    def __init__(self, app=None):
        super().__init__()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Add some config parameters and rules to the app to bind the
        extension

        Args:
            app (flask.app): the flask app where Almoststtic is attached.
        """
        self.app = app
        app.config.setdefault('FAS_CONFIG', "./content/config.yaml")
        self.load_config(config_file=app.config['FAS_CONFIG'])
        rule = f'/{self.content}/<path:filename>'
        app.add_url_rule(rule, 'content', self.content_static)
        app.template_context_processors[None].append(self.content_processor)
        app.jinja_env.autoescape = False
        app.jinja_loader = FileSystemLoader(self.templates)

    def content_processor(self):
        return self.vars

    def content_static(self, filename):
        """The content directory is rendered as static, files can have a
        relative path from there
        """
        path = os.path.join(self.app.root_path, self.content)
        return flask.send_from_directory(path, filename)

    def render_template(self, templ_name=None, **kwargs):
        if templ_name is None:
            templ_name = self.templ_name
        s = flask.render_template(
            templ_name, page=self.page, **self.extra_args, **kwargs)
        return s


def iif(condition, if_true, if_false=""):
    """Inline if short code
    try: iif(1==1, "Ok", "No")

    Args:
        condition (bool): condition to test
        if_true (any): value to return if condition is true
        if_false (any): value to return if condition is false
    Returns:
        any: the result
    """
    if condition:
        return if_true
    return if_false


def if_in(value, iterable, if_not=""):
    """Inline check for inclusion.
    try: if_in('a', ['a','b','c'], 'd')

    Args:
        value (any): value to check
        iterable (iterable): iterable to search for value
        if_not (any): value to return if not found

    Returns:
        any: the result
    """
    if not iterable:
        iterable = []
    if value in iterable:
        return value
    return if_not


def _json_date_encoder(value):
    """encoder for json dumps of dates"""
    if isinstance(value, datetime.date):
        return value.__str__()
