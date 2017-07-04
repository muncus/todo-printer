#!/usr/bin/env python
# encoding:utf8

import todoist
import yaml

import argparse
from pprint import pprint

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

  def __init__(self, auth_token=None, config=None):
    if config:
      self._config = yaml.load(file(config))
      self._stored_queries = self._config.get('queries', {})
      auth_token = self._config.get('token', auth_token)
    self._client = todoist.TodoistAPI(token=auth_token)
    self._output_format = 'plain'

  def parseResultsByProject(self, result_obj):
    """Parses a query result that's broken down by project and status."""
    # NB: only the 'viewall' query appears this way, afaik.
    results = {}
    for query_result in result_obj:
      data = query_result.get('data', [])
      for project in data:
        title = project.get('project_name', 'Result')
        results[title] = [i.get('content', None) for i in project['uncompleted']]
    return results

  def parseResults(self, result_obj):
    """Parses a list of query results into a dict by query."""
    results = {}
    for query_result in result_obj:
      data = query_result.get('data', [])
      title = query_result.get('query', 'Query Result')
      results[title] = [i.get('content', None) for i in data]
    return results

  def query(self, query=None):
    """query syntax is poorly doc'd by todoist api docs."""
    if not query:
      query = "viewall"
    # Check pre-configured stored queries.
    if self._stored_queries.has_key(query):
      query = self._stored_queries[query]

    if not type(query) == type([]):
      query = [query]

    qresults = self._client.query(query)
    if not qresults:
      print "FAIL"
    if qresults[0].get('data', [{}])[0].get('project_name', None):
      return self.parseResultsByProject(qresults)
    else:
      return self.parseResults(qresults)

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
    return t.render(projects=self.query(query))


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
    lst = TodoList(auth_token=args.token, config=args.config)
    #import pdb; pdb.set_trace()
    #print l.asText()
    #print l.asMarkdown()
    #print l.asPrinterHtml()
    print lst.asFormat(args.format, args.query)

