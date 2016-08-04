# encoding:utf8

import todoist
import yaml

import argparse


class TodoList(object):
  """Wrap the fetching of todoist todos, and markdown."""    

  def __init__(self, auth_token=None):
    self._client = todoist.TodoistAPI(token=auth_token)

  def todoItems(self, query=None):
    """query syntax is poorly doc'd by todoist api docs."""
    if not query:
      query = "viewall"
    results = {}
    qresults = self._client.query([query])
    if not qresults:
      print "FAIL"
    for project in qresults[0].get('data', []):
      results[project['project_name']] = []
      for todo in project['uncompleted']:
        results[project['project_name']].append(todo['content'])
    return results

  def asText(self, query=None):
    output = ''
    r = self.todoItems(query)
    for p in sorted(r.keys()):
      output += "%s\n" % p
      for i in r[p]:
        output += "[ ] %s\n" % i
    output += "\n"
    return output

  def asMarkdown(self, query=None):
    from jinja2 import Template
    t = Template("""
{%- for project in projects.keys()|sort %}
### {{project}}
{% for i in projects[project] %}
  * {{i}}
{%- endfor %}
{% endfor %}
""")
    return t.render(projects=self.todoItems(query))


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Get ToDoist list')
  parser.add_argument('--config', '-c', help='yaml config file with token')
  parser.add_argument('--token', '-t', metavar='TOKEN', nargs=1,
                      help='api token')

  args = parser.parse_args()

  if args.config:
    cfg = yaml.load(file(args.config))
    args.token = cfg['token']
    l = TodoList(args.token)
    print l.asText()
    #print l.asMarkdown()

