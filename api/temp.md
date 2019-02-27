I will explain what I am trying to say with an example:

## Example
# During Registration
email: "EXAMPLE@EXAMPLE.COM"

# Database
email stored in the database: "EXAMPLE@EXAMPLE.COM"
email in the index (we will construct): "example@example.com"

# During Logging In
email: "EXAMPLE@example.com"

## Problem
The email id entered by the user during logging in, does not match the email in database or the lowercase email on which index is constructed.

## Additional Problem
Also, while coming up with a solution we will also have to keep in mind that there might be existing mixed-case emails in the database.

## Solution
Everytime user enters email, we convert it to lowercase and then store it in the database.

## Auxiliary Problem

So let's take an example:
Say the user entered the email "Example@example.com" while registering.
Now, while trying to login he, say, he enters the email: "eXAMple@example.com". He will be rejected as his email will be compared with "example@example.com" only, because that's what we are indexing our database only on lowercase emails.
What I am suggesting is that every time user enters the email we convert it to lowercase, so that when he is registering, the email that get's stored in the database is "example@example.com" and while logging in the email that get's compared with the database is "example@example.com" despite of what the case (mixed-case) that user might use.
This would make the database consistent as with the solution all the email entered in the future would only be in lowercase. However, you are right, there would be a problem of dealing with the currently existing email ids, which would be present in the original case in which user entered them. There are two ways to deal with the problem of these pre-existing email ids:
1. 