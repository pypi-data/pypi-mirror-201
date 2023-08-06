# y42-client-python
A Python client library for the Y42 API. 
It also contains a `y42` CLI utility for local development, built on this library.

Note: The underlying API is currently still in an unstable 0.0.x release, 
meaning things (like this library and CLI) may break unexpectedly from time to time.

## Installation
Both the library and CLI tool can be installed via `pip3 install y42`.

## Python library usage
TODO - check the `tests` folder for some examples for now.

## Create a new release

- Bump `version` in `pyproject.toml` to desired semver release.
- Commit change with `chore: bump version to x.y.z`.
- Tag change with `git tag x.y.z`.
- Push new commit together with tag.

## CLI
### Authorization
The CLI utility will look for a Y42_API_KEY environment variable. You can also specify, or override, the API key via the --api-key flag.

### Help
Run `y42 --help` to get help with commands:
```console
foo@bar:~$ y42               
                                                                                                                                                  
 Usage: y42 [OPTIONS] COMMAND [ARGS]...                                                                                                       
                                                                                                                                                  
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --environment               TEXT  Override for Y42_ENVIRONMENT ('prod' or 'dev') [default: None]                                               │
│ --api-key                   TEXT  Override for Y42_API_KEY [default: None]                                                                     │
│ --install-completion              Install completion for the current shell.                                                                    │
│ --show-completion                 Show completion for the current shell, to copy it or customize the installation.                             │
│ --help                            Show this message and exit.                                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ company    List/activate companies                                                                                                             │
│ git        Helper alias for system's own `git` that applies Y42 authorization headers.                                                         │
│ repos      Print all currently cloned spaces and their local git repository directories.                                                       │
│ reset      Reset the local Y42 state. This does not delete your cloned repositories, (but will unlink them from the Y42 CLI).                  │
│ space      Manage spaces in Y42                                                                                                                │
│ state      Prints the current Y42 CLI app state in JSON format.                                                                                │
│ status     Show currently active company and space, if any.                                                                                    │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

foo@bar:~$ y42 company --help
                                                                                                                                                  
 Usage: y42 company [OPTIONS] COMMAND [ARGS]...                                                                                               
                                                                                                                                                  
 List/activate companies                                                                                                                          
                                                                                                                                                  
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                    │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ activate      Activate company. Only needed if the specified Y42_API_KEY allows access to multiple companies.                                  │
│ info          Print information about the specified (or only known) company in JSON format.                                                    │
│ ls            Refresh and print the list of known Y42 companies for your current credentials.                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

foo@bar:~$ y42 space --help  
                                                                                                                                                  
 Usage: y42 space [OPTIONS] COMMAND [ARGS]...                                                                                                 
                                                                                                                                                  
 Manage spaces in Y42                                                                                                                             
                                                                                                                                                  
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                    │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ clone    Helper for running `git clone` against the specified space's git repository.                                                          │
│ info     Print information about the specified space. If no space is specified, the current working directory must be a space.                 │
│ locate   Print the directory that the space has been cloned to, if any.                                                                        │
│ ls       List known spaces                                                                                                                     │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


```

Basic CLI workflow:
- Create an API key in Y42 and set Y42_API_KEY to this token, e.g. via `export Y42_API_KEY="your-api-key"`.
- List your available spaces via `y42 space ls`
- Clone a space via `y42 clone <space name or index> <target>`
- cd into the space via `cd target`, or alternatively via `cd $(y42 space locate <space name or index>)`
- Run git commands in the space, via `y42 git`, e.g. `y42 git add .` or `y42 git commit -am "Hello World!"`


### Example CLI usage:
```console
foo@bar:~$ y42 space ls
No known companies, refreshing..
No active company, defaulting to only known company my_company
0: some-space
1: another_space
2: test_space
foo@bar:~$ y42 space clone test_space  # could also use "2" instead of "test_space" here
Space will be cloned to /Users/foo/spaces/test_space. Proceed? [Y/n]
[Shell stderr output]
Cloning into '/Users/foo/spaces/test_space'...
foo@bar:~$ cd $(y42 space locate test_space)
foo@bar:~$ touch hello.txt
foo@bar:~$ y42 git add hello.txt # "y42" is optional for these kinds of local git commands
foo@bar:~$ y42 git commit -am "added hello.txt"
[Shell stdout output]
[main f285d88] added hello.txt
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 hello.txt
test_space > y42 git push
[Shell stderr output]
remote: [2b9cf0b112f709fbbef92066ce765369a698d45c..f285d8832701cb0712361d6e7b9b407722edde56] Response: Number of files:1, code:200, body:[true]        
remote: [2b9cf0b112f709fbbef92066ce765369a698d45c..f285d8832701cb0712361d6e7b9b407722edde56] Response: Number of files:1, code:200, body:[]        
To https://api.dev.y42.dev/gateway/companies/524/spaces/9f095dd1-1c32-4a7d-bb74-a431a8dfdece/git
   2b9cf0b..f285d88  main -> main
foo@bar:~$ y42 status
Configured Y42 root directory: /Users/foo/Library/Application Support/y42
Active company: my_company
Space in current directory: test_space
foo@bar:~$ y42 repos 
my_company/test_space -> /home/users/foo/spaces/test_space

```
