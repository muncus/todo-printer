## Print my Todo List (from Todoist).

I like paper, but updating (and keeping track of) a paper todo list isn't easy.

So ive hooked up a thermal printer to a raspberry pi, and now i can print a new
list whenever i want!

## Usage:

This script requires that the python todoist api client be installed:

```
pip install todoist-python
```

`todolist.py` can be run with either `--token` or `--config` options to provide a todoist api token.

To use `--config`, provide a valid yaml file like the following:

```yaml
token: YOURTOKENGOESHERE
```
For help with tokens, see the [ToDoist developer site](https://developer.todoist.com/index.html#authorization)

## Future work
* html templates for todolist output
