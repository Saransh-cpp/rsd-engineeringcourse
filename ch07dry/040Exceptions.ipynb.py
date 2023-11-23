# ---
# jupyter:
#   jekyll:
#     display_name: Exceptions
#   jupytext:
#     notebook_metadata_filter: -kernelspec,jupytext,jekyll
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
# ---

# %% [markdown]
# ## Exceptions

# %% [markdown]
#
# When we learned about testing, we saw that Python complains when things go wrong by raising an "Exception" naming a type of error:
#
#
#

# %%
1/0

# %% [markdown]
# Exceptions are objects, forming a [class hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy). We just raised an instance
# of the `ZeroDivisionError` class, making the program crash. If we want more
# information about where this class fits in the hierarchy, we can use [Python's
# `inspect` module](https://docs.python.org/3/library/inspect.html) to get a chain of classes, from `ZeroDivisionError` up to `object`:

# %%
import inspect
inspect.getmro(ZeroDivisionError)

# %% [markdown]
#
#
# So we can see that a zero division error is a particular kind of Arithmetic Error.
#
#
#

# %%
x = 1

for y in x:
    print(y)

# %%
inspect.getmro(TypeError)


# %% [markdown]
# ### Create your own Exception

# %% [markdown]
# When we were looking at testing, we saw that it is important for code to crash with a meaningful exception type when something is wrong.
# We raise an Exception with `raise`. Often, we can look for an appropriate exception from the standard set to raise. 
#
# However, we may want to define our own exceptions. Doing this is as simple as inheriting from Exception (or one of its subclasses):

# %%
class MyCustomErrorType(ArithmeticError):
    pass


raise(MyCustomErrorType("Problem"))


# %% [markdown]
#
#
# You can add custom data to your exception:
#
#
#

# %%
class MyCustomErrorType(Exception):
    def __init__(self, category=None):
        self.category = category

    def __str__(self):
        return f"Error, category {self.category}"


raise(MyCustomErrorType(404))

# %% [markdown]
#
#
# The real power of exceptions comes, however, not in letting them crash the program, but in letting your program handle them. We say that an exception has been "thrown" and then "caught".
#
#
#

# %%
import yaml

try:
    config = yaml.safe_load(open("datasource.yaml"))
    user = config["userid"]
    password = config["password"]

except FileNotFoundError:
    print("No password file found, using anonymous user.")
    user = "anonymous"
    password = None


print(user)

# %% [markdown]
#
#
# Note that we specify only the error we expect to happen and want to handle. Sometimes you see code that catches everything:
#
#
#

# %%
try:
    config = yaml.lod(open("datasource.yaml"))
    user = config["userid"]
    password = config["password"]
except:
    user = "anonymous"
    password = None

print(user)

# %% [markdown]
# This can be dangerous and can make it hard to find errors! There was a mistyped function name there ('`lod`'), but we did not notice the error, as the generic except caught it. 
# Therefore, we should be specific and catch only the type of error we want.

# %% [markdown]
# ### Managing multiple exceptions

# %% [markdown]
# Let's create two credential files to read

# %%
with open('datasource2.yaml', 'w') as outfile:
    outfile.write('userid: eidle\n')
    outfile.write('password: secret\n')

with open('datasource3.yaml', 'w') as outfile:
    outfile.write('user: eidle\n')
    outfile.write('password: secret\n')


# %% [markdown]
# And create a function that reads credentials files and returns the username and password to use.

# %%
def read_credentials(source):
    try:
        datasource = open(source)
        config = yaml.safe_load(datasource)
        user = config["userid"]
        password = config["password"]
        datasource.close()
    except FileNotFoundError:
        print("Password file missing")
        user = "anonymous"
        password = None
    except KeyError:
        print("Expected keys not found in file")
        user = "anonymous"
        password = None
    return user, password


# %%
print(read_credentials('datasource2.yaml'))

# %%
print(read_credentials('datasource.yaml'))

# %%
print(read_credentials('datasource3.yaml'))


# %% [markdown]
# This last code has a flaw: the file was successfully opened, the missing key was noticed, but not explicitly closed. It's normally OK, as Python will close the file as soon as it notices there are no longer any references to datasource in memory, after the function exits. But this is not good practice, you should keep a file handle for as short a time as possible.

# %%
def read_credentials(source):
    try:
        datasource = open(source)
        config = yaml.safe_load(datasource)
        user = config["userid"]
        password = config["password"]
    except FileNotFoundError:
        user = "anonymous"
        password = None
    finally:
        datasource.close()

    return user, password


# %% [markdown]
# The `finally` clause is executed whether or not an exception occurs.
#
# The last optional clause of a `try` statement, an `else` clause is called only if an exception is NOT raised. It can be a better place than the `try` clause to put code other than that which you expect to raise the error, and which you do not want to be executed if the error is raised. It is executed in the same circumstances as code put in the end of the `try` block, the only difference is that errors raised during the `else` clause are not caught. Don't worry if this seems useless to you; most languages' implementations of try/except don't support such a clause.

# %%
def read_credentials(source):
    try:
        datasource = open(source)
    except FileNotFoundError:
        user = "anonymous"
        password = None
    else:
        config = yaml.safe_load(datasource)
        user = config["userid"]
        password = config["password"]
    finally:
        datasource.close()
    return user, password


# %% [markdown]
#
#
# Exceptions do not have to be caught close to the part of the program calling
# them. They can be caught anywhere "above" the calling point in
# the call stack: control can jump arbitrarily far in the program: up to the `except` clause of the "highest" containing try statement.
#
#
#

# %%
def f4(x):
    if x == 0:
        return
    if x == 1:
        raise ArithmeticError()
    if x == 2:
        raise SyntaxError()
    if x == 3:
        raise TypeError()


# %%
def f3(x):
    try:
        print("F3Before")
        f4(x)
        print("F3After")
    except ArithmeticError:
        print("F3Except (💣)")


# %%
def f2(x):
    try:
        print("F2Before")
        f3(x)
        print("F2After")
    except SyntaxError:
        print("F2Except (💣)")


# %%
def f1(x):
    try:
        print("F1Before")
        f2(x)
        print("F1After")
    except TypeError:
        print("F1Except (💣)")


# %%
f1(0)

# %%
f1(1)

# %%
f1(2)

# %%
f1(3)

# %% [markdown]
# ### Design with Exceptions

# %% [markdown]
#
# Now we know how exceptions work, we need to think about the design implications... How best to use them.
#
# Traditional software design theory will tell you that they should only be used
# to describe and recover from **exceptional** conditions: things going wrong.
# Normal program flow shouldn't use them.
#
# Python's designers take a different view: use of exceptions in normal flow is
# considered OK. For example, all iterators raise a `StopIteration` exception to
# indicate the iteration is complete.
#
# A commonly recommended Python design pattern is to use exceptions to determine
# whether an object implements a protocol (concept/interface), rather than testing
# on type.
#
# For example, we might want a function which can be supplied *either* a data
# series *or* a path to a location on disk where data can be found. We can
# examine the type of the supplied content:

# %%
import yaml


def analysis(source):
    if type(source) == dict:
        name = source['modelname']
    else:
        content = open(source)
        source = yaml.safe_load(content)
        name = source['modelname']
    print(name)


# %%
analysis({'modelname': 'Super'})

# %%
with open('example.yaml', 'w') as outfile:
    outfile.write('modelname: brilliant\n')

# %%
analysis('example.yaml')


# %% [markdown]
#
#
#
# However, we can also use the try-it-and-handle-exceptions approach to this. 
#
#
#

# %%
def analysis(source):
    try:
        name = source['modelname']
    except TypeError:
        content = open(source)
        source = yaml.safe_load(content)
        name = source['modelname']
    print(name)


analysis('example.yaml')


# %% [markdown]
# This approach is more extensible, and **behaves properly if we give it some
# other data-source which responds like a dictionary or string.**

# %%
def analysis(source):
    try:
        name = source['modelname']
    except TypeError:
        # Source was not a dictionary-like object
        # Maybe it is a file path
        try:
            content = open(source)
            source = yaml.safe_load(content)
            name = source['modelname']
        except IOError:
            # Maybe it was already raw YAML content
            source = yaml.safe_load(source)
            name = source['modelname']
    print(name)


analysis("modelname: Amazing")

# %% [markdown]
# Sometimes we want to catch an error, partially handle it, perhaps add some
# extra data to the exception, and then re-raise to be caught again further up
# the call stack. 
#
# The keyword "`raise`" with no argument in an `except:` clause will cause the
# caught error to be re-thrown. Doing this is the only circumstance where it is
# safe to do `except:` without catching a specific type of error.

# %%
try:
    # Something
    pass
except:
    # Do this code here if anything goes wrong
    raise


# %% [markdown]
# If you want to be more explicit about where the error came from, you can use the `raise from` syntax, which will create a chain of exceptions:

# %%
def lower_function():
    raise ValueError("Error in lower function!")


def higher_function():
    try:
        lower_function()
    except ValueError as e:
        raise RuntimeError("Error in higher function!") from e


higher_function()

# %% [markdown]
#
#
# It can be useful to catch and re-throw an error as you go up the chain, doing any clean-up needed for each layer of a program.
#
# The error will finally be caught and not re-thrown only at a higher program
# layer that knows how to recover. This is known as the "throw low catch high"
# principle.
#
#
#
