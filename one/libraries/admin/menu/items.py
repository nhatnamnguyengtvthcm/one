from django.apps import apps as django_apps

from one.libraries.admin.menu.constants import MENU_EXTRA_DETAILS
from one.libraries.admin.utils import AppListElementMixin


class MenuItem:
    """
    This is the base class for custom menu items.
    A menu item can have the following properties:

    ``title``
        String that contains the menu item title, make sure you use the
        django gettext functions if your application is multilingual.
        Default value: 'Untitled menu item'.

    ``url``
        String that contains the menu item URL.
        Default value: '#'.

    ``css_classes``
        A list of css classes to be added to the menu item ``li`` class
        attribute. Default value: [].

    ``accesskey``
        The menu item accesskey. Default value: None.

    ``description``
        An optional string that will be used as the ``title`` attribute of
        the menu-item ``a`` tag. Default value: None.

    ``enabled``
        Boolean that determines whether the menu item is enabled or not.
        Disabled items are displayed but are not clickable.
        Default value: True.

    ``template``
        The template to use to render the menu item.
        Default value: 'admin_tools/menu/item.html'.

    ``children``
        A list of children menu items. All children items must be instances of
        the ``MenuItem`` class.
    """

    title = "Untitled menu item"
    url = "#"
    fas_icon = None
    css_classes = None
    accesskey = None
    description = None
    enabled = True
    template = "libraries/menu/item.html"
    children = None

    def __init__(self, title=None, url=None, **kwargs):
        if title is not None:
            self.title = title

        if url is not None:
            self.url = url

        for key in kwargs:
            if hasattr(self.__class__, key):
                setattr(self, key, kwargs[key])
        self.children = self.children or []
        self.css_classes = self.css_classes or []

    def init_with_context(self, context):
        """
        Like for menus, menu items have a ``init_with_context`` method that is
        called with a ``django.template.RequestContext`` instance as unique
        argument.
        This gives you enough flexibility to build complex items, for example,
        let's build a "history" menu item, that will list the last ten visited
        pages::

            from admin_tools.menu.items import MenuItem

            class HistoryMenuItem(MenuItem):
                title = 'History'

                def init_with_context(self, context):
                    request = context['request']
                    # we use sessions to store the visited pages stack
                    history = request.session.get('history', [])
                    for item in history:
                        self.children.append(MenuItem(
                            title=item['title'],
                            url=item['url']
                        ))
                    # add the current page to the history stack
                    history.insert(0, {
                        'title': context['title'],
                        'url': request.META['PATH_INFO']
                    })
                    if len(history) > 10:
                        history = history[:10]
                    request.session['history'] = history

        Here's a screenshot of our history item:

        .. image:: images/history_menu_item.png
        """
        pass

    def is_selected(self, request):
        """
        Helper method that returns ``True`` if the menu item is active.
        A menu item is considered as active if it's URL or one of its
        descendants URL is equals to the current URL.
        """
        current_url = request.get_full_path()
        return (
            self.url == current_url
            or len([c for c in self.children if c.is_selected(request)]) > 0
        )

    def is_empty(self):
        """
        Helper method that returns ``True`` if the menu item is empty.
        This method always returns ``False`` for basic items, but can return
        ``True`` if the item is an AppList.
        """
        return False


class AppList(MenuItem, AppListElementMixin):
    """
    A menu item that lists installed apps and their models.
    In addition to the parent :class:`~admin_tools.menu.items.MenuItem`
    properties, the ``AppList`` has two extra properties:

    ``models``
        A list of models to include, only models whose name (e.g.
        "blog.comments.Comment") match one of the strings (e.g. "blog.*")
        in the models list will appear in the menu item.

    ``exclude``
        A list of models to exclude, if a model name (e.g.
        "blog.comments.Comment") match an element of this list (e.g.
        "blog.comments.*") it won't appear in the menu item.


    If no models/exclude list is provided, **all apps** are shown.

    Here's a small example of building an app list menu item::

        from admin_tools.menu import items, Menu

        class MyMenu(Menu):
            def __init__(self, **kwargs):
                super(MyMenu, self).__init__(**kwargs)
                self.children.append(items.AppList(
                    title='Applications',
                    exclude_list=('django.contrib',)
                )

    The screenshot of what this code produces:

    .. image:: images/applist_menu_item.png

    .. note::

        Note that this menu takes into account user permissions, as a
        consequence, if a user has no rights to change or add a ``Group`` for
        example, the ``django.contrib.auth.Group model`` child item won't be
        displayed in the menu.
    """

    def __init__(self, title=None, **kwargs):
        """
        ``AppListMenuItem`` constructor.
        """
        self.models = list(kwargs.pop("models", []))
        self.exclude = list(kwargs.pop("exclude", []))
        self.include_list = kwargs.pop("include_list", [])  # deprecated
        self.exclude_list = kwargs.pop("exclude_list", [])  # deprecated
        super().__init__(title, **kwargs)

    def init_with_context(self, context):
        """
        Please refer to
        :meth:`~admin_tools.menu.items.MenuItem.init_with_context`
        documentation from :class:`~admin_tools.menu.items.MenuItem` class.
        """
        items = self._visible_models(context["request"])
        apps = {}
        for model, perms in items:
            if not (perms["change"] or perms.get("view", False)):
                continue
            app_label = model._meta.app_label  # noqa
            if app_label not in apps:
                apps[app_label] = {
                    "app_label": app_label,
                    "title": django_apps.get_app_config(app_label).verbose_name,
                    "url": self._get_admin_app_list_url(model, context),
                    "models": [],
                }
            apps[app_label]["models"].append(
                {
                    "app_label": app_label,
                    "title": model._meta.verbose_name_plural,  # noqa
                    "url": self._get_admin_change_url(model, context),
                }
            )

        for app in sorted(apps.keys()):
            app_dict = apps[app]
            title = app_dict["title"]
            icon = "fa-cube"
            if app in MENU_EXTRA_DETAILS:
                if "title" in MENU_EXTRA_DETAILS[app]:
                    title = MENU_EXTRA_DETAILS[app]["title"]
                if "icon" in MENU_EXTRA_DETAILS[app]:
                    icon = MENU_EXTRA_DETAILS[app]["icon"]

            item = MenuItem(title=title, url=app_dict["url"], fas_icon=icon)
            # sort model list alphabetically
            apps[app]["models"].sort(key=lambda x: x["title"])
            for model_dict in apps[app]["models"]:
                item.children.append(MenuItem(**model_dict))
            self.children.append(item)

    def is_empty(self):
        """
        Helper method that returns ``True`` if the applist menu item has no
        children.

        # >>> from admin_tools.menu.items import MenuItem, AppList
        # >>> item = AppList(title='My menu item')
        # >>> item.is_empty()
        # True
        # >>> item.children.append(MenuItem(title='foo'))
        # >>> item.is_empty()
        # False
        # >>> item.children = []
        # >>> item.is_empty()
        True
        """
        return len(self.children) == 0


class ModelList(MenuItem, AppListElementMixin):
    """
    A menu item that lists a set of models.
    In addition to the parent :class:`~admin_tools.menu.items.MenuItem`
    properties, the ``ModelList`` has two extra properties:

    ``models``
        A list of models to include, only models whose name (e.g.
        "blog.comments.Comment") match one of the strings (e.g. "blog.*")
        in the include list will appear in the dashboard module.

    ``exclude``
        A list of models to exclude, if a model name (e.g.
        "blog.comments.Comment" match an element of this list (e.g.
        "blog.comments.*") it won't appear in the dashboard module.

    Here's a small example of building a model list menu item::

        from admin_tools.menu import items, Menu

        class MyMenu(Menu):
            def __init__(self, **kwargs):
                super(MyMenu, self).__init__(**kwargs)
                self.children += [
                    items.ModelList(
                        'Authentication', ['django.contrib.auth.*',]
                    )
                ]

    .. note::

        Note that this menu takes into account user permissions, as a
        consequence, if a user has no rights to change or add a ``Group`` for
        example, the ``django.contrib.auth.Group model`` item won't be
        displayed in the menu.
    """

    def __init__(self, title=None, models=None, exclude=None, **kwargs):
        """
        ``ModelList`` constructor.
        """
        self.models = list(models or [])
        self.exclude = list(exclude or [])
        self.include_list = kwargs.pop("include_list", [])  # deprecated
        self.exclude_list = kwargs.pop("exclude_list", [])  # deprecated

        super().__init__(title, **kwargs)

    def init_with_context(self, context):
        """
        Please refer to
        :meth:`~admin_tools.menu.items.MenuItem.init_with_context`
        documentation from :class:`~admin_tools.menu.items.MenuItem` class.
        """
        items = self._visible_models(context["request"])
        for model, perms in items:
            if not (perms["change"] or perms.get("view", False)):
                continue
            title = model._meta.verbose_name_plural  # noqa
            url = self._get_admin_change_url(model, context)
            item = MenuItem(title=title, url=url)
            self.children.append(item)

    def is_empty(self):
        """
        Helper method that returns ``True`` if the modellist menu item has no
        children.

        # >>> from admin_tools.menu.items import MenuItem, ModelList
        # >>> item = ModelList(title='My menu item')
        # >>> item.is_empty()
        # True
        # >>> item.children.append(MenuItem(title='foo'))
        # >>> item.is_empty()
        # False
        # >>> item.children = []
        # >>> item.is_empty()
        # True
        """
        return len(self.children) == 0
