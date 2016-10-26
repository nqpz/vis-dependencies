# Dependencies

Datasets are located in the "data" directory.  For example,
"lts-7.3.json" describes all packages in the LTS 7.3 Stackage snapshot.
It is a list of packages.  Each package has five fields:

  + The name.
  + The version.
  + What modules it exposes (only relevant if the package is a library).
  + What modules it imports.
  + Its dependency dictionary.  Each key-value pair in the dependency
    dictionary consists of the package name of the dependency (the key)
    and a list of the modules from that package in use (the value).
  + Its source code repository if it has one.

**Dataset extraction note**: Depended-upon modules are only referenced
by name, and not also by the required version range.  This is a
simplification.  It is still valid, since everything is contained within
the same Stackage snapshot, and so any reference will be consistent and
okay.

Github data
the github data contains the properties

  + The name(which is the same as the original package
  + A json object containing several fields

Interesting fields are

  + "stargazers_count"
  + "subscribers_count"
  + "forks"
  + "watchers"
  + "open_issues_count"
  
