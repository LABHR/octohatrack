# Octohat

It's easy to see your [code contributions](https://help.github.com/articles/why-are-my-contributions-not-showing-up-on-my-profile/), but what about everything else?

**Octohat** takes a github repo name, and returns a list of every github user that has interacted with a project, but has not committed code. 

Interactions include: 

 * raising or commenting on an issue
 * raising or commenting on a pull request
 * commenting on a commit

"Let's All Build a Hat Rack" ([#LABHR](https://twitter.com/search?q=%23LABHR&src=typd)) is an original concept by [Leslie Hawthorn](http://hawthornlandings.org/2015/02/13/a-place-to-hang-your-hat/)

## Usage

`./octohat.py githubuser/repo`

Define an environment variable for `GITHUB_TOKEN` to use an [authentication token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/) (allows for deeper searching)

## Dependencies

 * [octohub](https://github.com/turnkeylinux/octohub)

## To do
 
 * parallel processing
 * wiki contributions
 * include merge-only contributors as non-code contributors(?)

## License

This code is [MIT licensed](https://github.com/bulletproofnetworks/coco/blob/master/LICENSE).

