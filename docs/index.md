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
