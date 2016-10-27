d3.json('lts-7.3-collection.json', function(error, json) {
  if (error) {
    document.write(error);
  }
  else {
    visualize(json, 240);
  }
});

function dependency_entries(p, d) {
  var m = p['maximums'];
  var entries = [ ['Use of modules',
                   [d['number_of_modules'] / d['total_number_of_modules'], 1.0]]
                  , ['Number of uses',
                     [d['number_of_uses'], m['number_of_uses']]]
                ];
  if (d['github'] && m['github']) {
    l = d['github']
    g = m['github']
    entries.push(['Forks on GitHub',
                  [l['forks'], g['forks']]]);
    entries.push(['Number of open issues on GitHub',
                  [l['open_issues_count'], g['open_issues_count']]]);
    entries.push(['Number of stargazers on GitHub',
                  [l['stargazers_count'], g['stargazers_count']]]);
    entries.push(['Number of subscribers on GitHub',
                  [l['subscribers_count'], g['subscribers_count']]]);
    entries.push(['Number of watchers on GitHub',
                  [l['watchers'], g['watchers']]]);
  }
  return entries;
}

var bar_length = 600;

function visualize(packages, package_index) {
  pac = packages[package_index];

  d3.select('body')[0][0].innerHTML = '';
  
  var header = d3.select('body')
      .append('h1');
  header.text('Dependencies of ' + pac['name']);

  var dependency_list = d3.select('body')
      .append('dl');
  
  var list_values = dependency_list.selectAll('dd')
      .data(pac['dependencies'])
      .enter()
      .append('dd');

  var list_keys = dependency_list.selectAll('dt')
      .data(pac['dependencies'])
      .enter()
      .insert('dt', function(d, i) { return list_values[0][i]; });

  list_keys.text(function(d) { return d['name']; });
  list_keys.on('click', function(d) { visualize(packages, d['index']); });

  var value_groups = list_values.selectAll('div')
      .data(function(d) { return dependency_entries(pac, d); })
      .enter()
      .append('div');

  var value_keys = value_groups.append('p')
      .attr('class', 'attribute_name');
  var value_values = value_groups.append('p')
      .attr('class', 'attribute_value');

  value_keys.text(function(d) { return d[0]; });
  value_values.append('div')
    .attr('class', 'full_bar')
    .style('width', bar_length + 'px');
  value_values.append('div')
    .attr('class', 'local_bar')
    .style('width', function(d) { return ((bar_length / d[1][1]) * d[1][0]) + 'px'; });
  value_values.append('div')
    .attr('class', 'actual_value')
    .text(function(d) { return d[1][0] + '/' + d[1][1]; })
  
}
