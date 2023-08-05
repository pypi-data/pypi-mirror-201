# name2user
name2user is a tool to generate potential user names from one or a list of full names. Possible use-cases are password cracking with tools like hydra together with a word list or account discovery in different services.

## Usage
```shell
name2user "Liam Smith"
```
Outputs all available user name variations for given full name.

```shell
name2user "Olivia Johnson" -c flast
```
Outputs user name variation FLAST (see below) for given full name.


```shell
name2user "Noah Williams" -m "somecompany.com"
```
Outputs all available user name variations for given full name followed by an @ and the domain.

```shell
cat some_text_file | name2user
```
Outputs all available user name variations for all full names in given text file.

```shell
cat some_text_file | name2user -c fulld > results.txt
```
Outputs user name variation FULLD for all full names in given text file and pipes them to results.txt.

## Conversion types
name2user support seven conversion modes:

| **Parameter** | **Description**                                 |
|---------------|-------------------------------------------------|
| all           | Generates all below variants.                   |
| last          | Last name only.                                 |
| flast         | First letter of the first name, last name.      |
| fdlast        | First letter of the first name, dot, last name. |
| full          | Full first- and last name without spaces.       |
| fulld         | Full first- and last name separated by dots.    |
| first         | First name only.                                 |

## Limitations
- Right now, name2user is designed with western languages in mind. It might produce less helpful results for other.
- For names with more than two words, the last word is considered as last name. The first letter of the first word will be used for corresponding conversion types. Ones using the full name will include all words.
