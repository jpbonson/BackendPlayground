import re

rawString = r'and this is a\nraw string' # and this is a\nraw string
re.match()
re.search()
re.findall()
re.sub()

# re.match() checks for a match only at the beginning of the string, while re.search() checks for a match anywhere in the string.

contactInfo = 'Doe, John: 555-1212'
match = re.search(r'(\w+), (\w+): (\S+)', contactInfo)
>>> match.group(1)
'Doe'
>>> match.group(2)
'John'
>>> match.group(3)
'555-1212'
>>> match.group(0)
'Doe, John: 555-1212'
match = re.search(r'(?P<last>\w+), (?P<first>\w+): (?P<phone>\S+)', contactInfo)
>>> match.group('last')
'Doe'
>>> match.group('first')
'John'
>>> match.group('phone')
'555-1212'

line = "Cats are smarter than dogs"
matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)
matchObj.group(1) :  Cats
matchObj.group(2) :  smarter

phone = "2004-959-559 # This is Phone Number"
# Delete Python-style comments
num = re.sub(r'#.*$', "", phone)
print "Phone Num : ", num # Phone Num :  2004-959-559
# Remove anything other than digits
num = re.sub(r'\D', "", phone)    
print "Phone Num : ", num # Phone Num :  2004959559

## Search for pattern 'iii' in string 'piiig'.
## All of the pattern must match, but it may appear anywhere.
## On success, match.group() is matched text.
match = re.search(r'iii', 'piiig') =>  found, match.group() == "iii"
match = re.search(r'igs', 'piiig') =>  not found, match == None
## . = any char but \n
match = re.search(r'..g', 'piiig') =>  found, match.group() == "iig"
## \d = digit char, \w = word char
match = re.search(r'\d\d\d', 'p123g') =>  found, match.group() == "123"
match = re.search(r'\w\w\w', '@@abcd!!') =>  found, match.group() == "abc"

str = 'purple alice-b@google.com monkey dishwasher'
match = re.search(r'[\w.-]+@[\w.-]+', str)
if match:
    print match.group()  ## 'alice-b@google.com'

 str = 'purple alice-b@google.com monkey dishwasher'
match = re.search('([\w.-]+)@([\w.-]+)', str)
if match:
    print match.group()   ## 'alice-b@google.com' (the whole match)
    print match.group(1)  ## 'alice-b' (the username, group 1)
    print match.group(2)  ## 'google.com' (the host, group 2)

## Suppose we have a text with many email addresses
str = 'purple alice@google.com, blah monkey bob@abc.com blah dishwasher'
## Here re.findall() returns a list of all the found email strings
emails = re.findall(r'[\w\.-]+@[\w\.-]+', str) ## ['alice@google.com', 'bob@abc.com']
for email in emails:
# do something with each found email string
print email

# Open file
f = open('test.txt', 'r')
# Feed the file text into findall(); it returns a list of all the found strings
strings = re.findall(r'some pattern', f.read())

str = 'purple alice@google.com, blah monkey bob@abc.com blah dishwasher'
tuples = re.findall(r'([\w\.-]+)@([\w\.-]+)', str)
print tuples  ## [('alice', 'google.com'), ('bob', 'abc.com')]
for tuple in tuples:
print tuple[0]  ## username
print tuple[1]  ## host

str = 'purple alice@google.com, blah monkey bob@abc.com blah dishwasher'
## re.sub(pat, replacement, str) -- returns new string with all replacements,
## \1 is group(1), \2 group(2) in the replacement
print re.sub(r'([\w\.-]+)@([\w\.-]+)', r'\1@yo-yo-dyne.com', str)
## purple alice@yo-yo-dyne.com, blah monkey bob@yo-yo-dyne.com blah dishwasher

# http://www.tutorialspoint.com/python/python_reg_expressions.htm