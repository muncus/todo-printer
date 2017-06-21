#!/usr/bin/env python
# encoding:utf8

import todoist
import yaml

import argparse

from jinja2 import Template


class TodoList(object):
  """Wrap the fetching of todoist todos, and markdown."""    

  _plain_template = Template("""
{%- for project in projects.keys()|sort %}
{{project}}
{% for i in projects[project] %}
  [ ] {{i}}
{%- endfor %}
{% endfor %}
""")

  _markdown_template = Template("""
{%- for project in projects.keys()|sort %}
### {{project}}
{% for i in projects[project] %}
  * {{i}}
{%- endfor %}
{% endfor %}
""")

  _html_template = Template("""
<style type="text/css">
html, body {
  -webkit-font-smoothing: none;
  width: 384px;
  overflow: hidden;
  margin: 0 auto;
  background-color: white; }
</style>
<body>
{%- for project in projects.keys()|sort %}
<h3>{{project}}</h3>
<ul>
{% for i in projects[project] %}
  <li>{{i}}</li>
{%- endfor %}
</ul>
{% endfor %}
</body>
""")

  def __init__(self, auth_token=None):
    self._client = todoist.TodoistAPI(token=auth_token)
    self._output_format = 'plain'

  def todoItems(self, query=None):
    """query syntax is poorly doc'd by todoist api docs."""
    if not query:
      query = "viewall"
    results = {}
    qresults = self._client.query([query])
    if not qresults:
      print "FAIL"
    data = qresults[0].get('data', [])
    for project in qresults[0].get('data', []):
      proj_key = project.get('project_name', 'Query Results')
      results[proj_key] = []
      # default query lists projects, broken down by state.
      if project.has_key('uncompleted'):
        for todo in project['uncompleted']:
          if todo['checked'] == 1:
            continue
          results[proj_key].append(todo['content'])
      else:
      # queries with non-default filters are not.
        for item in data:
          if item['checked'] == 1:
            continue
          results[proj_key].append(item['content'])
    return results

  def asText(self, query=None):
    return self.asFormat('plain', query)

  def asMarkdown(self, query=None):
    return self.asFormat('markdown', query)

  def asPrinterHtml(self, query=None):
    return self.asFormat('html', query)

  def asFormat(self, tmpl, query=None):
    output_formats = {
      'plain': self._plain_template,
      'html' : self._html_template,
      'md' : self._markdown_template,
      'markdown' : self._markdown_template,
    }
    t = output_formats[tmpl]
    return t.render(projects=self.todoItems(query))


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Get ToDoist list')
  parser.add_argument('--config', '-c', help='yaml config file with token')
  parser.add_argument('--token', '-t', metavar='TOKEN', nargs=1,
                      help='api token')
  parser.add_argument('--format', '-f', default='plain',
      help="type of output desired. html, markdown, plain")
  parser.add_argument('--query', '-q',
      help="todoist query. syntax is https://todoist.com/Help/Filtering",
      default=None)

  args = parser.parse_args()

  if args.config:
    cfg = yaml.load(file(args.config))
    args.token = cfg['token']
    l = TodoList(args.token)
    #print l.asText()
    #print l.asMarkdown()
    #print l.asPrinterHtml()
    print l.asFormat(args.format, args.query)

