---
title: Testing Python
subtitle: Shiny happy code holding hands
---
This is a discussion of the benefits and philosophy of test-driven development
that I wrote many years ago. I don't think there's anything ground-breaking here,
but it's a nice compilation of what I've read and learned over the years. This
version is adapted for Python.

## Whaddya mean, test? ##
> A whale is not a fish, it's an insect.  
> *Peter Cook*

> A unit test is not a test, it's a specification.  
> *Agile development mindset*

One of these is a joke, and one is a useful way to think about the world. When
you write one unit test, you actually get two things.

A safety net - If you or another developer make some changes that break the code,
that unit test will start failing. If you run the test right after you make the
change, then it's obvious that your change is the one that broke the code.

A working example - If you write your test clearly, then other developers can
look at it to see how your class should be used. Not only that, but error
condition tests explicitly show how not to use it.

## An example ##
There's a nice, simple example of a unit test in [this blog post][langr] by Jeff
Langr. It tests an implementation of the exponent function. Here are some
excerpts, adapted to Python:

First, a simple case of squaring the numbers from 1 to 10:

    from unittest import TestCase
    
    from math_util import power
    
    class PowerTest(TestCase):
        def test_squares(self):
            for i in range(1, 10):
                self.assertEqual(i * i, power(i, 2))

Then, some more exotic cases:

    def test_one_to_any_always_one(self):
        basicConfig(level=CRITICAL)
        self.assertEqual(1, power(1, 1))
        self.assertEqual(1, power(1, 2))
        self.assertEqual(1, power(1, LARGE_NUMBER))

And, finally, some error conditions:

    def test_negative_exponents(self):
        """ Negative exponents raise ValueError.

        They would be complicated to implement.
        """
        with self.assertRaises(ValueError):
            power(1, -1)

These three cases are typical of the kinds of things to put in your tests.
You've specified how to use the class, as well as how not to use the class and
shown what will happen when the class is abused.

I posted the full sample code for you to play with at [github.com][sample].

[langr]: http://langrsoft.com/2006/06/05/are-tests-specs/
[sample]: https://github.com/donkirkby/testing

## Whaddya mean, test driven? ##
OK, I wrote my code and it works; now I have to write a unit test? That can be
pretty painful. It's even worse if you get asked to try and write unit tests for
existing code that someone else wrote. Why is it painful? Because there are two
types of code: easy-to-test and hard-to-test code. If you write the tests after
the code is finished, you're gambling. You might have written easy-to-test code,
but maybe not. Once you find out, it's depressing to have to go back and change
code that works, just so you can write the stupid test.

Why gamble? Write easy-to-test code the first time. The simplest way to be sure
the code is easy to test is to write the test at the same time as the code.
That's what the "driven" means in test-driven development. You write a little
bit of test, then enough code to make the test compile and pass, but no more.
Then you write a little bit more test, and just enough code to make it compile
and pass. When you have enough tests to specify all the requirements for your
class, your class is finished.

## What makes code hard to test? ##
Hard-to-test code tends to have larger classes and methods that do several
things at once. It can also have fuzzy relationships between those classes.
Objects create instances of each other willy-nilly and messages fly back and
forth. Testing a big class is hard because you probably need to set up a lot of
input data, and there are probably a lot of different scenarios to test. If you
have several big classes that you have to test as a group, the number of
scenarios will often multiply together.

Easy-to-test code tends to have small classes that do one thing. It will often
have more classes collaborating to accomplish the task, but the relationships
and responsibilities of those classes are clear. Techniques like
[dependency injection][depinj] mean that objects don't have to worry about
creating the other objects they work with and that allows you test one class at
a time instead of testing the whole group at once.

There are no guarantees, but easy-to-test code has a lot in common with
easy-to-maintain code.

[depinj]: http://www.martinfowler.com/articles/injection.html

## Writing clearly ##
If unit tests are going to be your class's specification document, they had
better be easy to read. There are four things that every test should have to
make it readable: a name that describes it, data that describes the starting
conditions, the execution of the method being tested, and verification that the
method did the right thing.

## Diminishing returns ##
When are you done? You're done when you're comfortable that the code is nestled
safely in its testing blanket. The hardest thing to learn is when to stop
writing a test. Start small and learn from your experience. It's better to have
a readable, stable test that only covers half an object's code than to have a
big mess that covers all of the code but breaks all the time for bogus reasons.

An advantage of writing the test first is that the test and the code finish
around the same time. If you write a failing test before you add each feature,
you should have a pretty good test when you finish the last feature, and you
won't have any existential angst over whether you've tested enough.

## Refactoring ##
As you build the test and the class together, the design may evolve. As you add
features, a class may need to be split into smaller classes. You can use
refactoring techniques to do this safely. You may also need to refactor the test
to make it more readable. Refactoring is a big topic, and the best place to
start is Martin Fowler's book or his [web site][refactoring]. Refactoring is a
lot safer when you have the tests to catch mistakes.

[refactoring]: http://www.refactoring.com/

## Mock Objects ##
Code can be hard to test when it depends on some external system like the file
system, a database, or a web service. External dependencies can make a test
slow and brittle, and it's often hard to test failure scenarios.

One way to make this kind of code easier to test is to replace the external
system with a mock version of it. As an example, imagine I want to write a
function that fetches a list of a user's repositories from GitHub and returns
a list of the repository names. Here's what the GitHub API looks like:

    $ curl -s https://api.github.com/users/donkirkby/repos | head
    [
      {
        "id": 50468387,
        "name": "active_sinatra",
        "full_name": "donkirkby/active_sinatra",
        "owner": {
          "login": "donkirkby",
          "id": 1639148,
          "avatar_url": "https://avatars.githubusercontent.com/u/1639148?v=3",
          "gravatar_id": "",
    
This fetches the list of my repositories, and prints the first few lines. You
can see that it's a JSON response with a list of dictionaries. Each dictionary
has the name of a repository, plus a bunch of other data we don't care about.

To write a test for this, we can use the mock module. It's included with
Python 3 and available separately for Python 2. Here's the test that patches
the `requests.get()` function with a mock version.

    # test_github_util.py
    from mock import patch
    from unittest import TestCase
    
    from github_util import fetch_repo_names
    
    
    class GithubUtilTest(TestCase):
        @patch('requests.get')
        def test_fetch_repo_names(self, mock_get):
            mock_get.return_value.json.return_value = [
                {"name": "first"},
                {"name": "second"}]
            expected_names = ['first', 'second']
    
            names = fetch_repo_names('joesmith')
    
            self.assertEqual(expected_names, names)

Now when the main code calls `requests.get()`, it will return a mock response
with a `json()` method that returns the list of dictionaries. Once we see that
this test fails, we can write the code.

    # github_util.py
    import requests
    
    
    def fetch_repo_names(username):
        url = ('https://api.github.com/users/{}'
               '/repos'.format(username))
        repos = requests.get(url).json()
        return [repo['name'] for repo in repos]


Mocking in Python is amazing, because nothing is private! You can avoid all the
gymnastics required in statically typed languages, you just have to be careful
to clean up after yourself. Also, be sure that your mock objects behave in a
realistic way. If the real system gives very different responses, the mock tests
won't help.

In some situations, you may want to check what happened to the mock object
at the end of the test. In the example, you could check that your code passed the
correct parameters to the mock object.

            mock_get.assert_called_once_with(
                'https://api.github.com/users/joesmith/repos')

However, I only do this when there's some interesting calculation in the
parameter values. The more you lock down the mock object, the more brittle the
test will be.

## Mocking Django ##
The Django web framework provides a nice test framework that creates a database
from your migrations, bulk loads sample data, and cleans up after each test by
rolling back a transaction. However, all of that database work can be slow! You
can speed it up by using an in-memory SQLite3 database, but it's only about
twice as fast, and the SQLite3 database may behave differently from your
regular database.

We've had some success converting many of our Django tests to pure unit tests
that don't use any database. In my [source code][] you'll find `udjango.py` that
contains a trivial example of some model classes.

    class City(models.Model):
        name = models.CharField(max_length=100)

    class Person(models.Model):
        name = models.CharField(max_length=50)
        city = models.ForeignKey(City, related_name='residents')

        def count_dependents(self):
            return self.children.count()

    class Child(models.Model):
        parent = models.ForeignKey(Person, related_name='children')
        name = models.CharField(max_length=255)

Notice that the name fields and the foreign keys are required fields. A typical
test for the `count_dependents()` method needs to do a bunch of setup before it
can start the actual test. The city object is completely unrelated to the test,
but we need to create it before we can create a person object. In a real
application there's often much more setup.

    city = City.objects.create(name='Vancouver')
    dad = Person.objects.create(name='Dad', city=city)
    dad.children.create(name='Bobby')
    dad.children.create(name='Suzy')

    # Actual test
    dependent_count = dad.count_dependents()

    # Validation
    assert dependent_count == 2, dependent_count

Here's a test from `udjango_mocked.py` for the same function. It mocks out the
database call to `self.children.count()`. Notice how much less setup is needed.

    with patch.object(Person, 'children') as mock_children:
        mock_children.count.return_value = 2
        dad = Person()

        # Actual test
        dependent_count = dad.count_dependents()

        # Validation
        assert dependent_count == 2, dependent_count

In our projects, we've found an even better technique using the
[`django_mock_queries`][mock_queries] library. It lets your code use
`count()`, `order_by()`, `filter()`, and many other features of a query set without
needing a real database. Here's an example from `udjango_mock_set.py`.

    with patch.object(Person,
                      'children',
                      new=MockSet(Child(), Child())):
        dad = Person()

        # Actual test
        dependent_count = dad.count_dependents()

        # Validation
        assert dependent_count == 2, dependent_count

We're still working out the best way to mock out portions of the Django
framework. Our current [strategy][] is a method called `setup_mock_relations()`
that walks through all the related fields on a model class, and replaces them
with mock versions.

[mock_queries]: https://github.com/stphivos/django-mock-queries
[strategy]: https://github.com/cfe-lab/Kive/blob/master/kive/kive/mock_setup.py

## Further Reading ##
Read this series of blog posts on [writing unit tests][test blog]. Find
[further discussion][discuss] of [unit tests as specs][langr] or
[specification by example][example]. Some people talk about getting
[test infected][] when your perspective shifts and you can't imagine coding
without tests.

All of this is covered in detail in Gerard Meszaros's excellent book,
[xUnit Test Patterns][xunit]. Unsurprisingly, it's part of Martin Fowler's book
series.

[test blog]: http://osherove.com/blog/category/unit-testing
[discuss]: http://weblogs.java.net/blog/tball/archive/2004/10/the_problem_wit_1.html
[example]: http://martinfowler.com/bliki/SpecificationByExample.html
[test infected]: http://junit.sourceforge.net/doc/testinfected/testing.htm
[xunit]: http://books.google.ca/books?id=-izOiCEIABQC
[source code]: https://github.com/donkirkby/testing
