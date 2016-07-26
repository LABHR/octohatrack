# Change Log

## [0.6.1] - 2016-07-26

## Changed
 - pagination now uses `per_page` 100 (thanks @boneskull)

### BugFix
 - consolidating duplicate wiki and github contributors corrected (thanks @boneskull)

## [0.6.0] - 2016-05-04
### Added
 - Ensure Python 3 by adding blockers in `setup.py` and `__main__.py`

### Changed
 - project is now a module, which allows for easier local debugging
 - removed duplicate wiki contributors from main repo contributors

## [0.5.1] - 2016-05-01
### Bugfix
 - confirm git is available within the environment before using (thanks @rogeriopradoj)


## [0.5.0] - 2016-05-01
### Added
 - Ability to parse and add custom contributors based on a specially formatted CONTRIBUTORS file

### Changed
 - Relabelled report; was "Code/Non-Code Contributors", now "GitHub/All Contributors" (thanks @ossanna16)
   - Note: "All" is a superset of the old Code + the old Non-Code (hence, "all").
 - Wiki contributions are always checked, and nicely fails if there's no wiki associated on the repo
 - All old flags removed from the help. Kept for backward compatibility, though (thanks @mjec)

## [0.4.0] - 2016-03-26
### Added
  - Wiki Contributions are now included in the report, based on a list of authors of the username/repo.git repo
    - Note: This uses local git repo cloning, as there is no github wiki API

### Deprecated
 - HTML Output. Deprecated in favour of the web-based [HatRack](https://labhr.github.io/hatrack/)

### Bugfix
 - Corrected pagination logic for GitHub contribution endpoint.

## [0.3.1] - 2016-02-07
### Added
 - Flag to disable local cache (thanks @edunham)

## [0.3.0] - 2015-12-01
### Added
 - Local caching of API results

## [0.2.0] - 2015-11-22
### Changed
 - Project rename. `s/octohat/octohatrack`. [read more](http://glasnt.com/blog/2015/11/21/goodbye-octohat.html)

## [0.1.3] - 2015-09-24
### Added
 - Notification if GitHub rate limit has been exceeded.
### Changed
 - Appropriate use of sessions (thanks @lukasa)
 - Improved HTML output (thanks @stewart-ibm and @freakboy3742)
### Bugfix
 - Prevent hard failure on incomplete GitHub profiles (thanks @tclark)

## [0.1.0] - 2015-08-24
### Bugfix
 - Python 3 compatibility and requirements install properly (thanks @davidjb and @krockode)

## [0.0.2] - 2015-07-26
### Bugfix
 - correct error handling when finding 404 errors on single user API responses

## [0.0.1] - 2015-07-26
### Added
 - initial functionality: insert githubuser/repo, receive statistics.
 - basic html generation
 - limiting to most recent x pull requests/issues

