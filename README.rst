Muffin-Classy
=============

..  image:: https://travis-ci.org/ei-grad/muffin-classy.svg?branch=master
    :target: https://travis-ci.org/ei-grad/muffin-classy


..  image:: https://coveralls.io/repos/ei-grad/muffin-classy/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/ei-grad/muffin-classy?branch=master


.. module:: muffin_classy

Muffin-Classy provides class-based views to `Muffin` and `aiohttp`.

It is inspired by and is based on `Flask-Classy`.

`Muffin-Classy` will automatically generate routes based on the methods in your
views, and makes it simple to override those routes using Muffin's familiar
decorator syntax.

.. _Muffin-Classy: http://github.com/ei-grad/muffin-classy
.. _Flask-Classy: http://github.com/apiguy/flask-classy
.. _Muffin: https://github.com/klen/muffin/
.. _aiohttp: https://github.com/KeepSafe/aiohttp/

Installation
------------

Install the with::

    $ pip install git+https://github.com/ei-grad/muffin-classy.git#egg=muffin-classy


Let's see how it works
----------------------

If you're like me, you probably get a better idea of how to use something
when you see it being used. Let's go ahead and create a little app to
see how Muffin-Classy works::

    from muffin import Application
    from muffin_classy import MuffinView

    # we'll make a list to hold some quotes for our app
    quotes = [
        "A noble spirit embiggens the smallest man! ~ Jebediah Springfield",
        "If there is a way to do it better... find it. ~ Thomas Edison",
        "No one knows what he can do till he tries. ~ Publilius Syrus"
    ]

    app = Application(__name__)

    class QuotesView(MuffinView):
        def index(self):
            return "<br>".join(quotes)

    QuotesView.register(app, "/quotes")

    if __name__ == '__main__':
        app.run()

Run this app and open your web browser to: http://localhost:5000/quotes/

As you can see, it returns the list of quotes. But what if we just wanted
one quote? What would we do then?

::

    class QuotesView(MuffinView):
        def index(self):
            ...

        def get(self, id):
            id = int(id)
            if id < len(quotes) - 1:
                return quotes[id]
            else:
                return "Not Found", 404

Now direct your browser to: http://localhost:5000/quotes/1/ and you should
see the very poignant quote from the esteemed Mr. Edison.

That's cool and all, but what if we just wanted a random quote? What then?
Let's add a random view to our MuffinView::

    from random import choice

::

    class QuotesView(MuffinView):
        def index(self):
            ...

        def get(self, id):
            ...

        def random(self):
            return choice(quotes)

And point your browser to: http://localhost:5000/quotes/random/ and see
that a random quote is returned each time. Voilà!

So by now you must be keenly aware of the fact that you have not defined a
single route, but yet routing is obviously taking place. "Is this voodoo?"
you ask?

Not at all. Muffin-Classy will automatically create routes for any method
in a MuffinView that doesn't begin with an underscore character.
You can still define your own routes of course, and we'll look at that next.


Using custom routes
-------------------

So let's pretend that `/quotes/random/` is just too unsightly and we must
fix it to be something more spectacular forthwith. In a moment of blind
inspiration we decide that getting a random quote is on par with receiving
a rasher of your favorite porcine delicacy. The new url should be `/quotes/word_bacon/`
so that everyone knows what a treat they are in for.

::

    from muffin_classy import MuffinView, route

::

    class QuotesView(MuffinView):
        def index(self):
            ...

        def get(self, id):
            ...

        @route('/word_bacon/') #<--- Adding route
        def random(self):
            return choice(quotes)

Load up http://localhost:5000/quotes/word_bacon/ in your browser and behold
your latest achievement.

The route decorator takes exactly the same parameters as Muffin's `app.route`
decorator, so you should feel right at home adding custom routes to any
views you create.

.. note::
    If you want to use other decorators with your views, you'll need to
    make sure that the ``@route`` decorators are first.

Using multiple routes for a single view
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What happens when you need to apply more than one route to a specific view
(for what it's worth, Muffin core developer Armin Ronacher `says doing that is
a bad idea <http://stackoverflow.com/a/7876088/105987>`_). But since you're so
determined let's see how to do that anyway.

So let's say you add the following routes to one of your views::

    class QuotesView(MuffinView):

        @route('/quote/<id>')
        @route('/quote/show/<id>')
        def show_quote(self, id):
            ...

That would end up generating the following 2 routes:

============ ================================
**rule**     /quote/<id>
**endpoint** QuotesView:show_quote-1
**method**   GET
============ ================================

============ ================================
**rule**     /quote/show/<id>
**endpoint** QuotesView:show_quote
**method**   GET
============ ================================


Specify your own damn endpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So you don't like the nifty indexing trick? Well fine then. I guess you can
go ahead and specify your own endpoint if you like but that's only because I
like you.

::

    class QuotesView(MuffinView):

        @route('/quote/<id>', endpoint='show_quote')
        @route('/quote/show/<id>')
        def show_quote(self, id):
            ...

Will generate the following routes:

============ ================================
**rule**     /quote/<id>
**endpoint** show_quote
**method**   GET
============ ================================

============ ================================
**rule**     /quote/show/<id>
**endpoint** QuotesView:show_quote
**method**   GET
============ ================================

Special method names
--------------------

So I guess I have to break the narrative a bit here so I can take some
time to talk about `Muffin-Classy`'s special method names.

Here's the thing. `MuffinView` is smart. No, not solving differential
equations smart, but let's just say it knows how to put the round peg
in the round hole. When you register a `MuffinView` with an app,
`MuffinView` will look for special methods in your class. Why? Because
I care. I know that sometimes you just want things to just *work* and
not have to think about it. Let's look at `MuffinView`'s very special
method names:

**index**
    Woah... you've seen this one before! Remember way back at the
    beginning? Oh nevermind. So *index* is generally used for home pages
    and lists of resources. The automatically generated route is:

    ============ ================================
    **rule**     /
    **endpoint** <class name>:index
    **method**   GET
    ============ ================================

**get**
    Another old familiar friend, `get` is usually used to retrieve a
    specific resource. The automatically generated route is:

    ============ ================================
    **rule**     /<id>
    **endpoint** <class name>:get
    **method**   GET
    ============ ================================

**post**
    This method is generally used for creating new instances of a resource
    but can really be used to handle any posted data you want. The
    automatically generated route is:

    ============ ================================
    **rule**     /
    **endpoint** <class name>:post
    **method**   POST
    ============ ================================

**put**
    For those of us using REST this one is really helpful. It's generally
    used to update a specific resource. The automatically generated route
    is:

    ============ ================================
    **rule**     /<id>
    **endpoint** <class name>:put
    **method**   PUT
    ============ ================================

**patch**
    Similar to `put`, `patch` is used for updating a resource. Unlike `put`
    however you only send the parts of the resource you want changed,
    instead of doing a complete replacement of the resource. The automatically
    generated route is:

    ============ ================================
    **rule**     /<id>
    **endpoint** <class name>:patch
    **method**   PATCH
    ============ ================================

**delete**
    More RESTfulness. It's the most self explanatory of all the RESTful
    methods, and it's commonly used to destroy a specific resource. The
    automatically generated route is:

    ============ ================================
    **rule**     /<id>
    **endpoint** <class name>:delete
    **method**   DELETE
    ============ ================================


url_for art thou, Romeo?
------------------------

Sorry that's a terrible name for a section header, but naming things is what
am the least skilled at, so please bear with me.

Once you've got your `MuffinView` registered, you'll probably want to be able
to get the urls for it in your templates and redirects and whatnot. Muffin
ships with the awesome `url_for` function that does an excellent job of
turning a function name into a url that maps to it. You can use `url_for`
with Muffin-Classy by using the format "<Class name>:<method name>". Let's
look at an example::

    class DuckyView(MuffinView):
        def index(self):
            return "Duckies!"

        def get(self, name):
            return "Duck %s" % name

        @route('/do_duck_stuff', endpoint='do_duck_stuff')
        def post(self):
            return "Um... Quack?"

In this example, you can get a url to the index method using::

    app.router["DuckyView:index"].url()

And you can get a url to the get method using::

    app.router["DuckyView:get"].url(parts=dict(name="Howard"))

And for that view with the custom endpoint defined?::

    app.router["do_duck_stuff"].url()

.. note::
    Notice that the custom endpoint does not get prefixed with the class
    name like the auto-generated endpoints. When you define a custom
    endpoint, we hand that over to Muffin in it's original, unaltered form.


Your own methods (they're special too!)
---------------------------------------

Let's talk about how you can add your own methods (like we did with
`random` back in the day, remember? Good times.) If you add your own
methods `MuffinView` will detect them during registration and register
routes for them, whether you've gone and defined your own, or you just
want to let `MuffinView` do it's thing. By default, `MuffinView` will
create a route that is the same as the method name. So if you define a
view method in your `MuffinView` like this::

    class SomeView(MuffinView):

        def my_view(self):
            return "Check out my view!"

`MuffinView` will generate a route like this:

============ ================================
**rule**      /my_view/
**endpoint**  SomeView:my_view
**method**    GET
============ ================================

"That's fine." you say. "But what if I have a view method with some
parameters?" Well `MuffinView` will try to take care of that for you
too. If you were to define another view like this::

    class AnotherView(MuffinView):

        def this_view(self, arg1, arg2):
            return "Args: %s, %s" % (arg1, arg2,)

`MuffinView` would generate a route like this:

============ ================================
**rule**     /this_view/<arg1>/<arg2>
**endpoint** AnotherView:this_view
**method**   GET
============ ================================

.. note::
    One important thing to note, is that `MuffinView` does not type your
    parameters, so if you want or need them you'll need to define the
    route yourself using the `@route` decorator.


Before and After
----------------

Hey, remember that time when you made that big 'ol `Flask` app and then
had those ``@app.before_reqeust`` and ``@app.after_request``
decorated methods? Remember how you only wanted some of them to run for
certain views so you had all those ``if view == the_one_I_care_about:``
statements and stuff?

**Yuck.**

I've been there too, and I think you might like how `Muffin-Classy`
addresses this very touchy issue. ``MuffinView`` will look for wrapper
methods when your request is being processed so that you can create more
fine grained "before and after" processing methods.

Wrap all the views in a MuffinView
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

So there you are, eating a delicious Strawberry Frosted Pop Tart one
morning, thinking about the awesome `Muffin-Classy` app you deployed the
night before during one of your late night hackathons and it hits you:

*"Tracking! I need to track those widgets!"*

No doubt it's an inspired thought, but in this case it was a tragic
oversight. You realize now how lucky it was that you chose to use
`Muffin-Classy` because adding tracking is going to be a snap::

    from muffin_classy import MuffinView
    from made_up_tracking import track_it

    class WidgetsView(MuffinView):

        def before_request(self, request):
            track_it("something is happening to a widget")

        def after_request(self, request, response):
            track_it("something happened to a widget")
            return response

        def post(self):
            ...

        def get(self, id):
            ...

Whew. Crisis averted, am I right? So you go about your day and at lunch time
you hit your favorite Bacon Sandwich place and start daydreaming about your
life as a rockstar `Muffin-Classy` consultant when suddenly:

*"I really only care about when widgets are created and retrieved!"*

Wrap only specific views
~~~~~~~~~~~~~~~~~~~~~~~~

Yep, you've got a granularity problem. Not to worry though because
`Muffin-Classy` is happy to let you know that it has *smart* wrapper methods
too. Let's say for example you wanted to run something before the ``index`` view
runs? Just create a method called ``before_index`` and `Muffin-Classy` will make
sure it gets run only before that view. (as you have guessed by now,
``after_index`` will be run only after the index view).

::

    from muffin_classy import MuffinView
    from made_up_tracking import track_it

    class WidgetsView(MuffinView):

        # Will be run before the 'get' view
        def before_get(self, request):
            track_it("a widget is being accessed")

        # Will be run before the 'post' view
        def after_post(self, request, response):
            track_it("a widget was created")
            return response

        def post(self):
            ...

        def get(self, id):
            ...

The View Wrappin' Method List
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Just to be certain, let's go ahead and review the methods you can write to
wrap your views:

**before_request(self, request, *args, *kwargs)**
    Will be called before any view in this ``MuffinView`` is called.

    :request:    aiohttp request object.
                 The name of the view that's about to be called is available as
                 request.classy_method_name

    :\*args:     Any arguments that will be passed to the view.


    :\*\*kwargs: Any keyword arguments that will be passed to the view.


**before_<view_method>(self, request, *args, **kwargs)**
    Will be called before the view specified <view_method> is called.

    :request:    aiohttp request object.
                 The name of the view that's about to be called is available as
                 request.classy_method_name

    :\*args:     Any arguments that will be passed to the view.


    :\*\*kwargs: Any keyword arguments that will be passed to the view.


**after_request(self, request, response)**
    Will be called after any view in this ``MuffinView`` is called. You must
    return either the passed in response or a new response.

    :request:    aiohttp request object.
                 The name of the view that's about to be called is available as
                 request.classy_method_name

    :resposne:   The response produced after calling the view.


**after_<view_method>(self, request, response)**
    Will be called after the <view_method> is called. You must return either
    the passed in response or a new response.

    :request:    aiohttp request object.
                 The name of the view that's about to be called is available as
                 request.classy_method_name

    :response:   The response produced after calling the view.


Order of Wrapped Method Execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Wrapper methods are called in the same order every time. "How predictable."
you're thinking. (You're starting to sound like my ex, sheesh.) I prefer the
term *reliable*.

1. MuffinView's ``before_request`` method
2. MuffinView's ``before_<view_method>`` method
3. The actual view method
4. MuffinView's ``after_<view_method>`` method
5. MuffinView's ``after_request`` method


Questions?
----------

Feel free to ping me on twitter @ei-grad, or head on over to the
github repo at http://github.com/ei-grad/muffin-classy so you can join
the fun.


API
---

.. autoclass:: muffin_classy.MuffinView
    :members:


.. autofunction:: muffin_classy.route

----

© Copyright 2013 by Freedom Dumlao, `Follow Me @apiguy <https://twitter.com/APIguy>`_

© Copyright 2015 by Andrew Grigorev, `Follow Me @eigrad <https://twitter.com/eigrad>`_
